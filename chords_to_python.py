from Chord import Chord

line_count = 0
chord_count = 0
exception_count = 0
unknown_set = set()

with open("test.txt","r") as f:
    for line in f:
        #bad hack to get rid of _START_ and _END_
        line = line[8:-7]
        line_count = line_count + 1
        for chord_string in line.split(" "):
            if chord_string:
                chord_count = chord_count + 1
                try:
                    Chord(chord_string)
                except Exception as e:
                    unknown_set.add(str(e))
                    exception_count = exception_count + 1

for e in unknown_set:
    print(e)

print("total songs:", line_count)
print("total chords(not unique):", chord_count)
print("total unknown chords:", exception_count)
print("total types of unkown chords:", len(unknown_set))