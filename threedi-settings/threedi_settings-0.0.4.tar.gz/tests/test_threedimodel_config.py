import pytest

from threedi_settings.threedimodel_config import ThreedimodelSqlite, RowDoesNotExistError
from threedi_settings.threedimodel_config import AggregationIni
from threedi_settings.mappings import settings_map

from tests.fixtures import model_ini, AGGRE
from tests.sqlite_fixture import model_sqlite



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


def test_threedimodelsqlite_as_dict(model_sqlite):
    tms = ThreedimodelSqlite(model_sqlite, 1)
    tms_set = set(tms.as_dict().keys())
    map_set = set()
    for item in settings_map.values():
        _, _, sqlite_info = item
        map_set.add(sqlite_info.name)
    tms_set.discard("numerical_settings_id")
    assert tms_set == map_set


def test_threedimodelsqlite_aggregations(model_sqlite):
    tms = ThreedimodelSqlite(model_sqlite, 1)
    assert isinstance(tms.aggregation_settings, dict)
    assert len(tms.aggregation_settings.keys()) == 10


def test_threedimodelsqlite_wrong_row(model_sqlite):
    tms = ThreedimodelSqlite(model_sqlite, 100)
    with pytest.raises(RowDoesNotExistError):
        assert tms.global_settings

    with pytest.raises(RowDoesNotExistError):
        assert tms.numerical_settings

    with pytest.raises(RowDoesNotExistError):
        assert tms.as_dict()
