EMPTY_FIELD = -1

from to_root_int import TO_ROOT_INT
from to_quality_int import TO_QUALITY_INT

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

    def __init__(self, chord_string=None):
        self.base()
        if chord_string:
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


    def __str__(self):
        root = self.to_root_string[self.root] if self.root != EMPTY_FIELD else "empty"
        quality = self.to_quality_string[self.quality] if self.quality != EMPTY_FIELD else "empty"
        return root + ":" + quality

    def __eq__(self, other):
        return self.quality == other.quality and self.root == other.root