# Glossary

Names used for arguments and values throughout the library.

| Name             | Type            | Meaning                                                         | Example                                |
|------------------|-----------------|-----------------------------------------------------------------|----------------------------------------|
| `midi_num`       | int             | a MIDI note number, 0 to 127; 60 is middle C                    | `60`                                   |
| `note`           | str             | a note name with an octave, using sharps                        | `"C4"`                                 |
| `note_name`      | str             | a note name without its octave                                  | `"C"`                                  |
| `octave`         | int             | the octave of a note; `C4` starts octave 4                      | `4`                                    |
| `pitch_class`    | int             | a note name as a number, 0 (C) to 11 (B)                        | `0`                                    |
| `midi_nums`      | list[int]       | the notes of one chord                                          | `[60, 48]`                             |
| `notes`          | list[str]       | the notes of one chord                                          | `["C4", "C3"]`                         |
| `midi_nums_str`  | str             | `midi_nums` joined by `-`; chords joined by `_`                 | `"60-48"`, `"60-48_62-52"`             |
| `note_str`       | str             | `notes` joined by `-`; chords joined by `_`                     | `"C4-C3"`, `"C4-C3_D4-E3"`             |
| `midi_nums_list` | list[list[int]] | the notes of several chords                                     | `[[60, 48], [62, 52]]`                 |
| `notes_list`     | list[list[str]] | the notes of several chords                                     | `[["C4", "C3"], ["D4", "E3"]]`         |
| `chord_type`     | str             | the name of a chord type; `""` when none fits                   | `"major chord"`                        |
| `type_num`       | int             | a chord type's position in `TYPE_TEMPLATES`                     | `63`                                   |
| `type_id`        | int             | same as `type_num`; called `typeId` on chords                   | `63`                                   |
| `type_num_str`   | str             | `type_num`s joined by `_`                                       | `"63_59"`                              |
| `chord_types`    | list[str]       | the chord types of several chords                               | `["major chord", "minor chord"]`       |
| `duration`       | str             | a chord's length in [Tone.js time notation](progressions.md#durations) | `"1m"`                          |
| `durations`      | list[str]       | the durations of several chords                                 | `["1m", "2n", "2n"]`                   |
| `duration_str`   | str             | `durations` joined by `_`                                       | `"1m_2n_2n"`                           |
| `beats`          | list[float]     | chord lengths in quarter-note beats                             | `[4, 2, 2]`                            |
| `template`       | list[int]       | which of the 12 pitch classes, starting at C, a chord contains  | `[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]` |
| `template_str`   | str             | a `template` as a string                                        | `"100010010000"`                       |
| `rotation`       | list[int]       | a `template` transposed by some number of semitones             | `[0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]` |
| `freq`           | float           | a frequency in hertz                                            | `440.0`                                |
| `voicing`        | list[int]       | a chord's notes in a particular register, as MIDI numbers       | `[48, 64, 67]`                         |
| `chord`          | Chord           | a set of unique notes; see [Chords](chords.md)                  |                                        |
| `progression`    | Progression     | a sequence of chords with durations; see [Progressions](progressions.md) |                               |
