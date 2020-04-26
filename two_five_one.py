
import collections
import matplotlib.pyplot as plt
import numpy as np
import heapq as hq
import tensorflow as tf
import random
from tensorflow.keras import layers
from tensorflow.keras.utils import plot_model
from tensorflow.keras.optimizers import Adam
from Chord import Chord
from data_gen import data_gen, testdata_gen, testdata_output
from tensorflow.keras.callbacks import CSVLogger
from metrics import f1_m
from tensorflow.keras.models import load_model
from load_pickle import return_songs_as_list_of_lists_of_chords, return_songs_as_list_of_lists_of_np_arrays

sample_chord = Chord()
chords_on_either_side = 3
chord_array_len = sample_chord.number_of_unique_roots * sample_chord.number_of_unique_qualities
LEARNING_RATE = 0.005

# START of model definition
model = tf.keras.Sequential()
model.add(layers.LSTM(512,activation='tanh',recurrent_activation='sigmoid',return_sequences=True,recurrent_dropout=0.1, input_shape=(2 * chords_on_either_side, chord_array_len)))
model.add(layers.LSTM(512,activation='tanh',recurrent_activation='sigmoid',dropout=0.2,return_sequences=False))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(chord_array_len))
#model.add(layers.Dense(len(chord_array_len)))
model.add(layers.Activation('softmax'))
# END of model definition

model.compile(
    Adam(lr=LEARNING_RATE),
    loss='categorical_crossentropy',
    #optimizer='adam',
    metrics=['accuracy',f1_m]
)

model.summary()

model.load_weights('ProjF_Weights_I_06_Idx_08.hd5')


chords = [Chord(), Chord("D:min7"), Chord("G:7"), Chord(), Chord(), Chord()]
chords_np = [chord.np_array() for chord in chords]

tfo_c_x = np.array(chords_np)

x = np.array([tfo_c_x, tfo_c_x, tfo_c_x])

tfo_x_y = model.predict(x=x)

output_chord = Chord(np_array = tfo_x_y[0])
print(output_chord)
