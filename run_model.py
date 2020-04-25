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

from metrics import f1_m
from tensorflow.keras.models import load_model
from load_pickle import return_songs_as_list_of_lists_of_chords, return_songs_as_list_of_lists_of_np_arrays

# import matplotlib.pyplot as plt
#TEST_FILE = "test.pickle"
sample_chord = Chord()
chord_array_len = sample_chord.number_of_unique_roots * sample_chord.number_of_unique_qualities

batch_size = 50
chords_on_either_side = 3
STEPS_PER_EPOCH = 1024
TOTAL_EPOCHS = 20
OUTPUT_BATCH = 25 # song created is of length (chords): (OUTPUT_BATCH * chords_on_either_side * 2) + OUTPUT_BATCH
TOP_NUM = 3 # The 'TOP_NUM' of the predictions, y are included/inserted in the generated song instead of only 1 chord.

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
    Adam(lr=0.001),
    loss='categorical_crossentropy',
    #optimizer='adam',
    metrics=['accuracy',f1_m]
)

model.summary()
plot_model(model, to_file='projF_model_plot.png', show_shapes=True, show_layer_names=True)
# currently training and validaiting with random data

'''
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
'''
#model.save_weights('ProjF_Weights_I_05.hd5')
#del model
#model = load_model('ProjF_Model.hd5')
model.load_weights('ProjF_Weights_I_05.hd5')


counter = 0
for chords_x,chord_y,n in data_gen(chords_on_either_side=chords_on_either_side, batch_size=OUTPUT_BATCH):
    counter = counter + 1
    if counter >= 1:
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
print("\r\nTraining Set: Correct Predictions: {}/{}  Accuracy: {}\r\n".format(matching_chords,total_chords,accuracy))



counter = 0
for chords_x,chord_y,n in testdata_gen(chords_on_either_side=chords_on_either_side, batch_size=OUTPUT_BATCH):
    counter = counter + 1
    if counter >= 1:
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
print("\r\nTest Set Correct Predictions: {}/{}  Accuracy: {}\r\n".format(matching_chords,total_chords,accuracy))


counter = 0
for chords_x,chord_y,n in testdata_output(chords_on_either_side=chords_on_either_side):
    counter = counter + 1
    if counter >= 1:
        break

ch_prediction_array = model.predict(x=chords_x)

#top_predictions = np.argpartition(ch_prediction_array[1],-3)[-3:]   # these are not sorted
#top_predictions = hq.nlargest(3,range(len(ch_prediction_array[0])),ch_prediction_array[0].take)

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
print("\r\nTest Set 2 Correct Predictions: {}/{}  Accuracy: {}".format(matching_chords,total_chords,accuracy))


#Make a the songs with the predictions, and insert multiple (TOP_NUM) predictions into the song at each location between sets of 'chords_on_either_side'
#generated_song_np = []
generated_song_text = []
generated_song_text_multi = []
for idx in range(0,total_chords):
    top_predictions = hq.nlargest(TOP_NUM, range(len(ch_prediction_array[idx])), ch_prediction_array[idx].take) # get the top 'TOP_NUM' prediction (indices)
    for j in range(0,chords_on_either_side):
        generated_song_text.append(str(Chord(np_array=chords_x[idx][j])))
        generated_song_text_multi.append(str(Chord(np_array=chords_x[idx][j])))
    for p in range(0,TOP_NUM):        # insert the top 3 predicitons
        predictions_top_predictions = tf.keras.utils.to_categorical(top_predictions[p],192)
        temp_str = "{} // Prediction# {}, {:1.7f}".format(str(Chord(np_array=predictions_top_predictions)),p+1,ch_prediction_array[idx][top_predictions[p]])
        if (p == 0):
            temp_str = temp_str + ", Actual: {}".format(str(Chord(np_array=chord_y[idx])))
            generated_song_text.append(temp_str)  #inserted the chord predition into generated song ****
        generated_song_text_multi.append(temp_str)  #inserted the chord predition into generated song ****
    for j in range(chords_on_either_side,chords_on_either_side*2):
        generated_song_text_multi.append(str(Chord(np_array=chords_x[idx][j])))
        generated_song_text.append(str(Chord(np_array=chords_x[idx][j])))


#Convert song to text to play with MMA
#generated_song_text = []
#for idx in range(0,len(generated_song_np)):
#        generated_song_text.append(Chord(np_array=generated_song_np[idx]))


#Create a text file of the new song, generated using the datagenerator, random batches with test_songs.txt as the source chords in MMA format


mma_tempo = random.randrange(90,180,1)   #Select a random tempo
mma_style_strings = ["Blues1","Blues","BossaNova","68Swing","strut","EasySwing","Swing2","BluesSus"]
mma_rand_style = random.randrange(0,len(mma_style_strings),1)
mma_style = mma_style_strings[mma_rand_style]  #select a random style


#Write the generated song with multiple predictions inserted
generated_song_file = open("projF_generated_song_multiple_predictions.mma", "w")
generated_song_file.write("// Song Details..\r\n")

generated_song_file.write("Tempo {}\n".format(mma_tempo))  #write the random tempo & groove style
generated_song_file.write("Groove {}\n".format(mma_style))

for idx in range(0,len(generated_song_text_multi)):
    generated_song_file.write(str("{} ".format(idx+1)))
    generated_song_str = generated_song_text_multi[idx].replace(":","")  #more translation would need to be done (seperate function) to fully automate (these get it mostly in MMA format)
    generated_song_str = generated_song_str.replace("min","m")
    generated_song_str = generated_song_str.replace("maj", "")
    generated_song_str = generated_song_str.replace("aug", "+")
    generated_song_str = generated_song_str.replace("(", "")
    generated_song_str = generated_song_str.replace(')', "")
    generated_song_file.write(generated_song_str)
    generated_song_file.write('\n')

generated_song_file.close()


#Write the generated song with single prediction inserted
generated_song_file = open("projF_generated_song.mma", "w")
generated_song_file.write("// Song Details..\r\n")

generated_song_file.write("Tempo {}\n".format(mma_tempo))  #write the random tempo & groove style
generated_song_file.write("Groove {}\n".format(mma_style))

for idx in range(0,len(generated_song_text)):
    generated_song_file.write(str("{} ".format(idx+1)))
    generated_song_str = generated_song_text[idx].replace(":","")  #more translation would need to be done (seperate function) to fully automate (these get it mostly in MMA format)
    generated_song_str = generated_song_str.replace("min","m")
    generated_song_str = generated_song_str.replace("maj", "")
    generated_song_str = generated_song_str.replace("aug", "+")
    generated_song_str = generated_song_str.replace("(", "")
    generated_song_str = generated_song_str.replace(')', "")
    generated_song_file.write(generated_song_str)
    generated_song_file.write('\n')

generated_song_file.close()
