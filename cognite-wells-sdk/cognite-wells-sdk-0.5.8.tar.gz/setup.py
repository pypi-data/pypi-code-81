# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cognite',
 'cognite.well_model',
 'cognite.well_model.client',
 'cognite.well_model.client.api',
 'cognite.well_model.client.models',
 'cognite.well_model.client.utils']

package_data = \
{'': ['*']}

install_requires = \
['cognite-logger>=0.5.0,<0.6.0',
 'helpers>=0.2.0,<0.3.0',
 'nulltype>=2.3.1,<3.0.0',
 'numpy>=1.18.1,<2.0.0',
 'oauthlib>=3.1.0,<4.0.0',
 'pandas>=1.0.1,<2.0.0',
 'pydantic>=1.8,<2.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'requests>=2.21.0,<3.0.0']

setup_kwargs = {
    'name': 'cognite-wells-sdk',
    'version': '0.5.8',
    'description': '',
    'long_description': '# Installation with pip\n\n```bash\npip install cognite-wells-sdk\n```\n\n# Usage\n\n## Authenticating and creating a client\n\n### With environment variables\n\n**NOTE**: *must be valid for both cdf and geospatial API*\n\n```bash\nexport COGNITE_PROJECT=<project-tenant>\nexport COGNITE_API_KEY=<your-api-key>\n```\n\nYou can then initialize the client with\n```py\nfrom cognite.well_model import CogniteWellsClient\nwells_client = CogniteWellsClient()\n```\n\n### Without environment variables\n\nAlternatively, the client can be initialized like this:\n\n```python\nimport os\nfrom cognite.well_model import CogniteWellsClient\napi_key = os.environ["COGNITE_API_KEY"]\nwells_client = CogniteWellsClient(project="your-project", api_key=api_key)\n```\n\n### Connect to a different CDF environment\n\n```py\nfrom cognite.well_model import CogniteWellsClient, Cluster\nwells_client = CogniteWellsClient(cluster = Cluster.BP)\n```\n\n\n## **Well queries**\n\n### Get well by id\n\n```python\nwell = wells_client.wells.get_by_id(8456650753594878)\n```\n\n### List wells\n\n```python\nwells = wells_client.wells.list()\n```\n\n#### Filter wells by wkt polygon\n\n```python\nfrom cognite.well_model.models import PolygonFilter\n\npolygon = \'POLYGON ((0.0 0.0, 0.0 80.0, 80.0 80.0, 80.0 0.0, 0.0 0.0))\'\nwells = wells_client.wells.filter(polygon=PolygonFilter(geometry=polygon, crs="epsg:4326"))\n```\n\n#### Filter wells by wkt polygon, name/description and specify desired outputCrs\n\n```python\npolygon = \'POLYGON ((0.0 0.0, 0.0 80.0, 80.0 80.0, 80.0 0.0, 0.0 0.0))\'\nwells = wells_client.wells.filter(\n    polygon=PolygonFilter(geometry=polygon, crs="epsg:4326", geometry_type="WKT"),\n    string_matching="16/",\n    output_crs="EPSG:23031"\n)\n```\n\n### Get wells that have a trajectory\n\n```python\nfrom cognite.well_model.models import TrajectoryFilter\n\nwells = wells_client.wells.filter(has_trajectory=TrajectoryFilter(), limit=None)\n```\n\n### Get wells that have a trajectory with data between certain depths\n\n```python\nwells = wells_client.wells.filter(has_trajectory=TrajectoryFilter(min_depth=1400.0, max_depth=1500.0), limit=None)\n```\n\n### Get wells that has the right set of measurement types\n\n```python\nfrom cognite.well_model.models import MeasurementFilter, MeasurementFilters, MeasurementType\n\ngammarayFilter = MeasurementFilter(measurement_type=MeasurementType.gamma_ray)\ndensityFilter = MeasurementFilter(measurement_type=MeasurementType.density)\n\n# Get wells with all measurements\nmeasurements_filter = MeasurementFilters(contains_all=[gammarayFilter, densityFilter])\nwells = wells_client.wells.filter(has_measurements=measurements_filter, limit=None)\n\n# Or get wells with any of the measurements\nmeasurements_filter = MeasurementFilters(contains_any=[gammarayFilter, densityFilter])\nwells = wells_client.wells.filter(has_measurements=measurements_filter, limit=None)\n```\n\n### Get wellbores for a well id\n\n```python\nwellbores = wells_client.wellbores.get_from_well(well.id)\n```\n\nor\n\n```python\nwell = wells_client.wells.get_by_id(519497487848)\nwellbores = well.wellbores()\n```\n\n### Get wellbores from multiple well ids\n\n```python\nwellbores = wells_client.wellbores.get_from_wells([17257290836510, 8990585729991697])\n```\n\n### Filter - list all labels\n\n```python\nblocks = wells_client.wells.blocks()\nfields = wells_client.wells.fields()\noperators = wells_client.wells.operators()\nquadrants = wells_client.wells.quadrants()\nsources = wells_client.wells.sources()\nmeasurementTypes = wells_client.wells.measurements()\n```\n\n## Wellbore queries\n\n### Get wellbore by id\n\n```jupyterpython\nwellbore = wells_client.wellbores.get_by_id(2360682364100853)\n```\n\n### Get wellbore measurement for measurementType: \'GammaRay\'\n\n```python\nmeasurements = wells_client.wellbores.get_measurement(wellbore_id=2360682364100853, measurement_type=MeasurementType.gamma_ray)\n```\n\n### Get trajectory for a wellbore\n\n```python\nwellbore = wells_client.wellbores.get_by_id(2360682364100853)\ntrajectory = wellbore.trajectory()\n```\n\nOr get it directly from a wellbore id\n\n```python\ntrajectory = wells_client.surveys.get_trajectory(2360682364100853)\n```\n\n## Survey queries\n\n### Get data from a survey, from start and end rows\n\n```python\ntrajectory_data = wells_client.surveys.get_data(17257290836510, start=0, end=100000, columns=["MD", "AZIMUTH"])\n```\n\n### Get all data from a survey object\n```python\ntrajectory = wells_client.surveys.get_trajectory(2360682364100853)\ntrajectory_data = trajectory.data()\n```\n\n## Ingestion\n\n### Initialise tenant\n\nBefore ingesting any wells, the tenant must be initialized to add in the standard assets and labels used in the WDL.\n\n```python\nfrom cognite.well_model import CogniteWellsClient\n\nwells_client = CogniteWellsClient()\nlog_output = wells_client.ingestion.ingestion_init()\nprint(log_output)  # If something is wrong with authorization, you should see that in the logs\n```\n\n### Add source\n\nBefore ingestion from a source can take place, the source must be registered in WDL.\n\n```python\nimport os\nfrom cognite.well_model import CogniteWellsClient\n\nwells_client = CogniteWellsClient()\ncreated_sources = wells_client.sources.ingest_sources(["Source1, Source2"])\n```\n\n### Ingest wells\n```python\nimport os\nfrom datetime import date\n\nfrom cognite.well_model import CogniteWellsClient\nfrom cognite.well_model.models import DoubleWithUnit, WellDatum, Wellhead, WellIngestion\n\nwells_client = CogniteWellsClient()\nsource_asset_id = 102948135620745 # Id of the well source asset in cdf\n\nwell_to_create = WellIngestion(\n    asset_id=source_asset_id,\n    well_name="well-name",\n    description="Optional description for the well",\n    country="Norway",\n    quadrant="25",\n    block="25/5",\n    field="Example",\n    operator="Operator1",\n    spud_date=date(2021, 3, 17),\n    water_depth=0.0,\n    water_depth_unit="meters",\n    wellhead=Wellhead(\n        x = 21.0,\n        y = 42.0,\n        crs = "EPSG:4236" # Must be a EPSG code\n    ),\n    datum=WellDatum(\n        elevation = DoubleWithUnit(value=1.0, unit="meters"),\n        reference = "well-datum-reference",\n        name = "well-datum-name"\n    ),\n    source="Source System Name"\n)\n\nwells_client.ingestion.ingest_wells([well_to_create]) # Can add multiple WellIngestion objects at once\n```\n\n### Ingest wellbores with optional well and/or trajectory\n```python\nimport os\n\nfrom cognite.well_model import CogniteWellsClient\nfrom cognite.well_model.models import (\n    DoubleArrayWithUnit,\n    TrajectoryIngestion,    \n    WellIngestion,\n    WellboreIngestion,\n    ParentType,\n    MeasurementIngestion,\n    MeasurementField,\n    MeasurementType\n)\n\nwells_client = CogniteWellsClient()\nsource_asset_id = 102948135620745 # Id of the wellbore source asset in cdf\nsource_trajectory_ext_id = "some sequence ext id" # Id of the source sequence in cdf\n\nwell_to_create = WellIngestion(...)\ntrajectory_to_create = TrajectoryIngestion(\n    source_sequence_ext_id=source_trajectory_ext_id,\n    measured_depths = DoubleArrayWithUnit(values=[0.0, 1.0, 2.0], unit="meters"),\n    inclinations = DoubleArrayWithUnit(values=[10.0, 1.0, 22.0], unit="degrees"),\n    azimuths = DoubleArrayWithUnit(values=[80.0, 81.0, 82.0], unit="degrees")\n)\nmeasurements_to_create = [\n    MeasurementIngestion(\n        sequence_external_id="measurement_sequence_1",\n        measurement_fields=[\n            MeasurementField(type_name=MeasurementType.gamma_ray),\n            MeasurementField(type_name=MeasurementType.density),\n        ],\n    ),\n    MeasurementIngestion(\n        sequence_external_id="measurement_sequence_2",\n        measurement_fields=[\n            MeasurementField(type_name=MeasurementType.geomechanics),\n            MeasurementField(type_name=MeasurementType.lot),\n        ],\n    )   \n]\n\nwellbore_to_create = WellboreIngestion(\n    asset_id = source_asset_id,\n    wellbore_name = "wellbore name",\n    parent_name = "name of parent well or wellbore",\n    parent_type = ParentType.well, # or ParentType.wellbore\n    well_name = "name of parent well", # top level well; required in addition to the parent name (even if parent is well)\n    source = "Source System Name",\n    trajectory_ingestion = trajectory_to_create,\n    measurement_ingestions = measurements_to_create,\n    well_ingestion = well_to_create # if not ingesting a well, then one must already exist\n)\n\nwells_client.ingestion.ingest_wellbores([wellbore_to_create]) # Can add multiple WellboreIngestion objects at once\n```\n\n### Ingest casing data\n```python\nimport os\n\nfrom cognite.well_model import CogniteWellsClient\nfrom cognite.well_model.models import DoubleArrayWithUnit, CasingIngestion\n\nwells_client = CogniteWellsClient()\nsource_casing_id = 102948135620745 # Id of the casing source sequence in cdf\n\n\ncasing_to_ingest = CasingIngestion(\n    source_casing_id = source_casing_id,\n    wellbore_name = "wellbore name",\n    casing_name = "Surface Casing",\n    body_inside_diameter = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="mm"),\n    body_outside_diameter = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="mm"),\n    md_top = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="m"),\n    md_base = DoubleArrayWithUnit(values=[120.0, 150.0, 190.0], unit="m"),\n    tvd_top = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="m"), # TVD measurements are optional\n    tvd_base = DoubleArrayWithUnit(values=[120.0, 150.0, 190.0], unit="m") # TVD measurements are optional\n)\n\nwells_client.ingestion.ingest_casings([casing_to_ingest]) # Can add multiple CasingIngestion objects at once\n```\n',
    'author': 'Dylan Phelps',
    'author_email': 'dylan.phelps@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
