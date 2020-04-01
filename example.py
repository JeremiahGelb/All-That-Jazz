
from Chord import Chord
from load_pickle import return_songs_as_list_of_lists_of_chords, return_songs_as_list_of_lists_of_np_arrays

songs = return_songs_as_list_of_lists_of_np_arrays()

printed_one_already = False

for song in songs:
    # at this level we have each song, which is a list of chords
    for chord in song:
        # because of the import function I used,
        # chords are represented in numpy arrays (one hot)
        if not printed_one_already:
            #this will print the numpy array
            print(chord)
            printed_one_already = True
            # if you want to go from an array to human readable, you can construct a Chord object
            chord_object = Chord(np_array=chord)
            print(chord_object)

            #rn there is no tranpose method on a chord, but you could implement it like this
            old_root = chord_object.root
            semitones_up = 1
            new_root = (old_root + semitones_up) % chord_object.number_of_unique_roots
            chord_object.root = new_root
            print(chord_object)




