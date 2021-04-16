import tensorflow as tf
import os
from rs4 import importer
from rs4 import pathtool
from rs4 import attrdict
import numpy as np
import shutil
import gc
from .. import datasets
from ..predutil import get_latest_version, get_next_version
import requests
import pickle

class Model:
    meta = False

    def __init__ (self):
        self._model = None
        self.asset_path = None

    def create (self):
        # for meta model
        # automatically called by tfserver app
        raise NotImplementedError

    def save (self, path, model, ds, save_testset = True, assets = None, custom_objects = None):
        pathtool.mkdir (path)
        version = get_next_version (path)
        model_path = os.path.join (path, str (version))
        model.save (model_path)
        self.asset_path = os.path.join (model_path, 'assets')
        ds.save (self.asset_path, save_testset, assets)

        if custom_objects:
            import dill
            custom_objects_ = {}
            for k, v in custom_objects.items ():
                if '.<locals>.' in str (v):
                    custom_objects_ [k] = (1, dill.dumps (v))
                else:
                    custom_objects_ [k] = (0, v)
            self.write_asset ('custom-objects', custom_objects)

    def add_asset (self, filename):
        shutil.copy (filename, self.asset_path)

    def write_asset (self, filename, obj):
        with open (os.path.join (self.asset_path, filename), 'wb') as f:
            f.write (pickle.dumps (obj))

    def read_asset (self, filename):
        if not self.asset_path:
            return None
        asset = os.path.join (self.asset_path, filename)
        if not os.path.isfile (asset):
            return None
        with open (asset, 'rb') as f:
            return pickle.loads (f.read ())

    def load_custom_objects (self):
        custom_objects_ = self.read_asset ('custom-objects')
        if custom_objects_ is None:
            return None

        custom_objects = {}
        for k, (flag, v) in custom_objects_.items ():
            if flag  == 0:
                custom_objects [k] = v
            else:
                import dill
                custom_objects [k] = dill.loads (v)
        return custom_objects

    def load (self, path, **config):
        version = config.get ('version')
        testset = config.get ('testset')
        custom_objects = self.load_custom_objects ()

        self.config = config
        self.version = version or get_latest_version (path)
        self.model_root = path
        self.name = os.path.basename (self.model_root)

        self.model_dir = os.path.join (self.model_root, str (self.version))
        self.asset_path = os.path.join (self.model_dir, 'assets')
        self._model = tf.keras.models.load_model (self.model_dir, compile = False, custom_objects = custom_objects)

        self.ds = datasets.load (self.asset_path, testset)
        self.labels = self.ds.labels
        self.input_names = [self.get_tensor_name (each) for each in self._model.inputs]
        self.output_names = [self.get_tensor_name (each) for each in self._model.outputs]

    def get_tensor_name (self, t):
        n = t.name.split (":") [0].split ('/', 1) [0]
        parts = n.split ('_')
        if parts [-1].isdigit ():
            return '_'.join (parts [:-1])
        return n

    def get_latest_version (self):
        return get_latest_version (self.model_root)

    def get_next_version (self):
        return get_next_version (self.model_root)

    def remove_all_resources (self):
        shutil.rmtree (self.model_root)

    def remove_version (self, version):
        deletable = os.path.join (self.model_root, str (version))
        if not os.path.isdir (deletable):
            return
        shutil.rmtree (deletable)

    def add_version (self, version, asset_zfile):
        target = os.path.join (self.model_root, str (version))
        pathtool.unzipdir (asset_zfile, target)

    def get_version (self):
        return self.version

    def deploy (self, url, **data):
        while url:
            if url.endswith ('/'):
                url = url [:-1]
            else:
                break
        url = '{}/versions/{}'.format (url, self.version)
        model_dir = os.path.join (self.model_root, str (self.version))
        with pathtool.flashfile ('model.zip') as zfile:
            pathtool.zipdir ('model.zip', model_dir)
            resp = pathtool.uploadzip (url, 'model.zip', **data)
        assert resp.status_code == 201, 'upload failed'
        resp = requests.get ('/'.join (url.split ("/")[:-2]))
        return resp.json ()

    def close (self):
        self._model = None
        gc.collect()
        tf.keras.backend.clear_session ()

    def make (self, *args, **karg):
        raise NotImplementedError

    def normalize (self, xs):
        return self.ds.normalizer.transform (xs)

    def preprocess (self, input, *args, **karg):
        raise NotImplementedError

    def summary (self):
        self._model.summary ()

    def _reduce (self, reducer, preds):
        if isinstance (reducer, str):
            reducer = getattr (np, reducer)
        return tuple ([ reducer (pred, 0, keepdims = True) for pred in preds ])

    def _to_dict (self, preds):
        d = attrdict.AttrDict (
            { output: preds [i] for i, output in enumerate (self.output_names) }
        )
        for i, name in enumerate (self.output_names):
            v = d [name]
            classes, scores = [], []
            topks = np.flip (np.argsort (v, 1) [:,-16:], 1)
            for idx, topk in enumerate (topks):
                classes.append ([ self.labels [i].class_name (arg) for arg in topk ])
                scores.append ([ v [idx][arg] for arg in topk ])
            d ['{}_classes'.format (name)] = classes
            d ['{}_scores'.format (name)] = np.array (scores)
        return d

    def predict (self, xs, normalize = True, as_dict = False, reducer = None):
        if isinstance (xs, dict):
            xs_ = [ xs [name] for name in self.input_names ]
            xs = xs_ [0] if len (xs) == 1 else np.array (xs_)

        if normalize and self.ds.normalizer:
            xs = self.normalize (xs)

        preds = self._model.predict (xs)
        if len (self.output_names) == 1:
            preds = (preds,)

        if reducer:
            preds = self._reduce (reducer, preds)

        if as_dict:
            return self._to_dict (preds)

        return preds if len (self.output_names) > 1 else preds [0]

    def _reduce_with (self, xs, normalize = True, as_dict = False, reducer = 'mean'):
        return self.predict (xs, normalize, as_dict, reducer)

    def reduce_mean (self, xs, normalize = True, as_dict = False):
        return self._reduce_with (xs, normalize, as_dict, np.mean)

    def reduce_max (self, xs, normalize = True, as_dict = False):
        return self._reduce_with (xs, normalize, as_dict, np.max)

    def reduce_min (self, xs, normalize = True, as_dict = False):
        return self._reduce_with (xs, normalize, as_dict, np.min)


def get_latest_version (path):
    versions = [ int (v) for v in os.listdir (path) if v.isdigit () ]
    if not versions:
        raise ValueError ('cannot find any model')
    return sorted (versions) [-1]

def get_next_version (path):
    try:
        return get_latest_version (path) + 1
    except ValueError:
        return 1

def load (model_path, **config):
    if config.get ('version') is None:
        config ['version'] = get_latest_version (model_path)

    class_file = os.path.join (model_path, str (config ['version']), 'assets', 'service_model.py')
    if not os.path.isfile (class_file):
        model = Model ()
        model.load (model_path, **config)
        return model

    service_model = importer.from_file (
        "service_models.{}".format (os.path.basename (model_path).replace ('-', '_')),
        class_file
    )
    return service_model.load (model_path, **config)
