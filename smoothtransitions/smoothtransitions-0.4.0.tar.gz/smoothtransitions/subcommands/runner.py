import logging
import shutil
from pathlib import Path
from typing import Tuple, Union

import pandas as pd
import typer
import yaml

from .gaussian_io import io
from .utils.utils import STCOLUMNS, Slurm, load_project_file

logger = logging.getLogger(__name__)


def load_previous_state(p_gauss_out: Path, p_project_log: Path) -> pd.Series:
    """
    This functions loads the previous state from the project log file

    It also does several sanity checks. First it checks if the history of the
    configuration being checked is longer than 0, then if the number of iterations
    indicated by the filename is different than 0 and raises an Error otherwise.
    If it is the first iteration and no entry exists it creates a dummy state
    so that other functions can continue working.

    Parameters:
        p_gauss_out: Path to the gaussian output file.
        p_project_log: Path to the project log file.

    Returns:
        previous_state: Pandas Series that describes the previous state
    """
    project_log = load_project_file(p_project_log)
    molecule, conf, iteration = p_gauss_out.stem.split("-")
    # Get history of the state we are looking at
    state_history = project_log[
        (project_log["molecule"] == molecule) & (project_log["conf"] == conf)
    ].reset_index(drop=True)
    # If there is no history of a state but iteration count is larger
    # than 0 than raise an error
    if (len(state_history) == 0) and (iteration != "0"):
        raise ValueError(
            (
                "No history for this configuration found, "
                "log corrupt or wrong run please check manually"
            )
        )
    # check if this was the first iteration and if so load the first-iter
    elif (len(state_history) == 0) and (iteration == "0"):
        return pd.Series(
            [
                molecule,
                conf,
                "-1",
                False,
                False,
                False,
                False,
                False,
                False,
                "first-stage",
            ],
            index=STCOLUMNS,
        )
    else:
        return state_history.sort_values("iteration").iloc[-1]


def determine_next_stage(previous_state: pd.Series, p_config: Path) -> str:
    """
    Function to determine the next stage of the simulation run.

    Parameters:
        previous_state: Pandas Series that describes the
            previous state of the configuration.
        p_config: Path to the project configuration file.

    Returns:
        next_stage: String that identifies the section in the
            config that should be used to generate the next gjf file.
    """
    with open(p_config, "r") as stream:
        config = yaml.safe_load(stream)
    previous_stage = previous_state["stage"]
    # Here account for the fact that the previous stage could have been
    # the first stage and thus needs to check what should be run now.
    if previous_stage == "first-stage":
        previous_stage = config["first-stage"]
        config_previous_stage = config[previous_stage]
    elif previous_stage == "error":
        return "abort"
    else:
        config_previous_stage = config[previous_stage]
    if previous_stage == "optimisation":
        # check if converged. if yes then initiate next stage or abort
        if previous_state[["geo_opt_done", "vib_freq_done", "stationary"]].all():
            return config_previous_stage.get("next-stage", "abort")
    # Thus far there is no case where we would continue an SPE run
    elif previous_stage == "SPE":
        return "abort"
    # in all other cases check the config for what to do next
    if (int(previous_state["iteration"]) + 1) == config_previous_stage["max-iter"]:
        return config_previous_stage.get("after-max-iter", "abort")
    # abort if for some reason the number of iteration is bigger than
    # the maximum allowed number of iterations
    elif (int(previous_state["iteration"]) + 1) > config_previous_stage["max-iter"]:
        return "abort"
    else:
        return previous_stage


def setup_next_stage(
    gaussian_output: Path, previous_state: pd.Series, next_stage: str, p_config: Path
) -> Union[Path, None]:
    """
    Function that will generate the next stage gjf file.

    Parameters:
        gaussian_output: Gaussian output file
        previous_state: Pandas Series that describes the previous state
        next_stage: string that identifies the next section in the config
        p_config: Path to the project config file

    Returns:
        next_stage_gjf_file: Path to the next gjf file location
    """
    molecule, conf, _ = gaussian_output.stem.split("-")
    # if the next stage is abort return None so nothing is done
    if next_stage == "abort":
        return None
    # treat SPE stages specially because of GoodVibes and other dependancies
    elif next_stage == "SPE":
        previous_iter = int(previous_state["iteration"])
        next_iteration = str(previous_state["iteration"]) + "_SPE"
        next_iteration_folder = "SPE"
        io_iter = None
    else:
        previous_iter = io_iter = int(previous_state["iteration"])
        io_iter -= 1
        io_iter = max(0, io_iter)
        next_iteration = next_iteration_folder = str(previous_iter + 1)

    previous_stage_out_file = (
        f"{previous_iter}_iteration/" f"{molecule}-{conf}-{previous_iter}.out"
    )
    next_stage_gjf_file = Path(
        f"{next_iteration_folder}_iteration/" f"{molecule}-{conf}-{next_iteration}.gjf"
    )
    Path(next_stage_gjf_file).parents[0].mkdir(parents=True, exist_ok=True)
    # Copies the output file for the final converged optimisation so that Goodvibes
    # can incorporate both the optimisation and SPE files into energy extraction
    if next_stage == "SPE":
        shutil.copyfile(
            Path(previous_stage_out_file),
            Path(next_stage_gjf_file).parents[0] / Path(previous_stage_out_file).name,
        )
    io(
        input_files=[previous_stage_out_file],
        input_format="g09",
        config_file=p_config,
        section=next_stage,
        output_file_name=str(next_stage_gjf_file),
        iteration=io_iter,
    )
    return next_stage_gjf_file


def run_next_stage(
    p_gjf: Path, p_config: Path, p_project_log: Path, stage: str
) -> Tuple[Tuple[int, int, int], Path]:
    """
    Function that actually executes all slurm jobs.

    Parameters:
        p_gjf: Path to the gjf file to run
        p_config: Path to the project configuration file
        p_project_log: Path to the project log file
        stage: stage to be run

    Returns:
        (ids), gaussian_output_file: ids of jobs submitted
            and path to gaussian outputfile
    """
    molecule, conf, _ = p_gjf.stem.split("-")
    with open(p_config, "r") as stream:
        config = yaml.safe_load(stream)
    gaussian_output_file = (p_gjf.parent / p_gjf.name).with_suffix(".out")
    # load slurm instance for gaussian config
    slurm = Slurm(
        f"{molecule}-{stage}-{conf}",
        config[stage]["slurm"]["settings"],
        bash_strict=False,
    )
    # load slurm instance with smoothtransitions config
    slurm_st = Slurm(
        f"{molecule}-{stage}-{conf}",
        config["smoothtransitions"]["slurm"]["settings"],
        bash_strict=False,
    )
    j_id = slurm.run(
        config[stage]["slurm"]["command"],
        cmd_kwargs={"gjf_file": f"{p_gjf}", "outputfile": f"{gaussian_output_file}"},
        name_addition="gaussian",
    )
    # add the reporting script as a dependency
    j_id_report = slurm_st.run(
        config["smoothtransitions"]["slurm"]["report-command"],
        cmd_kwargs={
            "gaussianoutfile": str(gaussian_output_file),
            "configfile": str(p_config),
            "projectfile": str(p_project_log),
        },
        depends_on=[j_id],
        name_addition="report",
    )
    j_id_runner = slurm_st.run(
        config["smoothtransitions"]["slurm"]["runner-command"],
        cmd_kwargs={
            "configfile": str(p_config),
            "projectfile": str(p_project_log),
            "gaussianoutfile": str(gaussian_output_file),
        },
        depends_on=[j_id_report],
        name_addition="runner",
    )
    return (j_id, j_id_report, j_id_runner), gaussian_output_file


def check_file_is_output(p_gaussian_out: Path) -> Path:
    if p_gaussian_out.suffix != ".out":
        raise typer.BadParameter(
            "The input file must be a gaussian output file ending in *.out."
        )
    return p_gaussian_out


def runner(
    gaussian_output_file: Path = typer.Argument(
        ...,
        help="A gaussian output file.",
        callback=check_file_is_output,
    ),
    config_file: Path = typer.Option(
        "config.yaml", help="The project configuration file."
    ),
    project_file: Path = typer.Option("project.log", help="The project log file."),
) -> Union[Tuple[Tuple[int, int, int], Path], None]:
    """
    This command will do two things:

    1) Determine what needs to be run next within the defined worfklow.
    It will use the project log file, the config file and the output to determine
    where in the workflow the current structure is and what to do next.

    2) Run the next step (if any) of the workflow for the respective structure.
    """
    previous_state = load_previous_state(gaussian_output_file, project_file)
    next_stage = determine_next_stage(previous_state, config_file)
    new_gjf_file = setup_next_stage(
        gaussian_output_file, previous_state, next_stage, config_file
    )
    if new_gjf_file is None:
        return None
    j_ids, gaussian_out_file = run_next_stage(
        new_gjf_file, config_file, project_file, next_stage
    )
    return j_ids, gaussian_out_file
