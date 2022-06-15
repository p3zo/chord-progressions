from chord_progressions.chord import Chord
from chord_progressions.io.midi import make_midi_progression


class Progression:
    def __init__(self, chords: list[Chord]):
        self.chords = chords

    def from_audio(self, filepath):
        return

    def to_audio(self):
        return

    def from_midi(self):
        return

    def to_midi(self):
        return make_midi_progression(self.chords)
