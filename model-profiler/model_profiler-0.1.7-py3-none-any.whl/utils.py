import numpy as np
import tensorflow as tf
from tensorflow.python.client import device_lib


#%%
'''
For appropriate units
'''

multiplier = {
    'GB': 1 / 1024**3,     # memory unit gega-byte
    'MB': 1 / 1024**2,     # memory unit mega-byte
    'MFLOPs': 1 / 10**8,   # FLOPs unit million-flops
    'BFLOPs': 1 / 10**11,  # FLOPs unit billion-flops
    'Million': 1 / 10**6,  # paprmeter count unit millions
    'Billion': 1 / 10**9,  # paprmeter count unit billions
}
# will make the ouput in appropriate unit
def multiply(fn):
    def deco(units, *args, **kwds):
        return multiplier.get(units, -1) * fn(*args, **kwds)
    return deco
#%%
def get_available_gpus():
    """ Get available GPU devices info. """
    try:
        local_device_protos = device_lib.list_local_devices()
        gpus = [x.name for x in local_device_protos if x.device_type == 'GPU']
        names = []
        for i in gpus:
            names.append(i[-1:])
    except:
        names = 'None Detected'
    return names
#%%
@multiply
def get_param(model):
    '''Return Model Parameters in unit scale'''
    trainable_param = model.count_params()
    return trainable_param    #(trainable_param / 1000**2)
#%%
@multiply
def mem_for_storing_weights(model):
    '''Return mnemory required to store model parameters in bytes'''
    mem_req = model.count_params() * 4
    return mem_req
#%%
@multiply
def keras_model_memory_usage(model, batch_size):
    """
    Return the estimated memory usage of a given Keras model in bytes.
    This includes the model weights and layers, but excludes the dataset.

    The model shapes are multipled by the batch size, but the weights are not.

    Args:
        model: A Keras model.
        batch_size: The batch size you intend to run the model with. If you
            have already specified the batch size in the model itself, then
            pass `1` as the argument here.
    Returns:
        An estimate of the Keras model's memory usage in bytes..

    """
    default_dtype = tf.keras.backend.floatx()
    shapes_mem_count = 0
    internal_model_mem_count = 0
    for layer in model.layers:
        if isinstance(layer, tf.keras.Model):
            internal_model_mem_count += keras_model_memory_usage(
                layer, batch_size=batch_size
            )
        single_layer_mem = tf.as_dtype(layer.dtype or default_dtype).size
        out_shape = layer.output_shape
        if isinstance(out_shape, list):
            out_shape = out_shape[0]
        for s in out_shape:
            if s is None:
                continue
            single_layer_mem *= s
        shapes_mem_count += single_layer_mem

    trainable_count = sum(
        [tf.keras.backend.count_params(p) for p in model.trainable_weights]
    )
    non_trainable_count = sum(
        [tf.keras.backend.count_params(p) for p in model.non_trainable_weights]
    )

    total_memory = (
        batch_size * shapes_mem_count
        + internal_model_mem_count
        + trainable_count
        + non_trainable_count
    )
    
    # convery into bytes to GB
    # total_memory = total_memory / 1024**3
    return total_memory       
#%%
# bunch of cal per layer
def count_linear(layers):
    MAC = layers.output_shape[1] * layers.input_shape[1]
    if layers.get_config()["use_bias"]:
        ADD = layers.output_shape[1]
    else:
        ADD = 0
    return MAC*2 + ADD

def count_conv2d(layers, log = False):
    # if log:
    #     print(layers.get_config())
    # number of conv operations = input_h * input_w / stride = output^2
    numshifts = int(layers.output_shape[1] * layers.output_shape[2])
    
    # MAC/convfilter = kernelsize^2 * InputChannels * OutputChannels
    MACperConv = layers.get_config()["kernel_size"][0] * layers.get_config()["kernel_size"][1] * layers.input_shape[3] * layers.output_shape[3]
    
    if layers.get_config()["use_bias"]:
        ADD = layers.output_shape[3]
    else:
        ADD = 0
        
    return MACperConv * numshifts * 2 + ADD
@multiply
def count_flops(model, log = False):
    '''
    Parameters
    ----------
    model : A keras or TF model
    Returns
    -------
    Sum of all layers FLOPS in unit scale, you can convert it 
    afterward into Millio or Billio FLOPS
    '''
    layer_flops = []
    # run through models
    for layer in model.layers:
        if "dense" in layer.get_config()["name"] or "fc" in layer.get_config()["name"]:
            layer_flops.append(count_linear(layer))
        elif "conv" in layer.get_config()["name"] and "pad" not in layer.get_config()["name"] and "bn" not in layer.get_config()["name"] and "relu" not in layer.get_config()["name"] and "concat" not in layer.get_config()["name"]:
            layer_flops.append(count_conv2d(layer,log))
        elif "res" in layer.get_config()["name"] and "branch" in layer.get_config()["name"]:
            layer_flops.append(count_conv2d(layer,log))
        elif "stage" in layer.get_config()['name']:
            layer_flops.append(count_conv2d(layer,log))
            
    return np.sum(layer_flops)     #/10**11