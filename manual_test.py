from Chord import Chord

chord1 = Chord("C:maj")

chord2 = Chord("C")

print(chord1, "=", chord2, "?", chord1==chord2)

try:
    chord = Chord("this_wi:ll_fail")
except:
    print("failed as expected")


chord = Chord()
print(chord, Chord(np_array=chord.np_array()))
for root in range(chord.number_of_unique_roots):
    for quality in range(chord.number_of_unique_qualities):
        chord.root = root
        chord.quality = quality
        chord2 = Chord(np_array=chord.np_array())
        if (chord != chord2):
            print("ERROR with np array")
            print(chord, chord2)

print("Loading pickled songs...")
from load_pickle import return_songs_as_list_of_lists_of_chords, return_songs_as_list_of_lists_of_np_arrays
songs_chords = return_songs_as_list_of_lists_of_chords()
songs_arrays = return_songs_as_list_of_lists_of_np_arrays()

print("testing pickle...")
for song_index, song in enumerate(songs_chords):
    for chord_index, chord in enumerate(song):
        if (chord != Chord(np_array=songs_arrays[song_index][chord_index])):
            print("error depickling")
            print(chord, Chord(np_array=songs_arrays[song_index][chord_index]))