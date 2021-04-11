import logging
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import typer
import yaml

from .gaussian_io import io
from .runner import determine_next_stage, run_next_stage, setup_next_stage
from .utils.utils import load_project_file

logger = logging.getLogger(__name__)

MOLECULE_CONF_REGEX = re.compile(r"(?P<molecule>[A-z]+)-(?P<conf>\d+).mol2")


def check_and_map_filenames(mol: Path) -> str:
    """check if filename is a valid project filename including a conf otherwise create one"""
    mol_str = str(mol)
    res = MOLECULE_CONF_REGEX.fullmatch(mol_str)
    if res:
        return mol_str
    else:
        mol_str = Path(mol).stem.replace("-", "_")
        mol_str = mol_str + "-{conf}.mol2"
        logger.info(
            f"No configurtaion id given, adding placeholder and normalizing. Filename will be: {mol_str}"
        )
        return mol_str


def resolve_mol2_files(
    mol2_files: List[Path], mol2_files_in_mol2_folder: List[Path]
) -> Dict[Path, Path]:
    """This function handles all mol2 files in the root directory and what to do.

    For files with the right structure it will just process them as is.
    For files that don't have the proper structure it will take note of them
    and then add proper names for them at the end.

    mol2_files: List of mol2 files in the root folder
    mol2_files_in_mol2_folder: List of mol2 files in the mol2 folder

    Returns: A dict of all files that need to be run and their potential
        name mapping if they did not adhere to the naming convention.
    """
    # keep track of the hightest  configuration number per molecule
    molecule_configuration: Dict[str, int] = {}
    correct_mol2_to_process: Dict[Path, Path] = {}
    for mol in mol2_files_in_mol2_folder:
        molecule, conf = mol.stem.split("-")
        if int(conf) > molecule_configuration.get(molecule, -1):
            molecule_configuration[molecule] = int(conf)

    for mol in mol2_files:
        checked_mol_path = check_and_map_filenames(mol)
        if checked_mol_path in mol2_files_in_mol2_folder:
            logger.warning("Molecule already running, this file wont be added: {mol}")
            continue
        else:
            molecule, _ = Path(checked_mol_path).stem.split("-")
            conf_init = molecule_configuration.get(molecule, 0)
            new_path = Path(checked_mol_path.format(conf=conf_init + 1))
            correct_mol2_to_process[mol] = new_path

    return correct_mol2_to_process


def mol2_to_gjf(p_df: pd.DataFrame, config: dict, config_file: Path) -> List[Path]:
    """Generates a gjf file for every mol2 file.

    Parameters:
        p_df: Project log dataframe loaded from the project.log file.
        config: Dict that contains the overall project configuration details.
        config_file: Name of the configuration file

    Returns:
        conf_to_run: List of gjf files that need running
    """
    mol2_files_in_mol2_folder = list(Path("mol2_folder/").glob("*.mol2"))
    mol2_files = list(Path("./").glob("*.mol2"))
    conf_to_run = []
    if mol2_files == []:
        return []
    else:
        mol2_to_process = resolve_mol2_files(mol2_files, mol2_files_in_mol2_folder)
        if len(mol2_to_process) < 1:
            return []
        for mol, target_mol in mol2_to_process.items():
            molecule, conf, *rest = Path(target_mol).stem.split("-")
            assert conf.isnumeric(), "Configuration should be a number"
            # the following if condition checks in case mol2 files were added later
            # but others are already running and runs only those that are not
            # yet running. There could be cases where configurations are running
            # but have not finished so the project log don't include them yet.
            # This can cause multipe runs being started for the same structure.
            if (p_df["conf"] == int(conf)).sum() == 0:
                gaussian_input_filename = Path(f"0_iteration/{molecule}-{conf}-0.gjf")
                # Create the filepath if it does not exist yet
                Path(gaussian_input_filename).parents[0].mkdir(
                    parents=True, exist_ok=True
                )
                # generate the gjf file at the target location
                io(
                    input_files=[str(mol)],
                    input_format="mol2",
                    config_file=config_file,
                    output_file_name=str(gaussian_input_filename),
                    section=config["first-stage"],
                    iteration=0,
                )
                # move mol2 file into the mol2 folder
                shutil.move(str(mol), f"mol2_folder/{target_mol}")
                conf_to_run.append(gaussian_input_filename)
    return conf_to_run


def not_finished_simulations(
    p_project_log: Path, p_config: Path
) -> List[Tuple[Tuple[int, int, int], Path]]:
    """Determine which simulation have not finished and generate new inputfiels

    A simulation is considered finished if the project.log files indicates this.
    What counts as a finished simulation is determined by the logic included in
    the reporting script and can be altered there.
    """
    with open(p_config) as stream:
        config = yaml.safe_load(stream)
    project_df = load_project_file(p_project_log)
    not_finished = project_df[project_df["finished"] == False].reset_index()  # noqa
    last_states = not_finished.sort_values("iteration").drop_duplicates(
        subset=["conf"], keep="last"
    )
    simulation_details = []
    for _, previous_state in last_states.iterrows():
        project = config["project_name"]
        iteration = previous_state["iteration"]
        conf = previous_state["conf"]
        p_gaussian_out = Path(
            (f".{iteration}_iteration/" f"{project}-{conf}-{iteration}.out")
        )
        next_stage = determine_next_stage(previous_state, p_config)
        new_gjf_file = setup_next_stage(
            p_gaussian_out, previous_state, next_stage, p_config
        )
        if new_gjf_file is None:
            continue
        simulation_details.append(
            run_next_stage(new_gjf_file, p_config, p_project_log, next_stage)
        )
    return simulation_details


def workflow(
    config_file: Path = typer.Option(
        "config.yaml", help="The project configuration file."
    ),
    project_file: Path = typer.Option("project.log", help="The project log file."),
) -> None:
    """This function will start or continue a workflow defined by config.yaml.

    It will load the config and create or load the project log file as necessary.
    It will check if there are any mol2 files in the root directory. If there are,
    it will create gaussian submission files for those and move them to the mol2_folder.
    There are some sanity checks included so that no existing mol2 files or running structures
    are overwritten.

    Subsequently it will check if there are any structures that have not finished
    the workflow as defined in config.yaml and restart them at the appropriate step
    if necessary.

    WARNING: This will not take into account any structures currently runnning or queued.
    Therefore it might start a second set of simulations for a structure currently in the slurm queue!
    Ideally use this command only once at the beginning or when no structures of this experiment
    are running/queued.
    """
    with open(config_file, "r") as stream:
        config = yaml.safe_load(stream)
    project_df = load_project_file(project_file)
    mol2path = Path("mol2_folder/")
    # All mol2 structures in the root project directory, should
    # be moved into a subdirectory once they have been used to
    # kick of their respective simulations.
    # Thus a mol2 foleder is created here if it does not already exist
    mol2path.mkdir(parents=True, exist_ok=True)
    # constraint section and start-up
    not_run_gjf = mol2_to_gjf(project_df, config, config_file)
    logger.info(f"List of not run mol2 files: {not_run_gjf}")
    for gjf_file in not_run_gjf:
        _ = run_next_stage(gjf_file, config_file, project_file, config["first-stage"])
    continued_simulations = not_finished_simulations(project_file, config_file)
    logger.info(f"List of continued simulations: {continued_simulations}")
