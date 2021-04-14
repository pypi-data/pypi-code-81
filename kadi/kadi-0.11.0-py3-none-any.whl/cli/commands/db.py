# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

import click
from flask import current_app
from flask_migrate import downgrade as downgrade_db
from flask_migrate import upgrade as upgrade_db

from kadi.cli.main import kadi
from kadi.cli.utils import check_env
from kadi.cli.utils import echo
from kadi.cli.utils import success
from kadi.cli.utils import warning
from kadi.ext.db import db as database
from kadi.lib.licenses.utils import update_licenses
from kadi.modules.accounts.providers import LocalProvider
from kadi.modules.collections.core import create_collection
from kadi.modules.groups.core import create_group
from kadi.modules.permissions.utils import setup_system_role
from kadi.modules.records.core import create_record


@kadi.group()
def db():
    """Utility commands for database management."""


def _update_licenses():
    try:
        update_licenses()
        return True
    except Exception as e:
        warning(f"Error updating licenses: {e}")

    return False


@db.command()
@click.argument("revision", default="head")
def upgrade(revision):
    """Upgrade the database schema to a specified revision.

    The default behaviour is to upgrade to the latest revision. Will also update the
    licenses stored in the database using the configured LICENSE_URL.
    """
    upgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision=revision)

    if _update_licenses():
        echo("Updated licenses.")

    database.session.commit()

    success("Upgrade completed successfully.")


@db.command()
@click.argument("revision", default="-1")
@click.option("--i-am-sure", is_flag=True)
@check_env
def downgrade(revision, i_am_sure):
    """Downgrade the database schema to a specified revision.

    The default behaviour is to downgrade a single revision.
    """
    if not i_am_sure:
        warning(
            "This can potentially erase some data of database"
            f" '{current_app.config['SQLALCHEMY_DATABASE_URI']}'. If you are sure you"
            " want to do this, use the flag --i-am-sure."
        )
        sys.exit(1)

    downgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision=revision)

    success("Downgrade completed successfully.")


def _initialize_db():
    echo("Initializing database...")

    for role_name in current_app.config["SYSTEM_ROLES"]:
        role = setup_system_role(role_name)

        if role is not None:
            echo(f"Initialized system role '{role_name}'.")

    if _update_licenses():
        echo("Initialized licenses.")

    database.session.commit()


@db.command()
def init():
    """Initialize the database."""
    upgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision="head")
    _initialize_db()

    success("Initialization completed successfully.")


@db.command()
@click.option("--i-am-sure", is_flag=True)
@check_env
def reset(i_am_sure):
    """Reset and reinitialize the database."""
    if not i_am_sure:
        warning(
            "This will erase all data of database"
            f" '{current_app.config['SQLALCHEMY_DATABASE_URI']}'. If you are sure you"
            " want to do this, use the flag --i-am-sure."
        )
        sys.exit(1)

    downgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision="base")
    upgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision="head")
    _initialize_db()

    success("Reset completed successfully.")


@db.command()
@click.option("--i-am-sure", is_flag=True)
@check_env
def test_data(i_am_sure):
    """Reset the database and setup sample data."""
    if not i_am_sure:
        warning(
            "This will erase all data of database"
            f" '{current_app.config['SQLALCHEMY_DATABASE_URI']}' and replace it with"
            " sample data. If you are sure you want to do this, use the flag"
            " --i-am-sure."
        )
        sys.exit(1)

    downgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision="base")
    upgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision="head")
    _initialize_db()

    # Set up an admin that can do anything.
    LocalProvider.register(
        username="admin",
        email="admin@example.com",
        displayname="Admin",
        password="admin123",
        system_role="admin",
    )

    # Setup a guest user with read-only access.
    LocalProvider.register(
        username="guest",
        email="guest@example.com",
        displayname="Guest",
        password="guest123",
        system_role="guest",
    )

    # Set up a normal user that can create new resources.
    member = LocalProvider.register(
        username="member",
        email="member@example.com",
        displayname="Member",
        password="member123",
        system_role="member",
    )
    user = member.user

    # Setup additional local sample users and resources, the latter belonging to the
    # "member" user.
    with click.progressbar(
        range(1, 31), label="Setting up sample data..."
    ) as progress_bar:
        for i in progress_bar:
            LocalProvider.register(
                username=f"user_{i}",
                email=f"user_{i}@example.com",
                displayname=f"User {i}",
                password="user1234",
            )

            create_record(
                creator=user,
                identifier=f"sample-record-{i}",
                title=f"Sample record {i}",
                type="sample",
                description="This is a sample record.",
                visibility="private" if i <= 15 else "public",
                extras=[
                    {"type": "str", "key": "sample 1", "value": "test"},
                    {"type": "float", "key": "sample 2", "value": 3.141, "unit": "cm"},
                ],
                tags=["sample tag", "sample record tag"],
            )

            create_collection(
                creator=user,
                identifier=f"sample-collection-{i}",
                title=f"Sample collection {i}",
                description="This is a sample collection.",
                visibility="private" if i <= 15 else "public",
                tags=["sample tag", "sample collection tag"],
            )

            create_group(
                creator=user,
                identifier=f"sample-group-{i}",
                title=f"Sample group {i}",
                description="This is a sample group.",
                visibility="private" if i <= 15 else "public",
            )

        database.session.commit()

    success("Setup completed successfully.")
