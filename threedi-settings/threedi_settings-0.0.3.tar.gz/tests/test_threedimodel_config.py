from pathlib import Path

from threedi_settings.threedimodel_config import ThreedimodelIni
from threedi_settings.threedimodel_config import AggregationIni

from tests.fixtures import model_ini, AGGRE


def tests_threedimodelini_as_dict(model_ini):
    ini_dict = model_ini.as_dict()
    # note: set of sections is not complete
    for x in {"meta", "physics", "physical_attributes", "grid_administration"}:
        assert x not in set(ini_dict.keys())


def tests_threedimodelini_as_dict_with_sections(model_ini):
    ini_dict = model_ini.as_dict(flat=False)
    # note: set of sections is not complete
    for x in {"meta", "physics", "physical_attributes", "grid_administration"}:
        assert x in set(ini_dict.keys())


def tests_aggregation_as_dict():
    model_aggre = AggregationIni(AGGRE)
    ini_dict = model_aggre.as_dict()
    assert len(ini_dict.keys()) == 10

