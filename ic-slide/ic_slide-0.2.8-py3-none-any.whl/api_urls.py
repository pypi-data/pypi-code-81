from .config import get_config, is_client_grant


def urljoin(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """
    return "/".join(map(lambda x: str(x).rstrip('/'), args))


def get_storage_index_files_api_url():
    host_url = get_config("STORAGEINDEX_URL")
    return urljoin(
        host_url, "api/file-entry/all-organization-files"
    )


def get_storage_index_request_permission_token_api_url():
    if is_client_grant():
        raise Exception(
            "We can not access storage index with client grant type.")
    host_url = get_config("STORAGEINDEX_URL")
    return urljoin(
        host_url, "api/entry/request-permission-token"
    )


def get_asset_file_entry_api_url():
    if is_client_grant():
        raise Exception(
            "We can not access asset service with client grant type.")
    host_url = get_config("ASSETSERVICE_URL")
    return urljoin(
        host_url, "api/asset-service/file-entry"
    )


def get_metadata_url():
    host_url = get_config("SLIDECLOUD_URL")
    return urljoin(host_url,
                   "api/app/slideClientOnly/slideMetadata")


def get_tile_url():
    host_url = get_config("SLIDECLOUD_URL")
    return urljoin(host_url,
                   "api/app/slideClientOnly/tileUrl")
