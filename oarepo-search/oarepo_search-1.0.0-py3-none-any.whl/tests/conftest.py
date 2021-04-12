import shutil
import tempfile

import pytest
from flask import Flask
from invenio_search import InvenioSearch

from oarepo_search.ext import OARepoSearch


@pytest.yield_fixture()
def app():
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    # app.config.update(
    #     JSONSCHEMAS_HOST="nusl.cz",
    #     SQLALCHEMY_TRACK_MODIFICATIONS=True,
    #     SERVER_NAME='127.0.0.1:5000',
    #     INVENIO_INSTANCE_PATH=instance_path,
    #     DEBUG=True,
    #     # OAREPO_OAI_PROVIDERS={
    #     #     "uk": {
    #     #         "description": "Univerzita Karlova",
    #     #         "synchronizers": [
    #     #             {
    #     #                 "name": "xoai",
    #     #                 "oai_endpoint": "https://dspace.cuni.cz/oai/nusl",
    #     #                 "set": "nusl_set",
    #     #                 "metadata_prefix": "xoai",
    #     #                 "unhandled_paths": ["/dc/unhandled"],
    #     #                 "default_endpoint": "recid",
    #     #                 "from": "latest",
    #     #                 # "use_default_endpoint": True,
    #     #                 "endpoint_mapping": {
    #     #                     "field_name": "doc_type",
    #     #                     "mapping": {
    #     #                         "record": "recid"
    #     #                     }
    #     #                 }
    #     #             }
    #     #         ]
    #     #     },
    #     # },
    #     # RECORDS_REST_ENDPOINTS=RECORDS_REST_ENDPOINTS,
    #     # PIDSTORE_RECID_FIELD='pid'
    # )
    #
    # app.secret_key = 'changeme'
    #
    # InvenioDB(app)
    # # InvenioAccounts(app)
    # # InvenioAccess(app)
    # # Principal(app)
    # # InvenioJSONSchemas(app)
    InvenioSearch(app)
    OARepoSearch(app)
    # # InvenioIndexer(app)
    # # InvenioRecords(app)
    # # InvenioRecordsREST(app)
    # # InvenioPIDStore(app)
    # # app.url_map.converters['pid'] = PIDConverter
    # # app.register_blueprint(oai_client_blueprint, url_prefix="/oai-client")
    # # print("\n\nURL MAP", app.url_map)
    #
    # # app_loaded.send(app, app=app)
    #
    # # with app.app_context():
    # #     if current_search_client.indices.exists("test_index"):
    # #         current_search_client.indices.delete(index="test_index")
    # #     yield app
    yield app
    shutil.rmtree(instance_path)

# @pytest.fixture()
# def db(app):
#     """"Returns fresh db."""
#     with app.app_context():
#         if not database_exists(str(db_.engine.url)) and \
#                 app.config['SQLALCHEMY_DATABASE_URI'] != 'sqlite://':
#             create_database(db_.engine.url)
#         db_.create_all()
#
#     yield db_
#
#     # Explicitly close DB connection
#     db_.session.close()
#     db_.drop_all()
