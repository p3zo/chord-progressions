"""
    A common heuristic is that an interval is consonant when the
    ratio between the frequencies is simple.

    TODO: understand https://en.xen.wiki/w/Harmonic_Entropy

    Resonance


    Brilliance

        "for maximum brilliance let the lower tones [be somehow equally spaced out as] their overtones"
"""

import itertools
from pprint import pprint

import numpy as np

from chord_progressions.audio import get_n_overtones_harmonic
from chord_progressions.chord import (
    get_chords_from_chord_string,
    get_template_from_notes,
    get_type_from_chord,
    get_type_num_from_type,
    serialize_chords,
)
from chord_progressions.type_templates import TYPE_TEMPLATES
from chord_progressions.pitch import (
    get_freq_from_note,
    get_midi_num_from_note,
    get_pitch_class_from_note,
)
from chord_progressions.solver import select_chords

# created in `create_chord_classes.py`
# TODO: replace this table with a formula
MIN_MAX_EVENNESS_BY_CARDINALITY = [
    [0.0, 0.0],
    [0.5176380902050415, 2.0],
    [2.035276180410083, 5.196152422706632],
    [6.1815405503520555, 9.65685424949238],
    [9.631030293135233, 15.287884542627612],
    [16.226784405860382, 22.392304845413264],
    [24.822538518585535, 30.479392768077915],
    [35.350144283888824, 40.03987070039298],
    [47.609800856760984, 50.77067709905754],
    [61.28367099200624, 62.7660329018012],
    [75.9575411272515, 75.9575411272515],
    [91.14904935270181, 91.14904935270181],
]


def get_interval_class_vector(chord):
    """
    The interval classes designated by each digit ascend from left to right, i.e.

        minor seconds / major sevenths (1 or 11 semitones)
        major seconds / minor sevenths (2 or 10 semitones)
        minor thirds / major sixths (3 or 9 semitones)
        major thirds / minor sixths (4 or 8 semitones)
        perfect fourths / perfect fifths (5 or 7 semitones)
        tritones (6 semitones)
    """
    vec = [0] * 6

    template = get_template_from_notes(chord)

    one_indices = [ix for ix, i in enumerate(template) if i == 1]
    pairs = list(itertools.combinations(one_indices, 2))

    intervals = [p[1] - p[0] for p in pairs]

    modded = [12 - i if i > 6 else i for i in intervals]

    for i in range(6):
        vec[i] = modded.count(i + 1)

    return vec


def get_evenness(interval_class_vector):
    """
    A rough measure of acoustic consonance.
    Highly consonant chords divide the octave nearly evenly.

    Note that acoustic consonance implies near-evenness, but not the reverse.

    For background on the equation see https://www.researchgate.net/profile/Jack_Douthett/publication/249881698_Vector_Products_and_Intervallic_Weighting/links/575061d708ae1c34b39aaa1b.pdf
    """
    weight_vector = [0] * 6

    for i in range(6):

        k = i + 1

        weight_vector[i] += 2 * np.sin(k * np.pi / 12)

    weight = np.dot(weight_vector, interval_class_vector)

    return weight


def get_relative_evenness(evenness, cardinality):
    """
    Calculate the evenness of a pcset relative to its possible range
    because highly-even dyads will have a lower evenness than highly uneven hexachords.

    The result is a value between 0 and 1.
    """

    emin, emax = MIN_MAX_EVENNESS_BY_CARDINALITY[cardinality - 1]

    return (evenness - emin) / (emax - emin)


def get_overtone_agreement(notes):

    freqs = [get_freq_from_note(n) for n in notes]

    all_partials = []

    n_overtones = 10
    for f in freqs:
        all_partials.extend(get_n_overtones_harmonic(f, n_overtones))

    sorted_partials = sorted(all_partials)

    sum_of_differences = 0

    for i in range(1, len(sorted_partials)):
        diff = sorted_partials[i] - sorted_partials[i - 1]
        sum_of_differences += diff

    return sum_of_differences


def evaluate_chord(notes):
    """list of notes, e.g. ['F2', 'B2', 'D3', 'G#3']"""

    metrics = {}

    interval_class_vector = get_interval_class_vector(notes)

    # overtone_agreement = get_overtone_agreement(notes)

    # evenness = get_evenness(interval_class_vector)

    pc_cardinality = len(set([get_pitch_class_from_note(n) for n in notes]))
    assert pc_cardinality <= 12, "Pitch class cardinality > 12"

    chord_type = get_type_from_chord(notes)

    metrics["type_id"] = get_type_num_from_type(chord_type)
    metrics["type_name"] = chord_type
    metrics["num_notes"] = len(notes)
    metrics["num_pitches"] = len(set(notes))
    metrics["pc_cardinality"] = pc_cardinality
    metrics["interval_class_vector"] = interval_class_vector
    # metrics["evenness"] = evenness
    # metrics["relative_evenness"] = get_relative_evenness(evenness, cardinality)
    metrics["ambitus"] = get_ambitus(notes)
    # metrics["overtone_agreement"] = overtone_agreement

    return metrics


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


def get_macroharmony(progression):
    """The total collection of notes"""

    notes = set()

    for chord in progression:
        for note in chord:
            notes.add(note)

    return notes


def get_ambitus(macroharmony):
    """
    Ambitus, int, # semitones between the lowest and highest note
    """
    midi_notes = [get_midi_num_from_note(n) for n in macroharmony]

    return max(midi_notes) - min(midi_notes)


def evaluate_progression(progression, serialized=False):

    if serialized:
        progression = [chord["notes"] for chord in progression]

    metrics = {}

    macroharmony = get_macroharmony(progression)

    metrics["ambitus"] = get_ambitus(macroharmony)

    metrics["density"] = len(macroharmony) / len(progression)

    return metrics


def get_ofreqs_for_notes(notes):

    freqs = [get_freq_from_note(n) for n in notes]
    ofreqs = [get_n_overtones_harmonic(f, n_overtones) for f in freqs]

    return ofreqs


if __name__ == "__main__":

    notesA = ["C1", "D1", "E1"]

    notesB = ["C5", "D5", "E5"]

    freqsA = [get_freq_from_note(n) for n in notesA]

    freqsB = [get_freq_from_note(n) for n in notesB]

    n_overtones = 10

    ofreqsA = [get_n_overtones_harmonic(f, n_overtones) for f in freqsA]

    ofreqsB = [get_n_overtones_harmonic(f, n_overtones) for f in freqsB]

    """
        Random progression
    """
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
