# Notes and chord types

## Notes

Notes are named with a sharp and an octave, from `C-1` (MIDI 0) to `G9` (MIDI 127), with middle C as `C4`.
Flats are not used.

```python
from chord_progressions.pitch import (
    get_freq_from_note,
    get_midi_num_from_note,
    get_note_from_midi_num,
    get_note_list,
    get_note_name_from_note,
    get_octave_from_note,
    get_pitch_class_from_note,
)

get_midi_num_from_note("C4")      # 60
get_note_from_midi_num(61)        # 'C#4'
get_pitch_class_from_note("A#4")  # 10
get_note_name_from_note("A#4")    # 'A#'
get_octave_from_note("A#4")       # 4
get_freq_from_note("A4")          # 440.0
get_note_list(60, 64)             # ['C4', 'C#4', 'D4', 'D#4', 'E4']
```

`get_pitch_class_from_midi_num` and `get_freq_from_midi_num` take MIDI numbers instead.

### Chords and progressions as strings

A chord can be written as its MIDI numbers joined by `-`, and a progression as its chords joined by `_`.

```python
from chord_progressions.pitch import (
    get_midi_nums_list_from_midi_nums_str,
    get_notes_from_midi_nums_str,
    get_notes_list_from_midi_nums_str,
)

get_notes_from_midi_nums_str("60-64-67")                # ['C4', 'E4', 'G4']
get_notes_list_from_midi_nums_str("60-64-67_62-65-69")  # [['C4', 'E4', 'G4'], ['D4', 'F4', 'A4']]
get_midi_nums_list_from_midi_nums_str("60-64-67_62-65-69")
# [[60, 64, 67], [62, 65, 69]]
```

## Chord types

Every chord is named by the pitch classes it contains, regardless of octave or inversion, using
[Vladimir Ladma's list][ladma] of 191 types. A chord that fits none of them has the type `""`.

`TYPE_TEMPLATES` maps each type name to its template: 12 characters, one per pitch class starting at C, `1` where
the type has a note. Templates are written with their lowest note on C; a chord matches a type in any
transposition. A type's id (`typeId`, or `type_num`) is its position in `TYPE_TEMPLATES`.

```python
from chord_progressions import TYPE_TEMPLATES
from chord_progressions.type_templates import (
    get_template_from_pitch_classes,
    get_type_from_midi_nums,
    get_type_from_notes,
    get_type_from_type_num,
    get_type_num_from_type,
    get_types_from_type_num_str,
    notes_match_chord_type,
)

TYPE_TEMPLATES["major chord"]         # '100010010000'
get_type_from_notes(["C4", "E4", "G4"])  # 'major chord'
get_type_from_midi_nums([62, 66, 69])    # 'major chord'
get_type_num_from_type("major chord")    # 63
get_type_from_type_num(63)               # 'major chord'
get_types_from_type_num_str("63_59")     # ['major chord', 'minor chord']
notes_match_chord_type(["D4", "F#4", "A4"], "major chord")  # True
get_template_from_pitch_classes([0, 4, 7])
# [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
```

`get_template_from_midi_nums`, `get_template_from_notes` and `get_template_from_template_str` build templates
from other inputs, and `get_type_from_template` names one.

[ladma]: https://web.archive.org/web/20221116234056/https://vladimir_ladma.sweb.cz/english/music/structs/mus_rot.htm
