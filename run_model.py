import collections
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import random
from tensorflow.keras import layers
from Chord import Chord
from data_gen import data_gen
from tensorflow.keras.utils import plot_model
from metrics import f1_m
from tensorflow.keras.models import load_model

# import matplotlib.pyplot as plt

sample_chord = Chord()
chord_array_len = sample_chord.number_of_unique_roots * sample_chord.number_of_unique_qualities

batch_size = 50
chords_on_either_side = 4
STEPS_PER_EPOCH = 512
TOTAL_EPOCHS = 30
OUTPUT_BATCH = 5 # song created is of length (chords): (OUTPUT_BATCH * chords_on_either_side * 2) + OUTPUT_BATCH

# START of model definition
model = tf.keras.Sequential()
model.add(layers.LSTM(512,activation='tanh',recurrent_activation='sigmoid',return_sequences=True, input_shape=(2 * chords_on_either_side, chord_array_len)))
model.add(layers.Dropout(0.15))
model.add(layers.LSTM(256,activation='tanh',recurrent_activation='sigmoid',return_sequences=False))
model.add(layers.Dropout(0.15))
model.add(layers.Dense(chord_array_len))
model.add(layers.Activation('softmax'))
# END of model definition

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy',f1_m]
)


model.summary()
plot_model(model, to_file='projF_model_plot.png', show_shapes=True, show_layer_names=True)
# currently training and validaiting with random data


history = model.fit(
    data_gen(chords_on_either_side=chords_on_either_side, batch_size=batch_size),
    steps_per_epoch=STEPS_PER_EPOCH,
    epochs=TOTAL_EPOCHS,verbose=1)
    
  
# Plot training accuracy values
# Plot F1 Metric
plt.plot(history.history['f1_m'],marker=".",color="Blue")
plt.plot(history.history['accuracy'],marker="x",color="Red")
plt.title('Model Accuracy & F1-Score')
plt.ylabel('Metric Val.')
plt.xlabel('Epoch')
plt.legend(['F1-Score','Accuracy'], loc='lower right')
plt.savefig('ProjF_Plot_Accuracy_F1.png')
#plt.show()
plt.close()
# Plot training loss values
plt.plot(history.history['loss'],marker=".")
#plt.plot(history.history['val_loss'],marker="x")
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train'], loc='upper right')
plt.savefig('ProjF_Plot_Loss.png')
#plt.show()
plt.close()

model.save('ProjF_ModelC_07.hd5')
#del model
#model = load_model('ProjF_ModelB_01.hd5')


counter = 0
for chords_x,chord_y,n in data_gen(chords_on_either_side=chords_on_either_side, batch_size=OUTPUT_BATCH):
    counter = counter + 1
    if counter > 1:
        break

ch_prediction_array = model.predict(x=chords_x)

#obtain and print predictions from the array of chords_x obtained from data_gen
matching_chords = 0
total_chords = len(chords_x)
for idx in range(0,total_chords):
    if(np.argmax(ch_prediction_array[idx])==np.argmax(chord_y[idx])):
        matching_chords=matching_chords+1
    ch_prediction = Chord(np_array=ch_prediction_array[idx])
    ch_actual = Chord(np_array=chord_y[idx])
    print("index: {}  ch_prediction: {}  actual_chord: {} ".format(idx,ch_prediction, ch_actual))

accuracy = matching_chords / total_chords
print("Correct Predictions: {}/{}  Accuracy: {}".format(matching_chords,total_chords,accuracy))

#Make a the songs with the predictions, and original center chords using the data generator
generated_song_np = []
for idx in range(0,total_chords):
    for j in range(0,chords_on_either_side):
        generated_song_np.append(chords_x[idx][j])
    generated_song_np.append(ch_prediction_array[idx])  #inserted the chord predition into generated song
    for j in range(chords_on_either_side,chords_on_either_side*2):
        generated_song_np.append(chords_x[idx][j])


#Convert song to text to play with MMA
generated_song_text = []
for idx in range(0,len(generated_song_np)):
        generated_song_text.append(Chord(np_array=generated_song_np[idx]))


#Create a text file of the new song in MMA format


mma_tempo = random.randrange(90,180,1)   #Select a random tempo
mma_style_strings = ["Blues1","Blues","BossaNova","68Swing","strut","EasySwing","Swing2","BluesSus"]
mma_rand_style = random.randrange(0,len(mma_style_strings),1)
mma_style = mma_style_strings[mma_rand_style]  #select a random style
generated_song_file = open("projF_generated_song.mma", "w")
generated_song_file.write("// Song Details..\r\n")

generated_song_file.write("Tempo {}\n".format(mma_tempo))  #write the random tempo & groove style
generated_song_file.write("Groove {}\n".format(mma_style))

for idx in range(0,len(generated_song_np)):
    generated_song_file.write(str("{} ".format(idx+1)))
    generated_song_str = str(generated_song_text[idx]).replace(":","")  #more translation would need to be done (seperate function) to fully automate (these 3 get it mostly in MMA format)
    generated_song_str = generated_song_str.replace("min","m")
    generated_song_str = generated_song_str.replace("maj", "")
    generated_song_str = generated_song_str.replace("aug", "+")
    generated_song_str = generated_song_str.replace("(", "")
    generated_song_str = generated_song_str.replace(')', "")
    generated_song_file.write(generated_song_str)
    generated_song_file.write('\n')

generated_song_file.close()