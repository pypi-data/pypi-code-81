from typing import Tuple

import numpy as np
import pytest
from astropy.io import fits
from dkist_data_simulator.spec122 import Spec122Dataset

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.common import ParseInputData


class VispHeaders(Spec122Dataset):
    def __init__(
        self,
        dataset_shape: Tuple[int, ...],
        array_shape: Tuple[int, ...],
        time_delta: float,
        instrument="visp",
    ):
        super().__init__(dataset_shape, array_shape, time_delta, instrument=instrument)
        self.add_constant_key("WAVELNTH")
        self.add_constant_key("TELSCAN")
        self.add_constant_key("CAM__001")
        self.add_constant_key("CAM__002")
        self.add_constant_key("CAM__003")
        self.add_constant_key("CAM__004")
        self.add_constant_key("CAM__005")
        self.add_constant_key("CAM__006")
        self.add_constant_key("CAM__007")
        self.add_constant_key("CAM__008")
        self.add_constant_key("CAM__009")
        self.add_constant_key("CAM__010")
        self.add_constant_key("CAM__011")
        self.add_constant_key("CAM__012")
        self.add_constant_key("CAM__013")
        self.add_constant_key("CAM__014")
        self.add_constant_key("CAM__015")
        self.add_constant_key("CAM__016")
        self.add_constant_key("CAM__017")
        self.add_constant_key("CAM__018")
        self.add_constant_key("CAM__019")
        self.add_constant_key("CAM__020")
        self.add_constant_key("CAM__021")
        self.add_constant_key("CAM__022")
        self.add_constant_key("CAM__023")
        self.add_constant_key("CAM__024")
        self.add_constant_key("CAM__025")
        self.add_constant_key("CAM__026")
        self.add_constant_key("CAM__027")
        self.add_constant_key("CAM__028")
        self.add_constant_key("CAM__029")
        self.add_constant_key("CAM__030")
        self.add_constant_key("CAM__031")
        self.add_constant_key("CAM__032")
        self.add_constant_key("PAC__002")
        self.add_constant_key("PAC__004")
        self.add_constant_key("PAC__006")
        self.add_constant_key("PAC__008")
        self.add_constant_key("VISP_002")
        self.add_constant_key("VISP_007")
        self.add_constant_key("VISP_014", 8)
        self.add_constant_key("VISP_016")
        self.add_constant_key("VISP_019")


@pytest.fixture(scope="function")
def parse_inputs_task(tmp_path):
    class TaskClass(ParseInputData):
        def run(self):
            pass

    task = TaskClass(
        recipe_run_id=1, workflow_name="parse_visp_input_data", workflow_version="VX.Y"
    )
    task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    ds = VispHeaders(dataset_shape=(10, 512, 512), array_shape=(1, 512, 512), time_delta=10)
    header_generator = (d.header() for d in ds)
    for i in range(10):
        hdu = fits.PrimaryHDU(data=np.zeros(shape=(1, 10, 10)))
        generated_header = next(header_generator)
        for key, value in generated_header.items():
            hdu.header[key] = value
        hdul = fits.HDUList([hdu])
        task._scratch.write_fits(data=hdul, relative_path=f"input/input_{i}.fits")
    yield task
    task._scratch.purge()
    task.constants.purge()


@pytest.fixture(scope="function")
def parse_inputs_prepopulated_constants(parse_inputs_task):
    constants = ["INSTRUME", "VISP_014"]
    parse_inputs_task.add_constants(constants=constants)
    for i in range(10):
        hdul = fits.open(parse_inputs_task.input_dir / f"input_{i}.fits")
        parse_inputs_task.get_constants_from_header(header=hdul[0].header)

    yield parse_inputs_task


def test_add_constants(parse_inputs_task):
    """
    Given: An instance of a ParseInputData task
    When: adding names of constants to pipeline_constants
    Then: the named constants are in the pipeline_constants dict
    """
    constants = ["a", "b"]
    parse_inputs_task.add_constants(constants=constants)
    assert parse_inputs_task.pipeline_constants["a"] == set()
    assert parse_inputs_task.pipeline_constants["b"] == set()


def test_get_constants_from_header(parse_inputs_task):
    """
    Given: An instance of a ParseInputData task
    When: getting constant values out of a fits header
    Then: the values are populated in the pipeline_constants dict
    """
    constants = ["INSTRUME", "VISP_014"]
    parse_inputs_task.add_constants(constants=constants)
    hdul = fits.open(parse_inputs_task.input_dir / "input_0.fits")
    parse_inputs_task.get_constants_from_header(header=hdul[0].header)
    assert parse_inputs_task.pipeline_constants["INSTRUME"] == {"VISP"}
    assert parse_inputs_task.pipeline_constants["VISP_014"] == {8}


def test_verify_and_record_constants(parse_inputs_prepopulated_constants):
    """
    Given: An instance of a ParseInputData task with the pipeline_constants dict prepopulated
    When: verifying and recording constants
    Then: the constant values can be retrieves from the task's constants object
    """
    parse_inputs_prepopulated_constants.verify_and_record_constants()
    assert parse_inputs_prepopulated_constants.constants["INSTRUME"] == "VISP"
    assert parse_inputs_prepopulated_constants.constants["VISP_014"] == 8


def test_verify_and_record_constants_missing_value(parse_inputs_prepopulated_constants):
    """
    Given: An instance of a ParseInputData task with the pipeline_constants dict prepopulated
    When: verifying and recording constants where a key has no value
    Then: an error is raised
    """
    parse_inputs_prepopulated_constants.pipeline_constants["MISSING_VALUE"] = set()
    with pytest.raises(ValueError):
        parse_inputs_prepopulated_constants.verify_and_record_constants()


def test_verify_and_record_constants_value_not_constant(parse_inputs_prepopulated_constants):
    """
    Given: An instance of a ParseInputData task with the pipeline_constants dict prepopulated
    When: verifying and recording constants where a key a value that is not constant
    Then: an error is raised
    """
    parse_inputs_prepopulated_constants.pipeline_constants["NOT_CONSTANT"] = {1, 2, 3}
    with pytest.raises(ValueError):
        parse_inputs_prepopulated_constants.verify_and_record_constants()
