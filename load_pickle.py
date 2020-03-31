import pickle

PICKLE_FILE = "songs.pickle"

def return_songs_as_list_of_lists_of_chords(filename=PICKLE_FILE):
    with open(PICKLE_FILE, 'rb') as f:
        return pickle.load(f)

def return_songs_as_list_of_lists_of_np_arrays(filename=PICKLE_FILE):
    songs = return_songs_as_list_of_lists_of_chords(filename)
    return [[chord.np_array() for chord in song] for song in songs]