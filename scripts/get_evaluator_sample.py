"""
Evaluates a random chord progression and returns its evaluation.

Useful for checking the state of the evaluator.
"""

from pprint import pprint

from chord_progressions.chord import (
    serialize_chords,
    get_notes_list_from_midi_nums_str,
)
from chord_progressions.evaluator import (
    evaluate_chord,
    evaluate_progression,
    evaluate_notes_list,
)
from chord_progressions.solver import select_notes_list
from chord_progressions.type_templates import TYPE_TEMPLATES


def get_random_progression(n_segments):

    locks = "0" * n_segments

    chord_types, notes_list = select_notes_list(
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

    durations = ["1m"] * len(notes_list)

    chord_metrics = [evaluate_chord(c) for c in notes_list]

    return serialize_chords(notes_list, chord_types, durations, chord_metrics, locks)


if __name__ == "__main__":

    n_chords = 3

    progression = get_random_progression(n_chords)

    metrics = evaluate_progression(progression)

    pprint(metrics)

    """
        Without You I Am A Lie - Dustin O'Halloran
        chordi.co/ZMbw0YXO
    """
    midi_nums_str = "37-53-63_39-55-60-63_44-55-60-63-67_46-58-63-65-67"
    notes_list = get_notes_list_from_midi_nums_str(midi_nums_str)

    metrics = evaluate_notes_list(notes_list)

    # notes_list[0]
    # ["C#2", "F3", "D#4"]

    """
        Extension of whole-tone trichord experiments in scratch.md (chordi.co/-jYoWbMr)
        chordi.co/D5q5jb6V
    """
    midi_nums_str = "73-75-77_61-63-65_49-51-53_49-53-63_37-53-63_37-49-53-63-65-73-77_37-39-53_53-73-75_37-39-41-49-51-53-61-63-65-73-75-77"
    notes_list = get_notes_list_from_midi_nums_str(midi_nums_str)

    metrics = evaluate_notes_list(notes_list)
