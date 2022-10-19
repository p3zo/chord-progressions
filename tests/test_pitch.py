import pytest
from chord_progressions.pitch import (
    MIDI_NOTE_FREQUENCIES,
    MIDI_NOTES,
    create_notes_freqs_table,
    get_freq_from_note,
    get_midi_num_from_note,
    get_midi_nums_list_from_midi_nums_str,
    get_n_overtones_harmonic,
    get_note_from_midi_num,
    get_note_list,
    get_note_name_from_note,
    get_octave_from_note,
    get_pitch_class_from_note,
)

EXPECTATIONS = [
    {
        "note": "A#5",
        "name": "A#",
        "octave": 5,
        "midi_num": 82,
        "pitch_class": 10,
        "freq": 932.33,
    },
    {
        "note": "A4",
        "name": "A",
        "octave": 4,
        "midi_num": 69,
        "pitch_class": 9,
        "freq": 440.0,
    },
    {
        "note": "C-1",
        "name": "C",
        "octave": -1,
        "midi_num": 0,
        "pitch_class": 0,
        "freq": 8.18,
    },
    {
        "note": "G9",
        "name": "G",
        "octave": 9,
        "midi_num": 127,
        "pitch_class": 7,
        "freq": 12543.85,
    },
]


def test_get_note_list():

    start = 21
    end = 108

    notes = get_note_list(start, end)

    assert len(notes) == 88


def test_get_note_name_from_note():

    for ex in EXPECTATIONS:
        assert get_note_name_from_note(ex["note"]) == ex["name"]


def test_get_midi_num_from_note():

    for ex in EXPECTATIONS:
        assert get_midi_num_from_note(ex["note"]) == ex["midi_num"]

    with pytest.raises(ValueError):
        get_midi_num_from_note("L5")


def test_get_pitch_class_from_note():

    for ex in EXPECTATIONS:
        assert get_pitch_class_from_note(ex["note"]) == ex["pitch_class"]


def test_get_octave_from_note():
    for ex in EXPECTATIONS:
        assert get_octave_from_note(ex["note"]) == ex["octave"]


def test_get_note_from_midi_num():
    for ex in EXPECTATIONS:
        assert get_note_from_midi_num(ex["midi_num"]) == ex["note"]


def test_get_freq_from_note():
    for ex in EXPECTATIONS:
        assert get_freq_from_note(ex["note"]) == ex["freq"]


def test_create_notes_freqs_table():
    note_freqs = create_notes_freqs_table()

    assert list(note_freqs) == MIDI_NOTES
    assert list(note_freqs.values()) == MIDI_NOTE_FREQUENCIES


def test_get_midi_nums_list_from_midi_nums_str():
    expectations = [
        {"midi_nums_str": "60-48_62-50", "midi_nums_list": [[60, 48], [62, 50]]},
        {"midi_nums_str": "60-48_", "midi_nums_list": [[60, 48]]},
        {"midi_nums_str": "60-48_a", "midi_nums_list": [[60, 48]]},
    ]
    for ex in expectations:
        assert (
            get_midi_nums_list_from_midi_nums_str(ex["midi_nums_str"])
            == ex["midi_nums_list"]
        )


def test_get_n_overtones_harmonic():
    assert get_n_overtones_harmonic(440, 4) == [440, 880, 1320, 1760, 2200]
