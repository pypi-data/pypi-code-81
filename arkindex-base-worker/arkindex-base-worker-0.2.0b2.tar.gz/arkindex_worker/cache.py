# -*- coding: utf-8 -*-
import json
import os
import sqlite3

from peewee import (
    BooleanField,
    CharField,
    Field,
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
    UUIDField,
)

from arkindex_worker import logger
from arkindex_worker.image import open_image, polygon_bounding_box

db = SqliteDatabase(None)


class JSONField(Field):
    field_type = "text"

    def db_value(self, value):
        if value is None:
            return
        return json.dumps(value)

    def python_value(self, value):
        if value is None:
            return
        return json.loads(value)


class CachedImage(Model):
    id = UUIDField(primary_key=True)
    width = IntegerField()
    height = IntegerField()
    url = TextField()

    class Meta:
        database = db
        table_name = "images"


class CachedElement(Model):
    id = UUIDField(primary_key=True)
    parent_id = UUIDField(null=True)
    type = CharField(max_length=50)
    image = ForeignKeyField(CachedImage, backref="elements", null=True)
    polygon = JSONField(null=True)
    initial = BooleanField(default=False)
    worker_version_id = UUIDField(null=True)

    class Meta:
        database = db
        table_name = "elements"

    def open_image(self, *args, max_size=None, **kwargs):
        """
        Open this element's image as a Pillow image.
        This does not crop the image to the element's polygon.
        IIIF servers with maxWidth, maxHeight or maxArea restrictions on image size are not supported.

        :param max_size: Subresolution of the image.
        """
        if not self.image_id or not self.polygon:
            raise ValueError(f"Element {self.id} has no image")
        if max_size is None:
            resize = "full"
        else:
            bounding_box = polygon_bounding_box(self.polygon)
            # Do not resize for polygons that do not exactly match the images
            if (
                bounding_box.width != self.image.width
                or bounding_box.height != self.image.height
            ):
                resize = "full"
                logger.warning(
                    "Only full size elements covered, downloading full size image"
                )
            # Do not resize when the image is below the maximum size
            elif self.image.width <= max_size and self.image.height <= max_size:
                resize = "full"
            else:
                ratio = max_size / max(self.image.width, self.image.height)
                new_width, new_height = int(self.image.width * ratio), int(
                    self.image.height * ratio
                )
                resize = f"{new_width},{new_height}"

        url = self.image.url
        if not url.endswith("/"):
            url += "/"

        return open_image(f"{url}full/{resize}/0/default.jpg", *args, **kwargs)


class CachedTranscription(Model):
    id = UUIDField(primary_key=True)
    element = ForeignKeyField(CachedElement, backref="transcriptions")
    text = TextField()
    confidence = FloatField()
    worker_version_id = UUIDField()

    class Meta:
        database = db
        table_name = "transcriptions"


# Add all the managed models in that list
# It's used here, but also in unit tests
MODELS = [CachedImage, CachedElement, CachedTranscription]


def init_cache_db(path):
    db.init(
        path,
        pragmas={
            # SQLite ignores foreign keys and check constraints by default!
            "foreign_keys": 1,
            "ignore_check_constraints": 0,
        },
    )
    db.connect()
    logger.info(f"Connected to cache on {path}")


def create_tables():
    """
    Creates the tables in the cache DB only if they do not already exist.
    """
    db.create_tables(MODELS)


def merge_parents_cache(parent_ids, current_database, data_dir="/data", chunk=None):
    """
    Merge all the potential parent task's databases into the existing local one
    """
    assert isinstance(parent_ids, list)
    assert os.path.isdir(data_dir)
    assert os.path.exists(current_database)

    # Handle possible chunk in parent task name
    # This is needed to support the init_elements databases
    filenames = [
        "db.sqlite",
    ]
    if chunk is not None:
        filenames.append(f"db_{chunk}.sqlite")

    # Find all the paths for these databases
    paths = list(
        filter(
            lambda p: os.path.isfile(p),
            [
                os.path.join(data_dir, parent, name)
                for parent in parent_ids
                for name in filenames
            ],
        )
    )

    if not paths:
        logger.info("No parents cache to use")
        return

    # Open a connection on current database
    connection = sqlite3.connect(current_database)
    cursor = connection.cursor()

    # Merge each table into the local database
    for idx, path in enumerate(paths):
        logger.info(f"Merging parent db {path} into {current_database}")
        statements = [
            "PRAGMA page_size=80000;",
            "PRAGMA synchronous=OFF;",
            f"ATTACH DATABASE '{path}' AS source_{idx};",
            f"REPLACE INTO elements SELECT * FROM source_{idx}.elements;",
            f"REPLACE INTO transcriptions SELECT * FROM source_{idx}.transcriptions;",
        ]

        for statement in statements:
            cursor.execute(statement)
        connection.commit()
