from Chord import Chord

chord1 = Chord("C:maj")

chord2 = Chord("C")

print(chord1, "=", chord2, "?", chord1==chord2)

try:
    chord = Chord("this_wi:ll_fail")
except:
    print("failed as expected")


chord = Chord()
print(chord)

