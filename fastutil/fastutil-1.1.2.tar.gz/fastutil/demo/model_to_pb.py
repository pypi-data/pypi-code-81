import tensorflow as tf
from tensorflow.keras.backend import set_session
from tensorflow.keras.models import load_model
import os

os.environ['CUDA_VISIBLE_DEVICES'] = ''
model_path = '/data1/minisearch/upload/wenjie29/sync/video_dup_model/similarity_model_v2/data/20210218_194201_e9cc774c/model.h5'
finger_save_dir = '/data1/minisearch/upload/wenjie29/model/finger_model'
sim_save_dir = '/data1/minisearch/upload/wenjie29/model/sim_model'

sess = tf.Session()
set_session(sess)
model = load_model(model_path)
model.summary()
graph = tf.get_default_graph()
tf.saved_model.simple_save(
    sess,
    finger_save_dir,
    inputs={"input": model.inputs[0]},
    outputs={"finger": model.layers[-2].get_output_at(0)})

# if tf.__version__.startswith('1'):
#     sess = tf.Session()
#     set_session(sess)
#     model = load_model(model_path)
#     model.summary()
#     graph = tf.get_default_graph()
#     tf.saved_model.simple_save(
#         sess,
#         finger_save_dir,
#         inputs={"input": model.inputs[0]},
#         outputs={"finger": model.layers[-5].output})
#     tf.saved_model.simple_save(
#         sess,
#         sim_save_dir,
#         inputs={"input0": model.layers[-5].output, "input1": model.layers[-5].output},
#         outputs={"sim": model.output})
# else:
#     model = load_model(model_path)
#     model.summary()
#     tf.keras.models.save_model(model, finger_save_dir, include_optimizer=True)
