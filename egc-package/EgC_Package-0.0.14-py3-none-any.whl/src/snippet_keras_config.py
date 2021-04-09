# Function for deleting in output console the runfile... - ong string
from time import sleep

def cls():
    print("\033[2J\033[;H", end='Console out >>>>\n')
    sleep(0.1)

cls()

#----------------------------------------------------------------------------------------

import keras as ker
import tensorflow as tfl
from tensorflow.keras.mixed_precision import experimental as mixed_precision

# Set the computing precision via Policy
if tfl.config.list_physical_devices('CPU') != []:  # Adapt to 'GPU'
 
    # Adapt precision policy for minimal data type size 
    objPol = mixed_precision.Policy('mixed_float16')
    mixed_precision.set_policy(objPol)


print('Global policy dtype (used for computation): %s' % objPol.compute_dtype)
print('Local variable dtype (cast via global policy): %s' % objPol.variable_dtype)

# Clean up backend (reset name / number increment base)
ker.backend.clear_session()



#%%
import keras as ker
import tensorflow as tfl
from tensorflow.keras.mixed_precision import experimental as mixed_precision

# Set the computing precision via Policy
if tfl.config.list_physical_devices('CPU') != []:  # Adapt to 'GPU'
 
    # Adapt precision policy for minimal data type size 
    objPol = mixed_precision.Policy('mixed_float16')
    mixed_precision.set_policy(objPol)


print('Global policy dtype (used for computation): %s' % objPol.compute_dtype)
print('Local variable dtype (cast via global policy): %s' % objPol.variable_dtype)

# Clean up backend (reset name / number increment base)
ker.backend.clear_session() # Also possible: # Theano, CNTK
# Demo get next ID
# ker.backend.get_uid(prefix="")


#%% Work with tensors
import numpy as np

# Initialize tensor dimensions
shpTnsX = 1000
strNamSpc = 'EgCscope'

# Declare tensor and init scope, here 'PAG'
tVals = ker.backend.placeholder(shape=(shpTnsX,), name='strNamSpc', dtype='float16')
tVals2 = ker.backend.placeholder(shape=(shpTnsX,), name='strNamSpc', dtype='float16')

# Declare tensor related function-call
tValsPow2 = ker.backend.square(tVals)
tValsCos =  ker.backend.cos(tVals)
tValsArgmin =  ker.backend.argmin(tVals)

# Use tensors for simple math operations
arDemoVals = np.ones((shpTnsX,))
objFcnExec = ker.backend.function([tVals], [tValsPow2, tValsCos, tValsArgmin])

lsArRes = objFcnExec([arDemoVals])

#%% Create tensor of random variables (here EagerTensor from Keras, not the 
#   standard TensorFlow Tensor)

teVals = tfl.random.normal(shape=(shpTnsX, ), mean=0.0, stddev=1.0)
teVals2 = tfl.random.uniform(shape=(shpTnsX, 1), minval=0, maxval=10, dtype="int32")

#import matplotlib.pyplot as plt
# plt.plot(teVals2.numpy())

