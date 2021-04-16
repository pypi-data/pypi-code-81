from atila import Atila
import tensorflow as tf
import tfserver
from tfserver.pb2 import prediction_service_pb2, predict_pb2
from tensorflow.python.framework import tensor_util
import numpy as np
import os
from rs4.termcolor import tc

app = Atila (__name__)

@app.before_mount
def before_mount (wasc):
	import dnn
	dnn.setup_gpus (app.config.GPU_LIMIT, app.config.GPU_DEVICES) # this call must be in a child process
	for alias, model_dir in tfserver.load_models ():
		wasc.logger ("app", "- loading tensorflow model '{}' from {}".format (tc.cyan (alias), tc.white (model_dir)), 'info')

@app.umounted
def umounted (wasc):
	tfserver.close_models ()


# gRPC predict services ------------------------------------
@app.route ("/tensorflow.serving.PredictionService/Predict")
def Predict (was, request, timeout = 10):
	model = tfserver.get_model (request.model_spec.name)
	inputs = { k: tensor_util.MakeNdarray (v) for k, v in request.inputs.items () }

	result = getattr (model, request.model_spec.signature_name) (inputs, as_dict = True)
	response = predict_pb2.PredictResponse ()
	for k, v in result.items ():
		response.outputs [k].CopyFrom (tf.make_tensor_proto (v))
	return response

def serialize (result):
	resp = {}
	for k, v in result.items ():
		if isinstance (v, np.ndarray):
			resp [k] = v.tolist ()
		else:
			resp [k] = v
	return resp

# JSON predict service -------------------------------------------------------
@app.route ("/models/<alias>/predict", methods = ['POST'])
@app.inspect (reduce__in = ['mean', 'max', 'min'])
def predict (was, alias, reduce = None, **inputs):
	model = tfserver.get_model (alias)
	inputs = { k: np.array (v) for k, v in inputs.items () }
	result = model.predict (inputs, as_dict = True, reducer = reduce)
	return was.API (result = serialize (result))

# POST predict service -------------------------------------------------------
@app.route ("/models/<alias>/media/predict", methods = ['POST'])
@app.inspect (reduce__in = ['mean', 'max', 'min'])
def predict_media (was, alias, media, reduce = None, **options):
	assert hasattr (media, 'path'), was.Error ('400 Bad Request', 'file stream is required')
	model = tfserver.get_model (alias)
	with media.as_flashfile ():
		xs = model.preprocess (media.path, **options)
	result = model.predict (xs, as_dict = True, reducer = reduce)
	return was.API (result = serialize (result))


# JSON management services --------------------------------------------
@app.route ("/models")
def models (was):
	return was.API (models = tfserver.models ())

@app.route ("/models/<alias>", methods = ['GET', 'PATCH', 'DELETE'])
def model (was, alias):
	if was.request.method == 'GET':
		model = tfserver.get_model (alias)
		return was.API (
			path = model.model_root,
			version = model.version,
			labels = {lb.name: lb.items () for lb in model.labels or []}
		)

	if was.request.method == 'PATCH': # reload model
		tfserver.refresh_model (alias)
		app.emit ('tfserver:model-reloaded', alias)
		return was.API ('204 No Content')

	tfserver.delete_model (alias)
	app.emit ('tfserver:model-unloaded', alias)
	return was.API ('204 No Content')

@app.route ("/models/<alias>/versions/<int:version>", methods = ['PUT', 'POST'])
@app.inspect (booleans = ['refresh', 'overwrite'])
def put_model (was, alias, version, model, refresh = True, overwrite = False, config = None):
	with model.flashfile () as zfile:
		try:
			tfserver.add_version (alias, version, zfile, refresh, overwrite, config)
		except AssertionError:
			raise was.Error ('409 Conflict')
	app.emit ('tfserver:model-reloaded', alias)
	return was.API ('201 Created')

@app.route ("/models/<alias>/version", methods = ['GET'])
@app.route ("/model/<alias>/version", methods = ['GET']) # lower versoion compat
def version (was, alias):
	sess = tfserver.tfsess.get (alias)
	if sess is None:
		return was.response ("404 Not Found")
	return was.API (version = sess.get_version ())

@app.route ("/models/<alias>/versions/<int:version>", methods = ['DELETE'])
def delete_model_version (was, alias, version):
	tfserver.delete_versions (alias, version)
	app.emit ('tfserver:model-reloaded', alias)
	return was.API ('204 No Content')

@app.route ("/models/<alias>/versions", methods = ['DELETE'])
@app.inspect (lists = ['versions'])
def delete_model_versions (was, alias, versions):
	tfserver.delete_versions (alias, versions)
	return was.API ('204 No Content')
