import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from dataclasses_json import dataclass_json

from metaphor.common.event_util import EventUtil
from metaphor.common.extractor import BaseExtractor, RunConfig
from metaphor.common.metadata_change_event import (
    AspectType,
    DataPlatform,
    Dataset,
    DatasetDocumentation,
    DatasetLogicalID,
    DatasetSchema,
    DatasetStatistics,
    DatasetUpstream,
    EntityType,
    FieldDocumentation,
    MetadataChangeEvent,
    Ownership,
    PersonID,
    PersonOwner,
    SchemaField,
    SchemaType,
    SQLSchema,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass_json
@dataclass
class DbtRunConfig(RunConfig):
    manifest: str
    catalog: str


class DbtExtractor(BaseExtractor):
    """DBT metadata extractor"""

    def __init__(self):
        self._manifest: Dict = {}
        self._catalog: Dict = {}
        self._metadata: Dict[str, Dataset] = {}

    async def extract(self, config: RunConfig) -> List[MetadataChangeEvent]:
        assert isinstance(config, DbtRunConfig)

        logger.info("Fetching metadata from DBT repo")

        try:
            f = open(config.manifest, "r")
            self._manifest = json.load(f)
        except Exception as e:
            logger.error("Read manifest json error: {}".format(e))
            return []

        try:
            f = open(config.catalog, "r")
            self._catalog = json.load(f)
        except Exception as e:
            logger.error("Read catalog json error: {}".format(e))

        platform = self._parse_manifest()
        if platform is None:
            raise ValueError("Invalid platform from manifest.json")

        self._parse_catalog(platform)

        logger.debug(
            json.dumps(
                [EventUtil.clean_nones(d.to_dict()) for d in self._metadata.values()]
            )
        )

        return [EventUtil.build_dataset_event(d) for d in self._metadata.values()]

    def _parse_manifest(self) -> Optional[str]:
        if not self._manifest:
            return None

        metadata = self._manifest["metadata"]
        nodes = self._manifest["nodes"]
        sources = self._manifest["sources"]

        platform = metadata["adapter_type"].upper()

        models = {k: v for (k, v) in nodes.items() if v["resource_type"] == "model"}
        tests = {k: v for (k, v) in nodes.items() if v["resource_type"] == "test"}
        datasets = {**models, **sources}

        for model in datasets.values():
            self._parse_model(model, platform, datasets)

        for test in tests.values():
            self._parse_test(test)

        return platform

    def _parse_model(
        self, model: Dict, platform: str, datasets: Dict[str, Dict]
    ) -> None:
        dataset = self._init_dataset(model, platform)

        if "compiled_sql" in model:
            self._init_schema(dataset)
            assert dataset.schema is not None
            dataset.schema.sql_schema = SQLSchema()
            dataset.schema.sql_schema.table_schema = model["compiled_sql"]

        if model["description"]:
            self._init_documentation(dataset)
            assert (
                dataset.documentation is not None
                and dataset.documentation.dataset_documentations is not None
            )
            dataset.documentation.dataset_documentations.append(model["description"])

        for col in model["columns"].values():
            field = self._init_field(dataset, col["name"])
            field.description = col["description"]
            field.native_type = col["data_type"]

            field_doc = self._init_field_doc(dataset, col["name"])
            field_doc.documentation = col["description"]

        if "depends_on" in model:
            dataset.upstream = DatasetUpstream()
            dataset.upstream.aspect_type = AspectType.DATASET_UPSTREAM
            dataset.upstream.source_code_url = model["original_file_path"]
            dataset.upstream.sources = [
                self._get_upstream(n, platform, datasets)
                for n in model["depends_on"]["nodes"]
            ]

    def _parse_test(self, test: Dict) -> None:
        test_meta = test["test_metadata"]
        model_arg = test_meta["kwargs"]["model"]
        model_name = re.findall("^{{ ref\\('([^'\" ]+)'\\) }}$", model_arg)[0]
        table = DbtExtractor._dataset_name(test["database"], test["schema"], model_name)
        column = test_meta["kwargs"]["column_name"]

        dataset = self._metadata[table.upper()]

        field_doc = self._init_field_doc(dataset, column)
        if not field_doc.tests:
            field_doc.tests = []
        field_doc.tests.append(test_meta["name"])

    def _parse_catalog(self, platform: str) -> None:
        if not self._catalog:
            return

        nodes = self._catalog["nodes"]
        sources = self._catalog["sources"]

        for model in {**nodes, **sources}.values():
            self._parse_catalog_model(model, platform)

    def _parse_catalog_model(self, model: Dict, platform: str):
        meta = model["metadata"]
        columns = model["columns"]
        stats = model["stats"]

        dataset = self._init_dataset(meta, platform)

        self._init_ownership(dataset)
        assert dataset.ownership is not None and dataset.ownership.people is not None
        dataset.ownership.people.append(self._build_owner(meta["owner"]))

        self._init_schema(dataset)
        self._init_documentation(dataset)

        for col in columns.values():
            column_name = col["name"].lower()

            field = self._init_field(dataset, column_name)
            field.description = col["comment"]
            field.native_type = col["type"]

            field_doc = self._init_field_doc(dataset, column_name)
            field_doc.documentation = col["comment"]

        if stats and stats["has_stats"]["value"]:
            dataset.statistics = DatasetStatistics()
            dataset.statistics.aspect_type = AspectType.DATASET_STATISTICS
            dataset.statistics.record_count = float(stats["row_count"]["value"])
            dataset.statistics.data_size = (
                float(stats["bytes"]["value"]) / 1048576  # convert bytes to MB
            )
            dataset.statistics.last_updated = datetime.strptime(
                stats["last_modified"]["value"], "%Y-%m-%d %H:%M%Z"
            )

    @staticmethod
    def _dataset_name(db: str, schema: str, table: str) -> str:
        return "{}.{}.{}".format(db, schema, table)

    @staticmethod
    def _get_dataset_name(metadata: Dict) -> str:
        return DbtExtractor._dataset_name(
            metadata["database"], metadata["schema"], metadata["name"]
        )

    @staticmethod
    def _build_entity(table_name: str, platform: str) -> Dataset:
        dataset = Dataset()
        dataset.entity_type = EntityType.DATASET
        dataset.logical_id = DatasetLogicalID()
        dataset.logical_id.platform = DataPlatform[platform]
        dataset.logical_id.name = table_name
        return dataset

    def _init_dataset(self, metadata: Dict, platform: str) -> Dataset:
        table = self._get_dataset_name(metadata)
        if table.upper() not in self._metadata:
            self._metadata[table.upper()] = self._build_entity(table, platform)
        return self._metadata[table.upper()]

    @staticmethod
    def _init_schema(dataset: Dataset) -> None:
        if not dataset.schema:
            dataset.schema = DatasetSchema()
            dataset.schema.aspect_type = AspectType.DATASET_SCHEMA
            dataset.schema.schema_type = SchemaType.SQL
            dataset.schema.fields = []

    @staticmethod
    def _init_field(dataset: Dataset, column: str) -> SchemaField:
        assert dataset.schema is not None and dataset.schema.fields is not None

        field = next((f for f in dataset.schema.fields if f.field_path == column), None)
        if not field:
            field = SchemaField()
            field.field_path = column
            dataset.schema.fields.append(field)
        return field

    @staticmethod
    def _init_ownership(dataset: Dataset) -> None:
        if not dataset.ownership:
            dataset.ownership = Ownership()
            dataset.ownership.aspect_type = AspectType.OWNERSHIP
            dataset.ownership.people = []
            dataset.ownership.groups = []

    @staticmethod
    def _build_owner(db_owner: str) -> PersonOwner:
        owner = PersonOwner()
        owner.person = PersonID(db_owner)
        owner.role = "DB_TABLE_OWNER"
        return owner

    @staticmethod
    def _init_documentation(dataset: Dataset) -> None:
        if not dataset.documentation:
            dataset.documentation = DatasetDocumentation()
            dataset.documentation.aspect_type = AspectType.DATASET_DOCUMENTATION
            dataset.documentation.dataset_documentations = []
            dataset.documentation.field_documentations = []

    @staticmethod
    def _init_field_doc(dataset: Dataset, column: str) -> FieldDocumentation:
        assert (
            dataset.documentation is not None
            and dataset.documentation.field_documentations is not None
        )

        doc = next(
            (
                d
                for d in dataset.documentation.field_documentations
                if d.field_path == column
            ),
            None,
        )
        if not doc:
            doc = FieldDocumentation()
            doc.field_path = column
            dataset.documentation.field_documentations.append(doc)
        return doc

    @staticmethod
    def _get_upstream(
        node: str, platform: str, datasets: Dict[str, Dict]
    ) -> DatasetLogicalID:
        dataset_id = DatasetLogicalID()
        dataset_id.platform = DataPlatform[platform]
        dataset_id.name = DbtExtractor._get_dataset_name(datasets[node])
        return dataset_id
