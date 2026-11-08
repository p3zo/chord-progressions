from chord_progressions.type_templates import (
    TYPE_TEMPLATES,
    get_template_from_midi_nums,
    get_template_from_notes,
    get_template_from_pitch_classes,
    get_template_from_template_str,
    get_type_from_midi_nums,
    get_type_from_notes,
    get_type_from_type_num,
    get_type_num_from_type,
    get_types_from_type_num_str,
    notes_match_chord_type,
)
from chord_progressions.utils import is_circular_match


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


def test_each_set_class_has_a_single_type():
    # Names that share a set class are merged into one entry, e.g. "rite chord 2|tritone-fourth 1".
    # get_type_from_template returns the first match, so a second entry would never be found.
    types = [
        (chord_type, get_template_from_template_str(template_str))
        for chord_type, template_str in TYPE_TEMPLATES.items()
        if template_str
    ]
    duplicates = [
        (type_1, type_2)
        for ix, (type_1, template_1) in enumerate(types)
        for type_2, template_2 in types[ix + 1 :]
        if is_circular_match(template_1, template_2)
    ]
    assert duplicates == []
