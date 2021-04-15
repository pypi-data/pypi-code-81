from os import path
import shutil
import os
import numpy as np

import autolens as al


def test__point_source_dataset_structures_as_dict():

    point_source_dataset_0 = al.PointSourceDataset(
        name="source_1",
        positions=al.Grid2DIrregular([[1.0, 1.0]]),
        positions_noise_map=al.ValuesIrregular([1.0]),
    )

    point_source_dict = al.PointSourceDict(
        point_source_dataset_list=[point_source_dataset_0]
    )

    assert point_source_dict["source_1"].name == "source_1"
    assert point_source_dict["source_1"].positions.in_list == [(1.0, 1.0)]
    assert point_source_dict["source_1"].positions_noise_map.in_list == [1.0]
    assert point_source_dict["source_1"].fluxes == None
    assert point_source_dict["source_1"].fluxes_noise_map == None

    point_source_dataset_1 = al.PointSourceDataset(
        name="source_2",
        positions=al.Grid2DIrregular([[1.0, 1.0]]),
        positions_noise_map=al.ValuesIrregular([1.0]),
        fluxes=al.ValuesIrregular([2.0, 3.0]),
        fluxes_noise_map=al.ValuesIrregular([4.0, 5.0]),
    )

    point_source_dict = al.PointSourceDict(
        point_source_dataset_list=[point_source_dataset_0, point_source_dataset_1]
    )

    assert point_source_dict["source_1"].name == "source_1"
    assert point_source_dict["source_1"].positions.in_list == [(1.0, 1.0)]
    assert point_source_dict["source_1"].positions_noise_map.in_list == [1.0]
    assert point_source_dict["source_1"].fluxes == None
    assert point_source_dict["source_1"].fluxes_noise_map == None

    assert point_source_dict["source_2"].name == "source_2"
    assert point_source_dict["source_2"].positions.in_list == [(1.0, 1.0)]
    assert point_source_dict["source_2"].positions_noise_map.in_list == [1.0]
    assert point_source_dict["source_2"].fluxes.in_list == [2.0, 3.0]
    assert point_source_dict["source_2"].fluxes_noise_map.in_list == [4.0, 5.0]

    assert (point_source_dict.positions_list[0] == np.array([1.0, 1.0])).all()
    assert (point_source_dict.positions_list[1] == np.array([1.0, 1.0])).all()


def test__from_json_and_output_to_json():

    point_source_dataset_0 = al.PointSourceDataset(
        name="source_1",
        positions=al.Grid2DIrregular([[1.0, 1.0]]),
        positions_noise_map=al.ValuesIrregular([1.0]),
    )

    point_source_dataset_1 = al.PointSourceDataset(
        name="source_2",
        positions=al.Grid2DIrregular([[1.0, 1.0]]),
        positions_noise_map=al.ValuesIrregular([1.0]),
        fluxes=al.ValuesIrregular([2.0, 3.0]),
        fluxes_noise_map=al.ValuesIrregular([4.0, 5.0]),
    )

    point_source_dict = al.PointSourceDict(
        point_source_dataset_list=[point_source_dataset_0, point_source_dataset_1]
    )

    dir_path = path.join("{}".format(path.dirname(path.realpath(__file__))), "files")

    if path.exists(dir_path):
        shutil.rmtree(dir_path)

    os.makedirs(dir_path)

    file_path = path.join(dir_path, "point_source_dict.json")

    point_source_dict.output_to_json(file_path=file_path, overwrite=True)

    point_source_dict_via_json = al.PointSourceDict.from_json(file_path=file_path)

    assert point_source_dict_via_json["source_1"].name == "source_1"
    assert point_source_dict_via_json["source_1"].positions.in_list == [(1.0, 1.0)]
    assert point_source_dict_via_json["source_1"].positions_noise_map.in_list == [1.0]
    assert point_source_dict_via_json["source_1"].fluxes == None
    assert point_source_dict_via_json["source_1"].fluxes_noise_map == None

    assert point_source_dict_via_json["source_2"].name == "source_2"
    assert point_source_dict_via_json["source_2"].positions.in_list == [(1.0, 1.0)]
    assert point_source_dict_via_json["source_2"].positions_noise_map.in_list == [1.0]
    assert point_source_dict_via_json["source_2"].fluxes.in_list == [2.0, 3.0]
    assert point_source_dict_via_json["source_2"].fluxes_noise_map.in_list == [4.0, 5.0]
