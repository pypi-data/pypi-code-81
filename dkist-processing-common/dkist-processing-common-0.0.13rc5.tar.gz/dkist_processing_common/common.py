import logging
from abc import ABC
from os import environ
from pathlib import Path
from typing import List

from astropy.io import fits
from dkist_header_validator import spec122_validator

from dkist_processing_common._util.globus import submit_globus_transfer
from dkist_processing_common._util.graphql import DatasetCatalogReceiptAccountMutation
from dkist_processing_common._util.graphql import graph_ql_client
from dkist_processing_common._util.message import publish_messages
from dkist_processing_common.base import SupportTaskBase


class TransferInputData(SupportTaskBase):
    """
    Changes the status of the recipe run to "INPROGRESS"
    Starts a globus transfer of all data listed in the associated input dataset to scratch
    """

    def run(self) -> None:
        self.change_status_to_in_progress()

        bucket = self.input_dataset(section="bucket")
        frames = self.input_dataset(section="frames")

        source_files = [Path("/", bucket, frame) for frame in frames]

        submit_globus_transfer(
            source_files=source_files,
            destination_files=[
                self.globus_path(self.input_dir, source_file.name) for source_file in source_files
            ],
            source_endpoint=environ.get("OBJECT_STORE_ENDPOINT"),
            destination_endpoint=environ.get("SCRATCH_ENDPOINT"),
        )


class ParseInputData(SupportTaskBase, ABC):
    def __init__(self, recipe_run_id: int, workflow_name: str, workflow_version: str):
        super().__init__(recipe_run_id, workflow_name, workflow_version)
        self.pipeline_constants = {}

    def add_constants(self, constants: List[str]) -> None:
        """
        Add a new collection of constants to the pipeline constants dict for
        insertion to the constants mutable mapping
        Parameters
        ----------
        constants: the list of constants to be recorded

        Returns
        -------
        None
        """
        for constant in constants:
            self.pipeline_constants[constant] = set()

    def get_constants_from_header(self, header: fits.header.Header) -> None:
        """
        Add values from constant header keywords to the pipeline_constants dict
        Parameters
        ----------
        header: spec 214 fits header to remove values from

        Returns
        -------
        None
        """
        for key in self.pipeline_constants:
            self.pipeline_constants[key].add(header[key])

    def verify_and_record_constants(self):
        """
        Make sure that a given constant truly was constant across a collection of data and if so,
        records its value.
        Returns
        -------
        None
        """
        for key, value in self.pipeline_constants.items():
            if len(value) == 0:
                raise ValueError(f"No values were found for constant {key}.")
            elif len(value) > 1:
                raise ValueError(f"Constant {key} was found to change: {len(value)} values found.")
            # Value found to be constant, so record it in the constants object
            self.constants[key] = list(value).pop()

    @staticmethod
    def translate_fits_file(filepath: Path) -> fits.HDUList:
        """
        Perform the spec 122 to spec 214 translation on fits files
        Parameters
        ----------
        filepath: path of the fits file to translate header for

        Returns
        -------
        the translated HDUList in spec 214 format
        """
        return spec122_validator.validate_and_translate(fits.open(filepath))


class TransferOutputData(SupportTaskBase):
    """
    Transfers all data tagged as "OUTPUT" to the object store
    """

    def run(self) -> None:
        globus_output_paths = [self.globus_path(path) for path in self.output_paths]
        logging.info(f"{globus_output_paths=}")
        destination_files = [
            Path("/data", self.proposal_id, self.dataset_id, source_file.name)
            for source_file in globus_output_paths
        ]
        logging.info(f"{destination_files=}")

        submit_globus_transfer(
            source_files=globus_output_paths,
            destination_files=destination_files,
            source_endpoint=environ["SCRATCH_ENDPOINT"],
            destination_endpoint=environ["OBJECT_STORE_ENDPOINT"],
        )


class AddDatasetReceiptAccount(SupportTaskBase):
    """
    Creates a Dataset Catalog Receipt Account record populated with the number of objects
    """

    def run(self) -> None:
        expected_object_count = len(self.output_paths)
        graph_ql_client.execute_gql_mutation(
            mutation_base="createDatasetCatalogReceiptAccount",
            mutation_parameters=DatasetCatalogReceiptAccountMutation(
                datasetId=self.dataset_id, expectedObjectCount=expected_object_count
            ),
        )


class PublishCatalogMessages(SupportTaskBase):
    """
    Publishes a message for every object transferred to the object store
    """

    def run(self) -> None:
        object_filepaths = [
            str(Path(self.proposal_id, self.dataset_id, source_file.name))
            for source_file in self.output_paths
        ]
        logging.critical(f"{object_filepaths=}")
        messages = []
        for filepath in object_filepaths:
            if filepath.lower().endswith(".fits"):
                messages.append(self.create_frame_message(object_filepath=filepath))
            elif filepath.lower().endswith(".mp4"):
                messages.append(self.create_movie_message(object_filepath=filepath))
        logging.critical(f"{messages=}")
        publish_messages(messages=messages)


class Teardown(SupportTaskBase):
    """
    Changes the status of the recipe run to "COMPLETEDSUCCESSFULLY"
    Deletes the scratch directory containing all data from this pipeline run
    """

    def run(self) -> None:
        logging.info(f"Removing data and tags for recipe run {self.recipe_run_id}")
        self.change_status_to_completed_successfully()
        self.purge_file_system()
