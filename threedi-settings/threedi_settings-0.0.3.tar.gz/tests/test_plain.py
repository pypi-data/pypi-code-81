from threedi_settings.plain.output import SimulationConfigWriter
from threedi_settings.threedimodel_config import ThreedimodelIni
from threedi_settings.threedimodel_config import AggregationIni
from tests.fixtures import simulation_config, simulation_config_no_aggregation
from tests.fixtures import INI


def test_config_writer_to_init(simulation_config, tmp_path):
    ini = tmp_path / "test.ini"
    agg = tmp_path / "aggr.ini"
    sc = SimulationConfigWriter(simulation_config, ini, agg, INI)
    sc.to_ini()
    assert ini.exists() and ini.is_file()
    assert agg.exists() and agg.is_file()
    mi = ThreedimodelIni(ini)
    aggi = AggregationIni(agg)
    ini_dict = mi.as_dict(flat=False)
    # note: set of sections is not complete
    for x in {"meta", "physics", "physical_attributes", "grid_administration"}:
        assert x in set(ini_dict.keys())
    aggi_dict = aggi.as_dict()
    assert len(aggi_dict.keys()) == len(simulation_config.aggregation_config)


def test_config_writer_to_init_no_aggr(simulation_config_no_aggregation, tmp_path):
    ini = tmp_path / "test.ini"
    agg = tmp_path / "aggr.ini"
    sc = SimulationConfigWriter(simulation_config_no_aggregation, ini, agg, INI)
    sc.to_ini()
    assert not agg.exists() and not agg.is_file()


def test_config_writer_without_legacy_ini(simulation_config_no_aggregation, tmp_path):
    ini = tmp_path / "test.ini"
    agg = tmp_path / "aggr.ini"
    sc = SimulationConfigWriter(simulation_config_no_aggregation, ini, agg)
    sc.to_ini()
    assert ini.exists() and ini.is_file()
    mi = ThreedimodelIni(ini)
    ini_dict = mi.as_dict(flat=False)
    # note: set of sections is not complete
    for x in {"meta", "grid_administration", "controls", "external_forcings", "projected_coordinate_system"}:
        assert x not in set(ini_dict.keys())
