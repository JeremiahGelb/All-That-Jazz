EMPTY_FIELD = -1

class Chord:
    def base(self):
        self.root = EMPTY_FIELD
        self.quality = EMPTY_FIELD
        self.to_root_int = {
            #enharmonic to C
            'B#' : 0,
            'C' : 0,

            #enharmonic to Db
            'C#' : 1,
            'Db' : 1,

            #enharmonic to D
            'D' : 2,

            #enharmonic to Eb
            'D#' : 3,
            'Eb' : 3,

            #enharmonic to E
            'Fb' : 4,
            'E' : 4,

            #enharmonic to F
            'D#' : 5,
            'F' : 5,

            #enharmonic to Gb
            'F#' : 6,
            'Gb' : 6,

            #enharmonic to G
            'G' : 7,

            #enharmonic to Ab
            'G#' : 8,
            'Ab' : 8,

            #enharmonic to A
            'A' : 9,

            #enharmonic to Bb
            'A#' : 10,
            'Bb' : 10,

            #enharmonic to B
            'Cb' : 11,
            'B' : 11,
        }
        self.to_quality_int = {
            # major
            '' : 0,
            None : 0,
            'maj(7,9,11,13)' : 0,
            'maj(2,*3)/3' : 0,
            '9/3' : 0,
            '9/5' : 0,
            '6(9)' : 0,
            '6(9)/5' : 0,
            'maj/3' : 0,
            '9' : 0,
            'maj/5' : 0,
            'maj6' : 0,
            'maj7' : 0,
            'maj9' : 0,
            'maj7/2' : 0,
            'maj6/2' : 0,
            'maj7/5' : 0,
            "maj/2" : 0,
            'maj/7' : 0,
            'maj7/7' : 0,
            'maj/6' : 0,
            'maj6/5' : 0,
            '9/2' : 0,
            'maj6/3' : 0,
            'maj7/3' : 0,
            'maj' : 0,

            # 7
            '7/b7' : 1,
            'maj/b7' : 1,
            '7/3' : 1,
            '7/5' : 1,
            '9/b7' : 1,
            'maj(b7,9,11,13)' : 1,
            '7' : 1,

            # min7
            'min(7)/b3' : 2,
            'min/b3' : 2,
            'min/b7' : 2,
            'min7/b3' : 2,
            'min7/5' : 2,
            'min/5' : 2,
            'min9' : 2,
            'min7/4' : 2,
            'min(7)' : 2,
            'min/2' : 2,
            'min' : 2,
            'min(b7,9,11)' : 2,
            'min7/b7' : 2,
            'min7' : 2,

            # min6
            'min6/b3' : 3,
            'min6/6' : 3,
            'min6/5' : 3,
            'min6/2' : 3,
            'min6' : 3,

            # dim
            'dim/6' : 4,
            'dim/3' : 4,
            'dim' : 4,

            # half dim: 5
            'hdim/4' : 5,
            'hdim/b5' : 5,
            "hdim" : 5,

            # sus 4
            '(1,4,5,b7,9,11,13)' : 6,
            'sus4(b7)/5' : 6,
            'sus4(b7,9)' : 6,
            'sus4(b7)' : 6,
            'sus4' : 6,

            # flat 5 flat regular 9
            '(1,3,b5,b7,9,13)' : 7,
            '9(b5,*5)' : 7,
            'maj(b7,9,s11,13)' : 7,
            '7(b5,*5)/5' : 7,
            '9(s11)' : 7,
            '7(b5,*5)/b5' : 7,
            '7(s11)' : 7,
            '(1,3,b5,b7,9,13)/b5' : 7,
            '7(b5,*5)' : 7,
            
            # just b9 (jimi hendrix chord)
            'maj/b2' : 8,
            'maj(b7,b9,11,13)' : 8,
            '7(b9)' : 8,

            #flat 5 sharp 9
            '7(s9,s11,b13)' : 9,
            '7(s9)' : 9,

            #sharp 5 flat 9
            '7(s5,*5,b9)' : 10,

            #sharp 5 sharp 9
            '7(s5,*5,s9)' : 11,

            # #5 regular 9
            'maj/b6' : 12,
            'aug' : 12,
            '7(s5,*5)' : 12,
            'aug(b7,9)' : 12,
            '9(s5,*5)' : 12,
            'aug(b7)' : 12,

            # sus 2
            'maj(2,*3)/5' : 13,
            'maj(2,*3)' : 13,
            'sus2' : 13,
        }

        self.to_root_string = {}
        for key in self.to_root_int:
            self.to_root_string[self.to_root_int[key]] = key

        self.to_quality_string = {}
        for key in self.to_quality_int:
            self.to_quality_string[self.to_quality_int[key]] = key

    def __init__(self, chord_string=None):
        self.base()
        if chord_string is not None:
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