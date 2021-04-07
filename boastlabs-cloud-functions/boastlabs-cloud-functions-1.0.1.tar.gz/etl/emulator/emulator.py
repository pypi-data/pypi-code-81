import os
import mock
import google.auth.credentials
from google.cloud import firestore

from etl.execution.process import Process


if os.getenv('GAE_ENV', '').startswith('standard'):
    # production
    db = firestore.Client()
else:
    # localhost
    os.environ["FIRESTORE_DATASET"] = "test"
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8888"
    os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8888/firestore"
    os.environ["FIRESTORE_HOST"] = "http://localhost:8888"
    os.environ["FIRESTORE_PROJECT_ID"] = "boast-firebase"

    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    db = firestore.Client(project="boast-firebase", credentials=credentials)


def setup(tenant, user, fiscal_year):
    db.document(f'tenants/{tenant}').set({'debug': True})
    db.document(f'tenants/{tenant}/integrations/Github').set({'debug': True})

    db.document(f'tenants/{tenant}/integrations/Github/users/{user["name"]}').set(user)

    for config in user['configs']:
        db.document(f'tenants/{tenant}/integrations/Github/users/{user["name"]}/configs/{config["id"]}').set(config)

    db.document(f'tenants/{tenant}/integrations/Github/fiscal_years/{fiscal_year["name"]}').set(fiscal_year)
    db.document(f'tenants/{tenant}/integrations/Github/fiscal_years/{fiscal_year["name"]}/etl_jobs/1').set({
        'debug': True
    })

    ingest_path = f'tenants/{tenant}/integrations/Github/fiscal_years/{fiscal_year["name"]}/etl_jobs/1/jobs/ingest'
    db.document(ingest_path).set({
        'active': True,
        'status': 'new'
    })
    return ingest_path


if __name__ == '__main__':

    tenant = 'test'
    user = {
        'name': 'debug',
        'access_token': '14d4640066826957891dd3ce521ea3699742c4fd',
        'configs': [{
            'id': 1,
            'default_branch': 'master',
            'full_name': 'BoastCapitalLP/abi',
            'read_from': True
        }]
    }
    fiscal_year = {
        'name': 'debug FYE',
        'start_date': '2021-01-01',
        'end_date': '2021-12-31'
    }

    path = setup(tenant=tenant, user=user, fiscal_year=fiscal_year)

    Process(db=db, doc_path=path).run()
