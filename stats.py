print("Loading pickled songs...")
from load_pickle import return_songs_as_list_of_lists_of_chords, return_songs_as_list_of_lists_of_np_arrays
songs_chords = return_songs_as_list_of_lists_of_chords()


from Chord import Chord
helper_chord = Chord()

counts_by_chord = {}
counts_by_root = {}
counts_by_quality = {}
total_chords = 0
for song in songs_chords:
    for chord in song:
        total_chords += 1
        try:
            counts_by_chord[chord] += 1
        except:
            counts_by_chord[chord] = 1
        try:
            counts_by_root[chord.root] += 1
        except:
            counts_by_root[chord.root] = 1
        try:
            counts_by_quality[chord.quality] += 1
        except:
            counts_by_quality[chord.quality] = 1

count_chord = []
for chord in counts_by_chord:
    count_chord.append((chord, counts_by_chord[chord]/total_chords))

count_root = []
for root in counts_by_root:
    count_root.append((root, counts_by_root[root]/total_chords))

count_quality = []
for quality in counts_by_quality:
    count_quality.append((quality, counts_by_quality[quality]/total_chords))

count_chord.sort(key=lambda pair: pair[1])
count_root.sort(key=lambda pair: pair[1])
count_quality.sort(key=lambda pair: pair[1])


print("-----------------------")
print("Top 10 chords")
for item in count_chord[-10:]:
    print(item[0], ":", "{:.2%}".format(item[1]))
print("-----------------------")


print("-----------------------")
print("All Roots")
for item in count_root:
    print(helper_chord.to_root_string[item[0]], ":", "{:.2%}".format(item[1]))
print("-----------------------")


print("-----------------------")
print("All Qualities")
for item in count_quality:
    print(helper_chord.to_quality_string[item[0]], ":", "{:.2%}".format(item[1]))
print("-----------------------")