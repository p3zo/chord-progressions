# Chord progressions

A toolkit for extracting, generating and analyzing symbolic chord progressions

## Usage

See the [Makefile](Makefile) for available actions.

## TODO

-   make `note` and `midi_num` consistent throughout all modules

##### Prioritized

-   `extract_harman.segment_and_label()` gets really slow for many consecutive segments. test that a maxiumum of six segment evaluations occur per note

##### Eventually

-   [feature] get key for progression
-   [feature] get functional names for chords given key
-   [feature] output variable chord durations from solver
-   [feature] consider lower and upper structures in select_voicing
-   [feature] add the possibility of a repeated note in a different octave
-   [feature] Generalize `noteNumberToFrequency` to use any periodic tuning https://github.com/soul-lang/SOUL/pull/26/files
-   [feature] use VAE as solver
-   [feature] implement `is_partial_circular_match`, `chord_contained_in_type`, and `get_possible_types_of_chord`
-   [feature] make_midi_progression needs an `offset` param for when the first chord isn't at 0
-   [feature] use `bars:beats:sixteenths` format for progression duration

-   [maintainability] use a singular method of counting in `extract_harman.py`
    -   `get_segment_label` uses counter
    -   `get_segment_pc_weights` uses defaultdict
    -   `MinimalSegment.get_pitch_class_weights` uses list.count()
-   [maintainability] break out the merging of chord types into a function and test it
-   [maintainability] pass midi note numbers everywhere as "notes" and include note names as "noteNames"
-   [maintainability] break `select_notes_list` apart into smaller functions

##### Maybe

-   [feature] extend interval class vectors to "polychord-content" vectors
-   [feature] `chord_contained_in_type` function

## Definitions

Below are the names used by this library.

| Name                             | Type            | Description                                                  | Example                                                                                                                                                                  |
| -------------------------------- | --------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| midi_num                         | str             |                                                              | "60"                                                                                                                                                                     |
| note                             | str             |                                                              | "C4"                                                                                                                                                                     |
| note_name                        | str             |                                                              | "C"                                                                                                                                                                      |
| octave                           | int             |                                                              | 4                                                                                                                                                                        |
| pitch_class                      | int             |                                                              | 0                                                                                                                                                                        |
| midi_nums                        | list[int]       |                                                              | [60, 48]                                                                                                                                                                 |
| notes                            | list[str]       |                                                              | ["C4", "C3"]                                                                                                                                                             |
| midi_nums_str                    | str             |                                                              | "60-48" or "60-48_62-52"                                                                                                                                                 |
| note_str                         | str             |                                                              | "C4-C3" or "C4-C3_D4-E3"                                                                                                                                                 |
| midi_nums_list                   | list[list[int]] |                                                              | [[60, 48], [62, 52]]                                                                                                                                                     |
| notes_list                       | list[list[str]] |                                                              | [["C4", "C3"], ["D4", "E3"]]                                                                                                                                             |
| chord_type                       | str             |                                                              | "unison"                                                                                                                                                                 |
| type_num                         | int             | (todo: add chord prefix)                                     | 1                                                                                                                                                                        |
| type_id                          | int             | same as `type_num` (todo: use only one and add chord prefix) |                                                                                                                                                                          |
| type_num_str                     | str             | (todo: use only this or type_id_str and add chord\* prefix)  | 1\*1                                                                                                                                                                     |
| chord_types                      | list[str]       |                                                              | [ "unison", "unison" ]                                                                                                                                                   |
| duration                         | str             |                                                              | "1m"                                                                                                                                                                     |
| durations                        | list[str]       |                                                              | ["1m", "1m", "1m", "1m"]                                                                                                                                                 |
| duration_str                     | str             |                                                              | "1m_1m_1m_1m"                                                                                                                                                            |
| template                         | list[int]       | n array of pitch classes in type_templates                   | [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]                                                                                                                                     |
| template_str                     | str             |                                                              | '101010101010'                                                                                                                                                           |
| freq                             | float           |                                                              | 440.0                                                                                                                                                                    |
| chord_index                      | int             | the chord's position in a progression                        |                                                                                                                                                                          |
| id                               | str             | a random uuid assigned to the chord                          | aaaa_bbbb_cccc_dddd                                                                                                                                                      |
| locks (todo: rename to lock_str) | str             |                                                              | 00100                                                                                                                                                                    |
| chord                            | dict            |                                                              | {"id": `id`, "ix": `chord_index`, "type": `chord_type`, "duration": `duration`, "typeId": `type_id`, "notes": `notes`, "locked": `lock_str`, "metrics": `chord_metrics`} |
| progression                      | list[`chord`]   |                                                              |                                                                                                                                                                          |
| rotation                         | list[int]       | A template transposed by any number of steps                 |                                                                                                                                                                          |
| voicing                          | list[str]       | a notes_list                                                 |                                                                                                                                                                          |
