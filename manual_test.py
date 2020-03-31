from Chord import Chord

chord = Chord("C:maj")
print(chord)

chord = Chord("Db")
print(chord)

try:
    chord = Chord("this_wi:ll_fail")
except:
    print("failed as expected")


chord = Chord()
print(chord)
