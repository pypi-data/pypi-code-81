import os
import sys
import pickle
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from ms2deepscore import SpectrumBinner
from ms2deepscore.models import SiameseModel

ROOT = os.path.dirname(os.getcwd())
sys.path.insert(0, ROOT)
path_data = 'C:\\OneDrive - Netherlands eScience Center\\Project_Wageningen_iOMEGA\\Data\\'

#%%

import pickle
outfile = os.path.join(path_data, 'GNPS_all', 'ALL_GNPS_positive_train_split_binned_1.pickle')
with open(outfile, 'rb') as file:
    binned_spectrums_training = pickle.load(file)

outfile = os.path.join(path_data, 'GNPS_all', 'ALL_GNPS_positive_val_split_binned_1.pickle')
with open(outfile, 'rb') as file:
    binned_spectrums_val = pickle.load(file)

# #%%
filename = os.path.join(path_data, 'ALL_GNPS_210125_positive_tanimoto_scores.pickle')
tanimoto_df = pd.read_pickle(filename)



# #%%

import pickle
outfile = os.path.join(path_data, 'GNPS_all', 'ALL_GNPS_positive_training_spectrum_binner_1.pickle')
with open(outfile, 'rb') as file:
    spectrum_binner = pickle.load(file)
    

    
#%%
from ms2deepscore.data_generators import DataGeneratorAllSpectrums

dimension = len(spectrum_binner.known_bins)
same_prob_bins = list(zip(np.linspace(0,0.9,10), np.linspace(0.1,1,10)))

training_generator = DataGeneratorAllSpectrums(binned_spectrums_training, tanimoto_df,
                                               dim=dimension,
                                               same_prob_bins=same_prob_bins,
                                               augment_noise_max=20,
                                               augment_noise_intensity=0.1)

validation_generator = DataGeneratorAllSpectrums(binned_spectrums_val, tanimoto_df,
                                                 dim=dimension,
                                                 same_prob_bins=same_prob_bins,
                                                 num_runs=5,
                                                 augment_removal_max=0,
                                                 augment_removal_intensity=0,
                                                 augment_intensity=0,
                                                 augment_noise_max=0)


# #%%
model = SiameseModel(spectrum_binner, base_dims=(600, 500, 500), embedding_dim=400,
                     dropout_rate=0.25)
model.summary()

#%%
epochs = 150
learning_rate = 0.001
metrics = ["mae"]

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

# Parameters
patience_scoring_net = 10
model_output_file = "ms2ds_210210_ALL_GNPS_12k_600_500_500_400.hdf5"

model.compile(
    loss='mse',
    optimizer=Adam(lr=learning_rate),
    metrics=metrics)

checkpointer = ModelCheckpoint(
    filepath = model_output_file,
    monitor='val_loss', mode="min",
    verbose=1,
    save_best_only=True
    )

earlystopper_scoring_net = EarlyStopping(
    monitor='val_loss', mode="min",
    patience=patience_scoring_net,
    verbose=1
    )

history = model.model.fit(training_generator,
    validation_data=validation_generator,
    epochs = epochs,
    callbacks = [
        earlystopper_scoring_net,
        checkpointer,
        ]
    )


#%%
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12,8), dpi=200)

ax1.plot(history.history['loss'], "o--", label='MSE (training data)')
ax1.plot(history.history['val_loss'], "o--", label='MSE (validation data)')
ax1.set_title('MSE loss')
ax1.set_ylabel("MSE")
ax1.legend()

ax2.plot(history.history['mae'], "o--", label='training data')
ax2.plot(history.history['val_mae'], "o--", label='validation data')
ax2.set_title('MAE accuracy')
ax2.set_ylabel("MAE")
ax2.set_xlabel("epochs")
ax2.legend()

plt.savefig("ms2ds_210210_ALL_GNPS_positive_600_500_500_400_history.pdf")


#%%
model.save("ms2ds_siamese_210210_ALL_GNPS_positive_600_500_500_400.hdf5")

with open('ms2ds_210210_ALL_GNPS_positive_600_500_500_400_history.pickle', 'wb') as f:
    pickle.dump(history.history, f)


#%%
from tensorflow.keras.models import load_model as load_keras_model

keras_model_file_early_stopping = "ms2ds_210210_ALL_GNPS_positive_600_500_500_400.hdf5"
keras_model = load_keras_model(keras_model_file_early_stopping)

model_last_stop = SiameseModel(spectrum_binner, keras_model=keras_model)
model_last_stop.save("ms2ds_siamese_210210_ALL_GNPS_positive_600_500_500_400_early_stop.hdf5")


