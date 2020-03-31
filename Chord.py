EMPTY_FIELD = -1

from to_root_int import TO_ROOT_INT
from to_quality_int import TO_QUALITY_INT
import numpy as np

class Chord:
    def base(self):
        self.root = EMPTY_FIELD
        self.quality = EMPTY_FIELD
        self.to_root_int = TO_ROOT_INT
        self.to_quality_int = TO_QUALITY_INT

        self.to_root_string = {}
        for key in self.to_root_int:
            self.to_root_string[self.to_root_int[key]] = key

        self.to_quality_string = {}
        for key in self.to_quality_int:
            self.to_quality_string[self.to_quality_int[key]] = key
        
        self.number_of_unique_roots = max(key for key in self.to_root_string) + 1
        self.number_of_unique_qualities = max(key for key in self.to_quality_string) + 1

    def set_from_np_array(self, np_array):
        index = np.argmax(np_array)
        if (np_array[index] == 0):
            self.root = EMPTY_FIELD
            self.quality = EMPTY_FIELD
            return

        self.root = index//self.number_of_unique_qualities
        self.quality = index%self.number_of_unique_qualities

    def np_array(self):
        #print("number_of_unique_roots", self.number_of_unique_roots)
        #print("number_of_unique_qualities", self.number_of_unique_qualities)
        if (self.root == EMPTY_FIELD or self.quality == EMPTY_FIELD):
            return np.zeros((self.number_of_unique_roots * self.number_of_unique_qualities,))

        np_array = np.zeros((self.number_of_unique_roots * self.number_of_unique_qualities,))
        #grouping chords with the same root next to eachother
        index = self.number_of_unique_qualities * self.root + self.quality
        np_array[index] = 1
        return np_array

    def set_from_chord_string(self, chord_string):
        try:
            root_string, quality_string = chord_string.split(':')
            self.root = self.to_root_int[root_string]
            self.quality = self.to_quality_int[quality_string]
        except KeyError as e:
            # print("Chord:", chord_string)
            #print("UNRECOGNIZED VALUE:", e)
            raise
        except ValueError as e:
            try:
                self.root = self.to_root_int[chord_string]
                self.quality = self.to_quality_int[None]
            except KeyError as e:
                # print("Chord:", chord_string)
                #print("UNRECOGNIZED whole chord:", e)
                raise
    
    def __init__(self, chord_string=None, np_array=None):
        self.base()
        if np_array is not None:
            self.set_from_np_array(np_array)
        if chord_string is not None:
            self.set_from_chord_string(chord_string)

    def __str__(self):
        root = self.to_root_string[self.root] if self.root != EMPTY_FIELD else "empty"
        quality = self.to_quality_string[self.quality] if self.quality != EMPTY_FIELD else "empty"
        return root + ":" + quality

    def __eq__(self, other):
        return self.quality == other.quality and self.root == other.root
