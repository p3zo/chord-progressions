"""
A script to experiment with some counterpoint rules to construct parsimoniously voice-led progressions.

Rules:
    - 1 to n-1 notes can change each chord
    - Up to 1 note can be added or removed
    - Added notes can be... []
    - chords can range from 3 - 5 notes
    - 1 - 3 notes can change each chord
    - Can change by semitone or whole tone up or done
"""

import os

import numpy as np

from chord_progressions.chord import Chord
from chord_progressions.pitch import get_midi_num_from_note
from chord_progressions.progression import Progression
from chord_progressions.utils import get_run_id

try:
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
except:
    THIS_DIR = os.getcwd()

OUTPUT_AUDIO_DIR = os.path.join(THIS_DIR, "../assets/output/wav")


def choose_change_amount():
    choices = [-2, -1, 1, 2]  # num semitones
    return np.random.choice(choices)


def choose_add_amount(n):
    """n is the number of notes in the current chord"""
    choices = [-1, 0, 1]  # num notes
    if n == 2:
        choices.remove(-1)
    elif n == 5:
        choices.remove(1)
    return np.random.choice(choices)


def get_voice_led_progression(start):
    midi_chords = [start]

    n_chords = 12

    for i in range(1, n_chords + 1):
        chord = midi_chords[i - 1].copy()

        n_notes = len(chord)

        # choose which notes will change
        changes = np.random.choice(2, n_notes)

        one_ix = [ix for ix, i in enumerate(changes) if i == 1]

        for ix in one_ix:
            chord[ix] += choose_change_amount()

        add = choose_add_amount(n_notes)

        if add == -1:
            ix_to_rm = np.random.randint(n_notes)
            del chord[ix_to_rm]

        elif add == 1:
            ix_to_duplicate = np.random.randint(n_notes)
            new_note = chord[ix_to_duplicate] + choose_change_amount()
            chord.append(new_note)

        midi_chords.append(chord)

    chords = [Chord([n for n in c]) for c in midi_chords]

    durations = [1] * len(chords) # seconds

    run_id = get_run_id()

    progression = Progression(chords, durations, name=run_id)

    audio_outpath = os.path.join(OUTPUT_AUDIO_DIR, f"{run_id}.wav")
    progression.save_audio(audio_outpath, n_overtones=0)

    return chords


if __name__ == "__main__":
    whole_tone_trichord = [37, 53, 63]

    major_chord = [get_midi_num_from_note(n) for n in ["G#2", "G3", "C4", "D#4", "G4"]]

    chords = get_voice_led_progression(start=major_chord)
