"""
    Defines the metrics computed for every progression.

    TODO:
        - A common heuristic is that an interval is consonant when the ratio between the frequencies is simple.
        - Resonance
        - Brilliance: "for maximum brilliance let the lower tones [be somehow equally spaced out as] their overtones"
            - Vincent Persechetti, Twentieth-Century Harmony
        - something like https://en.xen.wiki/w/Harmonic_Entropy
"""

import itertools

import numpy as np
from chord_progressions.pitch import (
    get_freq_from_note,
    get_midi_num_from_note,
    get_n_overtones_harmonic,
    get_pitch_class_from_note,
)
from chord_progressions.type_templates import get_template_from_notes


def get_interval_class_vector(notes):
    """
    Returns a vector of interval classes.
        0: minor second / major seventh (1 or 11 semitones)
        1: major second / minor seventh (2 or 10 semitones)
        2: minor third / major sixth (3 or 9 semitones)
        3: major third / minor sixth (4 or 8 semitones)
        4: perfect fourth / perfect fifth (5 or 7 semitones)
        5: tritone (6 semitones)
    """
    vec = [0] * 6

    template = get_template_from_notes(notes)
    one_indices = [ix for ix, i in enumerate(template) if i == 1]
    pairs = list(itertools.combinations(one_indices, 2))

    intervals = [p[1] - p[0] for p in pairs]

    modded = [12 - i if i > 6 else i for i in intervals]

    for i in range(6):
        vec[i] = modded.count(i + 1)

    return vec


def get_evenness(interval_class_vector):
    """
    A rough measure of acoustic consonance. Highly consonant chords divide the octave nearly evenly.
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
    Calculate the evenness of a pitch class set relative to its possible range.
    A relative value is useful because highly-even dyads will have a lower evenness than highly uneven hexachords.
    The result is a value between 0 and 1.
    """
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


def evaluate_notes(notes):
    """list of notes, e.g. ["C4", "E4", "G4"]"""

    metrics = {}

    interval_class_vector = get_interval_class_vector(notes)

    # evenness = get_evenness(interval_class_vector)

    pc_cardinality = len(set([get_pitch_class_from_note(n) for n in notes]))
    assert pc_cardinality <= 12, "Pitch class cardinality > 12"

    metrics["num_notes"] = len(notes)
    metrics["num_pitches"] = len(set(notes))
    # metrics["pc_cardinality"] = pc_cardinality
    metrics["interval_class_vector"] = interval_class_vector
    # metrics["ambitus"] = get_ambitus(notes)
    # metrics["evenness"] = evenness
    # metrics["relative_evenness"] = get_relative_evenness(evenness, pc_cardinality)
    # metrics["overtone_agreement"] = get_overtone_agreement(notes)

    return metrics


def get_macroharmony(progression):
    """The total collection of notes"""

    collection = set()

    for notes in progression:
        for note in notes:
            collection.add(note)

    return collection


def get_ambitus(macroharmony):
    """Ambitus, int, # semitones between the lowest and highest note"""
    midi_notes = [get_midi_num_from_note(n) for n in macroharmony]

    return max(midi_notes) - min(midi_notes)


def evaluate_progression(progression):
    metrics = {}

    # macroharmony = get_macroharmony(notes_list)

    # metrics["ambitus"] = get_ambitus(macroharmony)

    # metrics["density"] = len(macroharmony) / len(notes_list)

    return metrics


def get_n_overtones_for_notes(notes, n):
    """Calculates `n` overtone frequencies for each note in `notes`"""

    freqs = [get_freq_from_note(n) for n in notes]
    ofreqs = [get_n_overtones_harmonic(f, n) for f in freqs]

    return ofreqs
