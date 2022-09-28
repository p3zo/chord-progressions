# Glossary

Terms used in the code

| Name                             | Type            | Description                                  | Example                              |
|----------------------------------|-----------------|----------------------------------------------|--------------------------------------|
| midi_num                         | str             |                                              | 60                                   |
| note                             | str             |                                              | C4                                   |
| note_name                        | str             |                                              | C                                    |
| octave                           | int             |                                              | 4                                    |
| pitch_class                      | int             |                                              | 0                                    |
| midi_nums                        | list[int]       |                                              | [60, 48]                             |
| notes                            | list[str]       |                                              | [C4, C3]                             |
| midi_nums_str                    | str             |                                              | 60-48 or 60-48_62-52                 |
| note_str                         | str             |                                              | C4-C3 or C4-C3_D4-E3                 |
| midi_nums_list                   | list[list[int]] |                                              | [[60, 48], [62, 52]]                 |
| notes_list                       | list[list[str]] |                                              | [[C4, C3], [D4, E3]]                 |
| chord_type                       | str             |                                              | unison                               |
| type_num                         | int             |                                              | 1                                    |
| type_id                          | int             | Same as `type_num`                           |                                      |
| type_num_str                     | str             |                                              | 1\*1                                 |
| chord_types                      | list[str]       |                                              | [ unison, unison ]                   |
| duration                         | str             |                                              | 1m                                   |
| durations                        | list[str]       |                                              | [1m, 1m, 1m, 1m]                     |
| duration_str                     | str             |                                              | 1m_1m_1m_1m                          |
| template                         | list[int]       | An array of 12 pitch classes starting at C   | [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0] |
| template_str                     | str             |                                              | 101010101010                         |
| rotation                         | list[int]       | A template transposed by any number of steps |                                      |
| freq                             | float           |                                              | 440.0                                |
| locks (todo: rename to lock_str) | str             |                                              | 00100                                |
| voicing                          | list[str]       | A notes_list                                 |                                      |
| chord                            | Chord           |                                              |                                      |
| progression                      | Progression     |                                              |                                      |

[//]: # (TODO add `chord_` prefix to `type_*` terms)
