from chord_progressions.type_templates import (
    TYPE_TEMPLATES,
    get_template_from_notes,
    get_template_from_pitch_classes,
    get_template_from_midi_nums,
    get_template_from_template_str,
    get_type_from_type_num,
    get_types_from_type_num_str,
    get_type_num_from_type,
    notes_match_chord_type,
    get_type_from_notes,
    get_type_from_midi_nums,
)


def test_type_templates_format():
    assert type(TYPE_TEMPLATES) == dict


def test_get_template_from_pitch_classes():
    assert get_template_from_pitch_classes([0, 4, 7]) == [
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
    ]


def test_get_template_from_midi_nums():
    assert get_template_from_midi_nums([48, 60]) == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def test_get_template_from_template_str():
    template = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    assert get_template_from_template_str("101010101010") == template


def test_get_type_from_type_num():
    assert get_type_from_type_num(63) == "major chord"


def test_get_types_from_type_num_str():
    assert get_types_from_type_num_str("59_63") == ["minor chord", "major chord"]


def test_get_type_num_from_type():
    assert get_type_num_from_type("major chord") == 63


def test_notes_match_chord_type():
    assert notes_match_chord_type(["C4", "E4", "G4"], "major chord")


def test_get_type_from_notes():
    assert get_type_from_notes(["C4", "C3"]) == "unison"


def test_get_type_from_midi_nums():
    assert get_type_from_midi_nums([48, 60]) == "unison"


def test_get_template_from_notes():
    expectations = [
        {
            "notes": ["C-1", "A4", "G9"],
            "template": [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        },
        {"notes": ["C4", "E4", "G4"], "template": [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]},
    ]
    for ex in expectations:
        assert get_template_from_notes(ex["notes"]) == ex["template"]
