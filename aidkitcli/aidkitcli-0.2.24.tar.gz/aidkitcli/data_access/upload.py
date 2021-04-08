"""Upload and list stored models and data sets."""
from aidkitcli.data_access.api import RESTApi


def upload_model(model_path: str):
    """Upload a stored model."""
    api = RESTApi()
    return api.post_model(
        model_path=model_path
    )


def list_models():
    """List all the uploaded models."""
    api = RESTApi()
    return api.list_model()


def upload_data(zip_path: str):
    """Upload a data set."""
    api = RESTApi()
    return api.post_data(
        zip_path=zip_path
    )


def list_data():
    """List all the uploaded data sets."""
    api = RESTApi()
    return api.list_data()
