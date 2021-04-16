__version__ = "0.4b1"

import tensorflow as tf
import os
import numpy as np
import time
import pickle
from tensorflow.python.framework import tensor_util
from tensorflow.core.framework import tensor_pb2
import sys
from .label import Label
import threading
from rs4 import pathtool
import shutil
from .predutil import get_latest_version

glock = threading.RLock ()
tfsess = {}
added_models = {}
MODEL_BASE_DIR = None

def preference (path = None):
    import skitai
    pref =  skitai.preference (path = path)
    pref.config.tf_models = {}
    return pref

# multiple models management ----------------------------------------
def load_models ():
    global added_models
    loaded = []
    for alias, (model_dir, config) in added_models.items ():
        load_model (alias, model_dir, config)
        loaded.append ((alias, model_dir))
    return loaded

def close_models ():
    global tfsess
    with glock:
        for sess in tfsess.values ():
            sess.close ()
        tfsess = {}


# model management ----------------------------------------
def models ():
    with glock:
        return list (tfsess.keys ())

def load_model (alias, model_dir, config = None):
    # tf2 saved model
    from . import service_models
    global tfsess

    config = config or {}
    meta_models = []
    if isinstance (model_dir, str):
        if not os.path.isdir (model_dir):
            return
        model = service_models.load (model_dir, **config)
    else:
        model = model_dir # Model instance
        model.meta = True
        meta_models.append (model)

    with glock:
        tfsess [alias] = model

    for model in meta_models:
        model.create ()

def add_model (alias, model_dir, **config):
    # for lazy loading
    global added_models
    with glock:
        added_models [alias] = (model_dir, config)

def get_model (alias):
    with glock:
        return tfsess.get (alias)

def close_model (alias):
    global tfsess
    with glock:
        if alias not in tfsess:
            return
        tfsess [alias].close ()
        del tfsess [alias]

def delete_model (alias):
    model = get_model (alias)
    close_model (alias)
    model.remove_all_resources ()

def refresh_model (alias):
    model = get_model (alias)
    config = model.config
    if 'version' in config:
        config.pop ('version')
    close_model (alias)
    load_model (alias, model.model_root, config)

# version management ----------------------------------------
def delete_versions (alias, versions):
    if isinstance (versions, int):
        versions = [versions]
    versions = sorted (map (int, versions))
    model = get_model (alias)
    need_refresh = False
    for version in versions:
        model.remove_version (version)
        if model.version == version:
            need_refresh = True
    need_refresh and refresh_model (alias)

def add_version (alias, version, asset_zfile, refresh = True, overwrite = False, config = None):
    model = get_model (alias)
    if model:
        model_dir = os.path.join (model.model_root, str (version))
        if not overwrite:
            assert not os.path.exists (model_dir)
        model.add_version (version, asset_zfile)
        refresh and refresh_model (alias)
        return

    root_root = os.path.join (get_model_base_directory (), alias)
    model_dir = os.path.join (root_root, str (version))
    pathtool.unzipdir (asset_zfile, model_dir)
    load_model (alias, root_root, config)

# utilities ----------------------------------------
def get_labels (alias):
    with glock:
        return tfsess [alias].labels

def get_model_base_directory ():
    global MODEL_BASE_DIR

    if MODEL_BASE_DIR:
        return MODEL_BASE_DIR

    dirs = {}
    for model_name in models ():
        m = get_model (model_name)
        root = os.path.dirname (m.model_root)
        try: dirs [root] += 1
        except KeyError: dirs [root] = 1
    MODEL_BASE_DIR = sorted (dirs.items (), key = lambda x: x [1]) [-1][0]
    return MODEL_BASE_DIR
