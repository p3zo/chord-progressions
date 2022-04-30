"""
Evaluates a random chord progression and returns its evaluation.

Useful for checking the state of the evaluator.
"""

from chord_progressions.chord import get_notes_list_from_midi_nums_str, serialize_chords
from chord_progressions.evaluator import evaluate_notes_list, evaluate_progression
from chord_progressions.solver import select_notes_list
from chord_progressions.type_templates import TYPE_TEMPLATES


def get_random_progression(n_segments):

    locks = "0" * n_segments

    notes_list, chord_types = select_notes_list(
        n_segments=n_segments,
        pct_notes_common=0,
        note_range_low=60,
        note_range_high=108,
        allowed_chord_types=list(TYPE_TEMPLATES),
        existing_notes_list=None,
        existing_types=None,
        locks=locks,
        adding=False,
        first_chord=None,
    )

    durations = ["1m"] * len(notes_list)

    chord_metrics = [evaluate_notes_list(c) for c in notes_list]

    return serialize_chords(notes_list, chord_types, durations, chord_metrics, locks)


def evaluate_sample_progression():
    # Without You I Am A Lie - Dustin O'Halloran
    # chordi.co/ZMbw0YXO

    midi_nums_str = "37-53-63_39-55-60-63_44-55-60-63-67_46-58-63-65-67"
    notes_list = get_notes_list_from_midi_nums_str(midi_nums_str)

    return evaluate_notes_list(notes_list)


def evaluate_sample_progression_2():
    # Extension of whole-tone trichord experiments in scratch.md (chordi.co/-jYoWbMr)
    # chordi.co/D5q5jb6V

    midi_nums_str = "73-75-77_61-63-65_49-51-53_49-53-63_37-53-63_37-49-53-63-65-73-77_37-39-53_53-73-75_37-39-41-49-51-53-61-63-65-73-75-77"
    notes_list = get_notes_list_from_midi_nums_str(midi_nums_str)

    return evaluate_notes_list(notes_list)


if __name__ == "__main__":

    sample_metrics_1 = evaluate_sample_progression()
    sample_metrics_2 = evaluate_sample_progression_2()

    random_metrics = []
    for i in range(10000):
        progression = get_random_progression(n_segments=3)
        random_metrics.append(evaluate_progression(progression))
