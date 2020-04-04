import collections
import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf

from tensorflow.keras import layers

from Chord import Chord

from data_gen import data_gen

sample_chord = Chord()
chord_array_len = sample_chord.number_of_unique_roots * sample_chord.number_of_unique_qualities

batch_size = 50
chords_on_either_side = 3


model = tf.keras.Sequential()

model.add(layers.Dense(200,
          input_shape=(2*chords_on_either_side, chord_array_len)))

model.add(layers.Dropout(0.2))
model.add(layers.Dense(300))
model.add(layers.Dropout(0.4))

model.add(layers.Flatten())
model.add(layers.Dense(192))

model.add(layers.Activation('softmax'))

model.compile(
    loss='categorical_crossentropy',
    optimizer='rmsprop',
    metrics=['accuracy']
)

model.summary()

#currently training and validaiting with random data
model.fit(
    data_gen(chords_on_either_side=chords_on_either_side, batch_size=batch_size),
    steps_per_epoch=1024,
    epochs=100,
)