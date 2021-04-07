# -*- coding: utf-8 -*-
import os
from uuid import UUID

import pytest
from peewee import OperationalError

from arkindex_worker.cache import (
    CachedElement,
    CachedImage,
    create_tables,
    db,
    init_cache_db,
)


def test_init_non_existent_path():
    with pytest.raises(OperationalError) as e:
        init_cache_db("path/not/found.sqlite")

    assert str(e.value) == "unable to open database file"


def test_init(tmp_path):
    db_path = f"{tmp_path}/db.sqlite"
    init_cache_db(db_path)

    assert os.path.isfile(db_path)


def test_create_tables_existing_table(tmp_path):
    db_path = f"{tmp_path}/db.sqlite"

    # Create the tables once…
    init_cache_db(db_path)
    create_tables()
    db.close()

    with open(db_path, "rb") as before_file:
        before = before_file.read()

    # Create them again
    init_cache_db(db_path)
    create_tables()

    with open(db_path, "rb") as after_file:
        after = after_file.read()

    assert before == after, "Existing table structure was modified"


def test_create_tables(tmp_path):
    db_path = f"{tmp_path}/db.sqlite"
    init_cache_db(db_path)
    create_tables()

    expected_schema = """CREATE TABLE "elements" ("id" TEXT NOT NULL PRIMARY KEY, "parent_id" TEXT, "type" VARCHAR(50) NOT NULL, "image_id" TEXT, "polygon" text, "initial" INTEGER NOT NULL, "worker_version_id" TEXT, FOREIGN KEY ("image_id") REFERENCES "images" ("id"))
CREATE TABLE "images" ("id" TEXT NOT NULL PRIMARY KEY, "width" INTEGER NOT NULL, "height" INTEGER NOT NULL, "url" TEXT NOT NULL)
CREATE TABLE "transcriptions" ("id" TEXT NOT NULL PRIMARY KEY, "element_id" TEXT NOT NULL, "text" TEXT NOT NULL, "confidence" REAL NOT NULL, "worker_version_id" TEXT NOT NULL, FOREIGN KEY ("element_id") REFERENCES "elements" ("id"))"""

    actual_schema = "\n".join(
        [
            row[0]
            for row in db.connection()
            .execute("SELECT sql FROM sqlite_master WHERE type = 'table' ORDER BY name")
            .fetchall()
        ]
    )

    assert expected_schema == actual_schema


@pytest.mark.parametrize(
    "image_width,image_height,polygon_width,polygon_height,max_size,expected_url",
    [
        # No max_size: no resize
        (400, 600, 400, 600, None, "http://something/full/full/0/default.jpg"),
        # max_size equal to the image size, no resize
        (400, 600, 400, 600, 600, "http://something/full/full/0/default.jpg"),
        (600, 400, 600, 400, 600, "http://something/full/full/0/default.jpg"),
        (400, 400, 400, 400, 400, "http://something/full/full/0/default.jpg"),
        # max_size is smaller than the image, resize
        (400, 600, 400, 600, 400, "http://something/full/266,400/0/default.jpg"),
        (400, 600, 200, 600, 400, "http://something/full/266,400/0/default.jpg"),
        (600, 400, 600, 400, 400, "http://something/full/400,266/0/default.jpg"),
        (400, 400, 400, 400, 200, "http://something/full/200,200/0/default.jpg"),
        # max_size above the image size, no resize
        (400, 600, 400, 600, 800, "http://something/full/full/0/default.jpg"),
        (600, 400, 600, 400, 800, "http://something/full/full/0/default.jpg"),
        (400, 400, 400, 400, 800, "http://something/full/full/0/default.jpg"),
    ],
)
def test_element_open_image(
    mocker,
    image_width,
    image_height,
    polygon_width,
    polygon_height,
    max_size,
    expected_url,
):
    open_mock = mocker.patch(
        "arkindex_worker.cache.open_image", return_value="an image!"
    )

    image = CachedImage(
        id=UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
        width=image_width,
        height=image_height,
        url="http://something",
    )
    elt = CachedElement(
        id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        type="element",
        image=image,
        polygon=[
            [0, 0],
            [image_width, 0],
            [image_width, image_height],
            [0, image_height],
            [0, 0],
        ],
    )

    assert elt.open_image(max_size=max_size) == "an image!"
    assert open_mock.call_count == 1
    assert open_mock.call_args == mocker.call(expected_url)


def test_element_open_image_requires_image():
    with pytest.raises(ValueError) as e:
        CachedElement(id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")).open_image()
    assert str(e.value) == "Element aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa has no image"
