"""
Evaluates a random chord progression and returns its evaluation.

Useful for checking the state of the evaluator.
"""

from pprint import pprint

from chord_progressions.chord import (
    serialize_chords,
    get_chords_from_chord_string,
)
from chord_progressions.evaluator import evaluate_chord, evaluate_progression
from chord_progressions.solver import select_chords
from chord_progressions.type_templates import TYPE_TEMPLATES


def get_random_progression(n_segments):

    locks = "0" * n_segments

    chord_types, chords = select_chords(
        n_segments=n_segments,
        n_notes_min=0,
        n_notes_max=12,
        pct_notes_common=0,
        note_range_low=60,
        note_range_high=108,
        spacing_cutoff=52,
        min_spacing=4,
        allowed_chord_types=list(TYPE_TEMPLATES),
        existing_chords=None,
        existing_types=None,
        locks=locks,
        adding=False,
        first_chord=None,
    )

    durations = ["1m"] * len(chords)

    chord_metrics = [evaluate_chord(c) for c in chords]

    return serialize_chords(chords, chord_types, durations, chord_metrics, locks)


if __name__ == "__main__":

    n_chords = 3

    progression = get_random_progression(n_chords)

    metrics = evaluate_progression(progression, serialized=True)

    pprint(metrics)

    """
        Without You I Am A Lie - Dustin O'Halloran
        chordi.co/ZMbw0YXO
    """
    chord_str = "37-53-63_39-55-60-63_44-55-60-63-67_46-58-63-65-67"
    chords = get_chords_from_chord_string(chord_str)

    metrics = evaluate_progression(chords)

    chords[0]
    ["C#2", "F3", "D#4"]

    """
        Extension of whole-tone trichord experiments in scratch.md (chordi.co/-jYoWbMr)
        chordi.co/D5q5jb6V
    """
    chord_str = "73-75-77_61-63-65_49-51-53_49-53-63_37-53-63_37-49-53-63-65-73-77_37-39-53_53-73-75_37-39-41-49-51-53-61-63-65-73-75-77"
    chords = get_chords_from_chord_string(chord_str)

    metrics = evaluate_progression(chords)
