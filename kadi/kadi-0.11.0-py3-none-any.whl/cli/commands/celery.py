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
import click
from celery.bin.celery import CeleryCommand

from kadi.cli.main import kadi
from kadi.ext.celery import celery as _celery
from kadi.ext.db import db


# This wrapper command ensures that the correct celery application is used and that it
# gets initialized correctly (by creating the Flask application as normal). It also
# leads to an application context being pushed, which is needed for the pre- and
# post-run handlers, while the tasks themselves run in their own application context.
@kadi.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    }
)
@click.pass_context
def celery(ctx):
    """celery wrapper command."""

    # Test the database connection before actually starting celery, since it might be
    # needed for persisting task information. The engine needs to be disposed
    # afterwards, as otherwise it gets copied to each worker.
    db.engine.connect()
    db.engine.dispose()

    cmd = CeleryCommand(_celery)
    cmd.execute_from_commandline(["kadi celery"] + ctx.args)
