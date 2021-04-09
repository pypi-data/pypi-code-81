from pathlib import Path

import numpy as np
import pytest
from astropy.io import fits

from dkist_processing_common._util.graphql import CreateRecipeRunStatusResponse
from dkist_processing_common._util.graphql import InputDatasetResponse
from dkist_processing_common._util.graphql import ProcessingCandidateResponse
from dkist_processing_common._util.graphql import RecipeInstanceResponse
from dkist_processing_common._util.graphql import RecipeRunResponse
from dkist_processing_common._util.graphql import RecipeRunStatusResponse
from dkist_processing_common._util.scratch import WorkflowFileSystem


class FakeGQLClient:
    @staticmethod
    def execute_gql_query(**kwargs):
        query_base = kwargs["query_base"]

        if query_base == "recipeRunStatuses":
            return [RecipeRunStatusResponse(recipeRunStatusId=1)]
        if query_base == "recipeRuns":
            return [
                RecipeRunResponse(
                    recipeInstance=RecipeInstanceResponse(
                        processingCandidate=ProcessingCandidateResponse(
                            observingProgramExecutionId="abc", proposalId="123"
                        ),
                        inputDataset=InputDatasetResponse(
                            inputDatasetDocument='{"bucket": "bucket-name", "parameters": [{"parameterName": "", "parameterValues": [{"parameterValueId": 1, "parameterValue": "[[1,2,3],[4,5,6],[7,8,9]]", "parameterValueStartDate": "1/1/2000"}]}], "frames": ["objectKey1", "objectKey2", "objectKeyN"]}'
                        ),
                    )
                )
            ]

    @staticmethod
    def execute_gql_mutation(**kwargs):
        mutation_base = kwargs["mutation_base"]

        if mutation_base == "updateRecipeRun":
            return
        if mutation_base == "createRecipeRunStatus":
            return CreateRecipeRunStatusResponse(
                recipeRunStatus=RecipeRunStatusResponse(recipeRunStatusId=1)
            )


@pytest.fixture(scope="function")
def fits_filepaths_list(tmp_path, complete_common_header):
    number_of_files = 10
    filepaths = []
    for i in range(number_of_files):
        data_array = np.random.rand(10, 10)
        hdu = fits.PrimaryHDU(data_array, header=complete_common_header)
        hdul = fits.HDUList([hdu])
        filepath = tmp_path / f"ave_data_{i}.fits"
        hdul.writeto(filepath)
        filepaths.append(filepath)
    return filepaths


@pytest.fixture(scope="function")
def fits_filepaths_list_with_multiple_hdus(tmp_path):
    number_of_files = 10
    filepaths = []
    for i in range(number_of_files):
        data_array = np.random.rand(10, 10)
        hdu0 = fits.PrimaryHDU()
        hdu1 = fits.ImageHDU(data_array)
        hdul = fits.HDUList([hdu0, hdu1, hdu1])
        filepath = tmp_path / f"ave_data_{i}.fits"
        hdul.writeto(filepath)
        filepaths.append(filepath)
    return filepaths


@pytest.fixture(scope="function")
def fits_filepaths_no_data_arrays(tmp_path):
    number_of_files = 10
    filepaths = []
    for i in range(number_of_files):
        hdu = fits.PrimaryHDU()
        hdul = fits.HDUList([hdu])
        filepath = tmp_path / f"ave_data_{i}.fits"
        hdul.writeto(filepath)
        filepaths.append(filepath)
    return filepaths


def test_change_status_to_in_progress(support_task, mocker):
    """
    Given: a support task
    When: requesting that the status of its recipe run is changed
    Then: the recipe run status changes
    """
    mocker.patch("dkist_processing_common._util.graphql.graph_ql_client", new=FakeGQLClient)
    support_task.change_status_to_in_progress()


def test_change_status_to_completed_successfully(support_task, mocker):
    """
    Given: a support task
    When: requesting that the status of its recipe run is changed
    Then: the recipe run status changes
    """
    mocker.patch("dkist_processing_common._util.graphql.graph_ql_client", new=FakeGQLClient)
    support_task.change_status_to_completed_successfully()


def test_constants(base_ext_task):
    """
    Given: a base_ext task
    When: using its .constants attribute
    Then: the constants behaves like a dictionary
    """
    base_ext_task.constants["foo"] = "baz"
    assert base_ext_task.constants["foo"] == "baz"


def test_input_dataset(support_task, mocker):
    """
    Given: a support task
    When: requesting an input data set
    Then: the input data set is returned either from a db query or local storage
    """
    mocker.patch("dkist_processing_common.base.graph_ql_client", new=FakeGQLClient)
    r_all = support_task.input_dataset()
    r_section = support_task.input_dataset(section="parameters")
    assert r_all["bucket"] == "bucket-name"
    assert len(r_all["frames"]) == 3
    assert r_section[0]["parameterValues"][0]["parameterValueId"] == 1
    assert r_section[0]["parameterValues"][0]["parameterValue"] == "[[1,2,3],[4,5,6],[7,8,9]]"
    assert r_section[0]["parameterValues"][0]["parameterValueStartDate"] == "1/1/2000"


def test_get_proposal_id(support_task, mocker):
    """
    Given: a support task
    When: the proposal id is requested
    Then: the proposal task is obtained via a db query and returned
    """
    mocker.patch("dkist_processing_common.base.graph_ql_client", new=FakeGQLClient)
    assert support_task.proposal_id == "123"


def test_frame_message(support_task):
    """
    Given: a support task
    When: a frame message is created
    Then: the components of the frame message are correctly populated
    """
    msg = support_task.create_frame_message(object_filepath="/test/object/path.ext")
    assert msg.objectName == "/test/object/path.ext"
    assert msg.conversationId == str(support_task.recipe_run_id)
    assert msg.bucket == "data"
    assert msg.incrementDatasetCatalogReceiptCount


def test_movie_message(support_task):
    """
    Given: a support task
    When: a movie message is created
    Then: the components of the movie message are correctly populated
    """
    msg = support_task.create_movie_message(object_filepath="/test/object/path.ext")
    assert msg.objectName == "/test/object/path.ext"
    assert msg.conversationId == str(support_task.recipe_run_id)
    assert msg.bucket == "data"
    assert msg.objectType == "MOVIE"
    assert msg.groupName == "DATASET"
    assert msg.incrementDatasetCatalogReceiptCount


def test_write_intermediate_fits(science_task, intermediate_fits, tmp_path):
    """
    Given: a fits file
    When: writing the file
    Then: the file exists
    """
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_intermediate_fits(
        data=intermediate_fits, datatype="TEST_WRITE", tags=["INT1", "INT2"]
    )
    assert Path(science_task._scratch.workflow_base_path, "TEST_WRITE.fits").exists()


def test_write_intermediate_fits_custom_filename(science_task, intermediate_fits, tmp_path):
    """
    Given: a fits file
    When: writing the file with a custom filename
    Then: the file exists
    """
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_intermediate_fits(
        data=intermediate_fits,
        datatype="TEST_WRITE",
        tags=["INT1", "INT2"],
        filename="custom_filename.fits",
    )
    assert not Path(science_task._scratch.workflow_base_path, "TEST_WRITE.fits").exists()
    assert Path(science_task._scratch.workflow_base_path, "custom_filename.fits").exists()


def test_write_output_fits(science_task, output_fits, tmp_path):
    """
    Given: a fits file
    When: writing the file
    Then: the file exists
    """
    relative_path = "test_output.fits"
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_output_fits(
        data=output_fits, relative_path=relative_path, tags=["OUTPUT1", "OUTPUT2"]
    )
    assert Path(science_task._scratch.workflow_base_path, relative_path).exists()


# @pytest.mark.parametrize(
#     "mod_state",
#     [
#         pytest.param(1, id="Modstate 1"),
#         pytest.param(2, id="Modstate 2"),
#         pytest.param(3, id="Modstate 3"),
#         pytest.param(4, id="Modstate 4"),
#         pytest.param(5, id="Modstate 5"),
#     ],
# )
# def test_group_by_modulator(science_task_with_modulated_inputs, mod_state):
#     """
#     Given: a dataset with some number of modulator states
#     When: grouping files of multiple tags by modulator state number
#     Then: each path gets assigned to the correct modulator state number and all states are checked
#     """
#     mod_dict = science_task_with_modulated_inputs.group_by_modulator_state(["GAIN"])
#     assert sorted(list(mod_dict.keys())) == [1, 2, 3, 4, 5]
#     assert len(list(mod_dict[mod_state])) == 1
#
#
# @pytest.mark.parametrize(
#     "mod_state",
#     [
#         pytest.param(1, id="Modstate 1"),
#         pytest.param(2, id="Modstate 2"),
#         pytest.param(3, id="Modstate 3"),
#         pytest.param(4, id="Modstate 4"),
#         pytest.param(5, id="Modstate 5"),
#     ],
# )
# def test_group_by_modulator_partial_tag(science_task, tmp_path, mod_state):
#     """
#     Given: a dataset with some number of modulator states
#     When: grouping files with with an insufficient tag set
#     Then: files that don't meet all tags are not grouped
#     """
#     science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
#     science_task.num_modulator_states = 5
#     for i in range(1, 5 + 1):
#         hdu = fits.PrimaryHDU()
#         hdul = fits.HDUList([hdu])
#         science_task._scratch.write_fits(
#             hdul, f"DATA_{i}.fits", tags=["TAG1", "TAG2", f"MODSTATE {i}"]
#         )
#         science_task._scratch.write_fits(hdul, f"DATA_BAD_{i}.fits", tags=["TAG2", f"MODSTATE {i}"])
#         science_task._scratch.write_fits(
#             hdul, f"DATA_BADDER_{i}.fits", tags=["TAG3", f"MODSTATE {i}"]
#         )
#
#     mod_dict = science_task.group_by_modulator_state(["TAG1", "TAG2"])
#     assert sorted(list(mod_dict.keys())) == [1, 2, 3, 4, 5]
#     assert len(list(mod_dict[mod_state])) == 1
#
#
# def test_group_by_modulator_no_num_modulator_states(science_task, tmp_path):
#     """
#     Given: a ScienceTaskL0ToL1 object that hasn't had its .num_modulator_states attribute set
#     When: trying to group any files by modulator state
#     Then: raise and error
#     """
#     science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
#     for i in range(2):
#         hdu = fits.PrimaryHDU()
#         hdul = fits.HDUList([hdu])
#         science_task._scratch.write_fits(
#             hdul, f"DATA_{i}.fits", tags=["TAG1", "TAG2", f"MODSTATE {i}"]
#         )
#
#     with pytest.raises(RuntimeError):
#         mod_dict = science_task.group_by_modulator_state(["TAG1", "TAG2"])


def test_read_intermediate_fits(science_task, intermediate_fits, tmp_path):
    """
    Given: a type of file
    When: reading that file
    Then: the file is read correctly and the contents can be examined
    """
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_intermediate_fits(data=intermediate_fits, datatype="TEST_READ")
    hdul = fits.open(science_task.read_intermediate_fits(datatype="TEST_READ"))
    assert hdul[0].header["DKIST004"] == "TEST_INTERMEDIATE"


@pytest.mark.parametrize(
    "tags",
    [
        pytest.param(["INPUT", "DARK"], id="DARK"),
        pytest.param(["INPUT", "GAIN"], id="GAIN"),
        pytest.param(["INPUT", "TARGET"], id="TARGET"),
        pytest.param(["INPUT", "INSTPOLCAL"], id="INSTPOLCAL"),
        pytest.param(["INPUT", "TELPOLCAL"], id="TELPOLCAL"),
        pytest.param(["INPUT", "GEOMETRIC"], id="GEOMETRIC"),
    ],
)
def test_read_fits(science_task_with_inputs, tags):
    """
    Given: a type of file
    When: reading that file
    Then: the file is read correctly and the contents can be examined
    """
    frames = science_task_with_inputs.read_fits(tags=tags)
    frame = next(frames)
    f = fits.open(frame)
    assert f[0].header["DKIST004"] == tags[1]


def test_input_dark_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_dark_frames
    frame = next(frames)
    f = fits.open(frame)
    assert f[0].header["DKIST004"] == "DARK"


def test_input_lamp_gain_frames(science_task_with_modulated_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_modulated_inputs.input_lamp_gain_frames(modstate=1)
    frame = next(frames)
    f = fits.open(frame)
    assert f[0].header["DKIST004"] == "LAMP GAIN"


def test_input_target_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_target_frames
    frame = next(frames)
    f = fits.open(frame)
    assert f[0].header["DKIST004"] == "TARGET"


def test_input_instpolcal_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_instpolcal_frames
    frame = next(frames)
    f = fits.open(frame)
    assert f[0].header["DKIST004"] == "INSTPOLCAL"


def test_input_telpolcal_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_telpolcal_frames
    frame = next(frames)
    f = fits.open(frame)
    assert f[0].header["DKIST004"] == "TELPOLCAL"


def test_input_geometric_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_geometric_frames
    frame = next(frames)
    f = fits.open(frame)
    assert f[0].header["DKIST004"] == "GEOMETRIC"


def test_intermediate_dark(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "DARK"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_dark(data=hdul)
    f = fits.open(science_task.intermediate_dark)
    assert f[0].header["datatype"] == datatype


def test_intermediate_dark_too_many_darks(science_task, tmp_path):
    """
    Given: A ScienceTaskL0ToL1 object with more than 1 intermediate Dark frame
    When: Trying to get the single intermediate dark frame
    Then: An error is raised
    """
    for i in range(2):
        hdu = fits.PrimaryHDU()
        hdu.header["DKIST004"] = "DARK"
        hdul = fits.HDUList([hdu])
        science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
        science_task._scratch.write_fits(hdul, f"DARK_{i}.fits", tags=["INTERMEDIATE", "DARK"])

    with pytest.raises(RuntimeError):
        _ = science_task.intermediate_dark


def test_intermediate_gain(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "GAIN"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_gain(data=hdul)
    f = fits.open(science_task.intermediate_gain())
    assert f[0].header["datatype"] == datatype


@pytest.mark.parametrize(
    "modulation_state",
    [
        pytest.param(1, id="Modulation state 1"),
        pytest.param(2, id="Modulation state 2"),
        pytest.param(3, id="Modulation state 3"),
        pytest.param(4, id="Modulation state 4"),
        pytest.param(5, id="Modulation state 5"),
    ],
)
def test_intermediate_gain_with_modstate(science_task, tmp_path, modulation_state):
    """
    Given: a specific type of input with an associated modulation state
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "GAIN"
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    for modstate in range(1, 6):
        hdu = fits.PrimaryHDU()
        hdu.header["datatype"] = datatype
        hdu.header["modstate"] = modstate
        hdul = fits.HDUList([hdu])
        science_task.write_gain(data=hdul, modstate=modstate)
    f = fits.open(science_task.intermediate_gain(modstate=modulation_state))
    assert f[0].header["datatype"] == datatype
    assert f[0].header["modstate"] == modulation_state


def test_intermediate_target(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "TARGET"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_target(data=hdul)
    f = fits.open(science_task.intermediate_target)
    assert f[0].header["datatype"] == datatype


def test_intermediate_instpolcal(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "INSTPOLCAL"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_instpolcal(data=hdul)
    f = fits.open(science_task.intermediate_instpolcal)
    assert f[0].header["datatype"] == datatype


def test_intermediate_telpolcal(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "TELPOLCAL"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_telpolcal(data=hdul)
    f = fits.open(science_task.intermediate_telpolcal)
    assert f[0].header["datatype"] == datatype


def test_intermediate_geometric(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "GEOMETRIC"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_geometric(data=hdul)
    f = fits.open(science_task.intermediate_geometric)
    assert f[0].header["datatype"] == datatype


def test_input_dir(science_task, tmp_path):
    science_task._scratch = WorkflowFileSystem(
        scratch_base_path=tmp_path, recipe_run_id=science_task.recipe_run_id
    )
    assert science_task.input_dir == tmp_path / str(science_task.recipe_run_id) / "input"


def test_output_dir(science_task, tmp_path):
    science_task._scratch = WorkflowFileSystem(
        scratch_base_path=tmp_path, recipe_run_id=science_task.recipe_run_id
    )
    assert science_task.output_dir == tmp_path / str(science_task.recipe_run_id) / "output"


def test_globus_path(science_task, tmp_path):
    """
    Given: An instance of WorkflowFileSystem
    When: call globus path method
    Then: Retrieve path to recipe run id
    """
    science_task._scratch = WorkflowFileSystem(
        scratch_base_path=tmp_path, recipe_run_id=science_task.recipe_run_id
    )
    assert science_task.globus_path() == Path(f"{science_task.recipe_run_id}/")
    assert science_task.globus_path(science_task._scratch.workflow_base_path, "foo.txt") == Path(
        f"{science_task.recipe_run_id}/foo.txt"
    )


def test_output_paths(support_task_with_outputs):
    """
    Given: an instance of a support task that has output files associated with it
    When: the list of output paths is inspected
    Then: the correct number of output paths are found
    """
    assert len(support_task_with_outputs.output_paths) == 10


def test_fits_to_numpy(science_task, fits_filepaths_list):
    """
    Given: an iterable of fits filepaths
    When: converting them to numpy arrays
    Then: the numpy arrays contained within the referenced fits files are exposed
    through a generator
    """
    filepaths = fits_filepaths_list
    data_arrays = science_task.fits_to_numpy(filepaths)
    for i in range(len(filepaths)):
        data_array = next(data_arrays)
        assert isinstance(data_array, np.ndarray)
        assert np.amax(data_array) <= 1
        assert np.amin(data_array) >= 0


def test_fits_to_numpy_multiple_arrays_in_files(
    science_task, fits_filepaths_list_with_multiple_hdus
):
    """
    Given: an iterable of fits filepaths with multiple data arrays in the hdus
    When: converting them to numpy arrays
    Then: an error is generated
    """
    filepaths = fits_filepaths_list_with_multiple_hdus
    data_arrays = science_task.fits_to_numpy(filepaths)
    with pytest.raises(ValueError):
        next(data_arrays)


def test_fits_to_numpy_no_data(science_task, fits_filepaths_no_data_arrays):
    """
    Given: an iterable of fits filepaths that have no data in their data arrays
    When: converting them to numpy arrays
    Then: an error is raised as there is no numpy element to return
    """
    with pytest.raises(ValueError):
        filepaths = fits_filepaths_no_data_arrays
        data_arrays = science_task.fits_to_numpy(filepaths)
        for i in range(len(filepaths)):
            next(data_arrays)
