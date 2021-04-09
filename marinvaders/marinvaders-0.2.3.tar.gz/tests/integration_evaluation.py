""" This is a full integration test.

The runtime for this script is several hours as it loops over all
eco-regions and check if we receive data for that. As such, it tests
all API calls and functionalities.

"""
import sys
import logging
import logging.handlers
from pathlib import Path
import os


TESTPATH = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(TESTPATH, ".."))

import marinvaders  # noqa

if __name__ == "__main__":
    # Logging to console and file, with each run in a different file
    logpath = TESTPATH / "evaluation_logs"
    logpath.mkdir(exist_ok=True, parents=True)
    logfile = logpath / "integration_evaluation.log"
    ig_log = logging.getLogger(__name__)
    ig_log.setLevel(logging.INFO)

    _do_rollover = True if os.path.exists(logfile) else False
    loghandler_file = logging.handlers.RotatingFileHandler(
        filename=logfile, backupCount=50
    )
    if _do_rollover:
        loghandler_file.doRollover()

    loghandler_stream = logging.StreamHandler()
    log_format = logging.Formatter(
        fmt="%(asctime)s %(levelname)-4s %(filename)s - %(funcName)s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    loghandler_file.setFormatter(log_format)
    loghandler_stream.setFormatter(log_format)
    ig_log.addHandler(loghandler_file)
    ig_log.addHandler(loghandler_stream)

    ig_log.info("Start logging to {} and screen".format(logfile))

    df_er = marinvaders.marine_ecoregions()

    for run_nr, run_data in df_er.iterrows():
        try:
            ig_log.info(f"LOOP {run_nr}: {run_data.ECOREGION} - {run_data.ECO_CODE}")
            reg_data = marinvaders.MarineLife(eco_code=run_data.ECO_CODE)
            ig_log.info(f"Received species - total: {len(reg_data.all_species)}")
            ig_log.info(f"Received species - alien: {len(reg_data.aliens)}")
        except:  # noqa
            ig_log.exception(f"Exception for eco-code {run_data.ECO_CODE}:")

    ig_log.info("Finished integration test run")

    # removing the logging handlers for next interactive run
    ig_log.handlers = []
