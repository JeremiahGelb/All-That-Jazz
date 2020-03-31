import pickle
from Chord import Chord

line_count = 0
chord_count = 0
complete_songs_count = 0
exception_count = 0
unknown_set = set()

PICKLE_FILE = "songs.pickle"

songs = []

with open("test.txt","r") as f:
    for line in f:
        #bad hack to get rid of _START_ and _END_
        line = line[8:-7]
        line_count = line_count + 1
        song_had_exception = False
        song = []
        for chord_string in line.split(" "):
            if chord_string:
                chord_count = chord_count + 1
                try:
                    chord = Chord(chord_string)
                    # filtering duplicate serial chords
                    if not song or chord != song[-1]:
                        song.append(chord)
                except Exception as e:
                    song_had_exception = True
                    unknown_set.add(str(e))
                    exception_count = exception_count + 1
        if not song_had_exception:
            complete_songs_count = complete_songs_count + 1
            songs.append(song)

for e in unknown_set:
    print(e)

for chord in songs[0]:
    #print(chord)
    pass

print("total songs:", line_count)
print("complete_songs_count:",  complete_songs_count)
print("total chords(not unique):", chord_count)
print("total unknown chords:", exception_count)
print("total types of unkown chords:", len(unknown_set))

with open(PICKLE_FILE, "wb") as f:
    pickle.dump(songs, f)
