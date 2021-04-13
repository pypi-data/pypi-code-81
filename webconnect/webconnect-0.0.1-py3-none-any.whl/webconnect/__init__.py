"""
A simple tool to be able to publish web sites to RStudio Connect
"""

import os
import json
import tarfile
import tempfile
import requests as req

try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata

__version__ = metadata.version('webconnect')

def pub_rsconnect(local_dir, name, pretty_name, connect_server, api_key):
    """
    publish a static site to RStudio Connect.

      Parameters:
        local_dir (str): a path to a directory containing the site
        name (str): name of content on Connect - only alphanumeric and underscores
        pretty_name (str): display name of content
        connect_server (str): RStudio Connect server address e.g. https://connect.example.com/
        api_key (str): API key of a user on RStudio Connect

       Return:
         Url of content

    """

    # Create Manifest
    manifest = {
        "version": 1,
        "locale": "en_US",
        "platform": "3.5.1",
        "metadata": {
            "appmode": "static",
            "primary_rmd": None,
            "primary_html": "index.html",
            "content_category": "document",
            "has_parameters": False,
        },
        "packages": None,
        "files": None,
        "users": None,
    }
    with open(local_dir + "/manifest.json", "w") as manifest_conn:
        json.dump(manifest, manifest_conn)

    # Turn dir into tarfile
    website_tf = tempfile.NamedTemporaryFile()
    with tarfile.open(website_tf.name, "w:gz") as tar:
        tar.add(local_dir, arcname=os.path.basename(local_dir))

    auth = {"Authorization": "Key " + api_key}

    content = get_content(name, pretty_name, connect_server, auth)
    content_url = connect_server + "/__api__/v1/content/" + content["guid"]

    # Upload Bundle
    with open(website_tf.name, "rb") as tf_conn:
        bundle = req.post(content_url + "/bundles", headers=auth, data=tf_conn)
    bundle_id = bundle.json()["id"]

    # Deploy bundle
    _deploy = req.post(
        content_url + "/deploy", headers=auth, json={"bundle_id": bundle_id}
    )
    return {"dash_url": content["dashboard_url"], "content_url": content["content_url"]}


def get_content(name, pretty_name, connect_server, auth):
    """
    Intermediate function to get content from Connect
    """
    content = req.get(
        connect_server + "/__api__/v1/content", headers=auth, params={"name": name}
    ).json()
    if content:  # content item created already
        return content[0]
    data = {"access_type": "acl", "name": name, "title": pretty_name}
    content = req.post(
        connect_server + "/__api__/v1/content", headers=auth, json=data
    ).json()
    return content
