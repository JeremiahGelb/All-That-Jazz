
import random
from load_pickle import return_songs_as_list_of_lists_of_np_arrays
from Chord import Chord
import numpy as np

def data_gen(chords_on_either_side=2, batch_size=10):
    """
    Will return a batch of input data and their labels
    Chords on either side is the number of chords on either side of the target chord

    So if chords on either side is 1 and batch size is two
    
    if the song looked like
    preceding_chord_1, target_chord1, following_chord_1
    preceding_chord_2, target_chord2, following_chord_2


    the x data will look like [preceding_chord_1, following_chord_1
                               preceding_chord_2, following_chord_2]

    and the y data will be [target_chord1
                            target_chord2]
    """
    songs = return_songs_as_list_of_lists_of_np_arrays()
    len_sequence = 2*chords_on_either_side + 1
    songs = [song for song in songs if len(song) >= len_sequence] #filter short songs
    while True:
        x_batch = []
        y_batch = []

        for i in range(batch_size):
            # Create random arrays
            rand_song = random.choice(songs) #this will overvalue chords from short songs
            #print(rand_song)

            
            first_xchord_min_index = 0
            first_xchord_max_index = len(rand_song) - len_sequence
            first_xchord_index = random.randint(first_xchord_min_index, first_xchord_max_index)

            #print("------")
            #print(first_xchord_min_index, first_xchord_max_index, first_xchord_index)
            #print("------")

            x_before = rand_song[first_xchord_index:(first_xchord_index+chords_on_either_side)]
            y = rand_song[first_xchord_index+chords_on_either_side]
            x_after = rand_song[(first_xchord_index+chords_on_either_side+1): first_xchord_index+chords_on_either_side+chords_on_either_side+1]

            x = np.array(x_before + x_after)

            #print(np.shape(x))
            #print(np.shape(x_batch))
            #print("------")
            #print(x_after)
            #print("------")

            x_batch.append(x)
            y_batch.append(y)
        #print("Shape of x Batch: ")
        #print(np.shape(x_batch))
        #print("Shape of y Batch: ")
        #print(np.shape(y_batch))
        yield np.array(x_batch), np.array(y_batch), [None] #Magic None to avoid warning :)