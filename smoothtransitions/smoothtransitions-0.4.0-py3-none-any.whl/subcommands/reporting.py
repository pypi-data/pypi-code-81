import logging
from pathlib import Path
from typing import List

import cclib
import numpy as np
import pandas as pd
import typer
import yaml
from matplotlib import pyplot as plt

from .runner import determine_next_stage, load_previous_state
from .utils.gaussian_ts import GaussianTS
from .utils.utils import STCOLUMNS, load_project_file

logger = logging.getLogger(__name__)


def generate_distance_graph(atoms: List[int], data: cclib, f_title: str) -> np.ndarray:
    """Create a plot and png of the distance between two atoms

    Parameters:
        atoms: List of integers that determine the atom id.
        data: Data object created from cclib by reading in
            the gaussian output file.
        f_title: Title of the figure.
    """
    fig, axes = plt.subplots()
    distances = data.calculate_distances(atoms)
    elems = data.get_elements()
    axes.plot(distances)
    title = (
        f"Distance between {elems[atoms[0]]}-{atoms[0]} "
        f"and {elems[atoms[1]]}-{atoms[1]}"
    )
    axes.set_title(title)
    axes.set_xlabel("cycles")
    axes.set_ylabel("distances (A)")
    fig.savefig(f"{f_title}_{title.replace(' ', '_')}.png", dpi=200)
    return distances


def update_project_file(
    df: pd.DataFrame, file_name: Path, cclib_data: cclib, stage: str
) -> pd.DataFrame:
    """Update the project log file with data from the most recent completed ST run.

    Parameters:
    df: DataFrame containing the current progress of the project.
    name: Name of the gaussian output file.
    cclib_data: Data object created by cclib when reading in the
        Gaussian output file.

    Returns:
        Updated version of the project.log dataframe.
    """
    molecule, name_based_conf, name_based_iter = file_name.stem.split("-")
    current_view = df.loc[
        (df["molecule"] == molecule) & (df["conf"] == name_based_conf)
    ]
    # Check if SPE was already run
    if "SPE" in current_view["iteration"].values:
        logger.error("This structure has already an SPE entry -> skipping update")
        return pd.DataFrame(columns=STCOLUMNS)
    if len(current_view) == 0:
        log_based_iter = -1
    else:
        log_based_iter = int(current_view["iteration"].max())
    if ("SPE" not in name_based_iter) and (
        not int(name_based_iter) == (log_based_iter + 1)
    ):
        logger.error(
            (
                f"Iteration {name_based_iter} for conf {name_based_conf} "
                f"already exists in project log file -> skipping update"
            )
        )
        return pd.DataFrame(columns=STCOLUMNS)
    # check if all three opt have been True at some point
    finished_value = (
        current_view[["geo_opt_done", "vib_freq_done", "stationary", "SPE_done"]]
        .max(axis=0)
        .sum()
    )
    # Check if all conditions for a successful calculation are there
    if finished_value == 3 and cclib_data.spe_done and "SPE" in name_based_iter:
        finished = True
    else:
        finished = finished_value == 4
    # stationary can happen in two ways so check both here
    stationary = cclib_data.stationary_full or cclib_data.stationary_close_enough
    # In order to keep the index of the project log file continuous we update it here.
    # However, if no entry is in the project log (and thus in this dataframe).
    # We capture this case here and assign it the 0 entry to avoid any NaNs in our index.
    if df.index.max() is np.nan:
        idx = [0]
    else:
        idx = [max(0, df.index.max()) + 1]
    temp = pd.DataFrame(
        [
            {
                "molecule": molecule,
                "conf": name_based_conf,
                "iteration": name_based_iter,
                "geo_opt_done": cclib_data.opt_done,
                "vib_freq_done": cclib_data.freq_done,
                "stationary": stationary,
                "SPE_done": cclib_data.spe_done,
                "constrained": cclib_data.is_constrained,
                "finished": finished,
                "stage": stage,
            }
        ],
        index=idx,
    )
    return temp


def check_files_are_output(input_files: List[Path]) -> List[Path]:
    if not all([f.suffix == ".out" for f in input_files]):
        raise typer.BadParameter(
            "One of the Input files is not a gaussian output file. "
            "They should all end with *.out"
        )
    return input_files


def report(
    input_files: List[Path] = typer.Argument(
        ...,
        help="One or more input files for which reporting should be done.",
        callback=check_files_are_output,
    ),
    config_file: Path = typer.Option(
        "config.yaml", help="The project configuration file."
    ),
    project_file: Path = typer.Option("project.log", help="The project log file."),
) -> None:
    """
    Run the reporting logic for all structures provided. This will update the project.log
    file to include the results of a run as recorded by the .out file from a
    gaussian run.
    """
    project_df = load_project_file(project_file)
    with open(config_file, "r") as stream:
        config = yaml.safe_load(stream)
    for f in input_files:
        f = Path(f)
        try:
            data = GaussianTS(str(f), loglevel="CRITICAL").parse()
        except AttributeError:
            logging.error(
                (
                    "ERROR WITH GAUSSIAN OUTPUTFILE, DELETE .out + .gjf "
                    "FILES AND THE LINE IN THE LOGFILE"
                )
            )
            molecule, conf, iteration = f.stem.split("-")
            append_df = pd.DataFrame(
                [
                    [
                        molecule,
                        conf,
                        iteration,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        "error",
                    ]
                ],
                columns=STCOLUMNS,
                index=[max(0, project_df.index.max()) + 1],
            )
            append_df[STCOLUMNS].to_csv(project_file, mode="a", header=False)
            continue
        state = load_previous_state(f, project_file)
        stage = state["stage"]
        # in case this was the first iteration we need to replace
        # the name with what is in the config file
        if stage == "first-stage":
            stage = config["first-stage"]
        else:
            # otherwise the stage to be reported was the next stage
            stage = determine_next_stage(state, config_file)
        append_df = update_project_file(project_df, f, data, stage)
        # Only append an update if the update is not empty
        if len(append_df) > 0:
            append_df[STCOLUMNS].to_csv(project_file, mode="a", header=False)
