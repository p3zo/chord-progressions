# Chord progressions

Functions for generating and evaluating chord progressions.

## Definitions

`midi_num`: str, "60"
`note`: str, "C4"
`note_name`: str, "C"
`octave`: int, 4
`pitch_class`: int, 0

`midi_nums`: list[int], [60, 48]
`notes`: list[str], ["C4", "C3"]

`midi_num_str`: str, "60-48" or "60-48_62-52"
`note_str`: str, "C4-C3" or "C4-C3_D4-E3"

`midi_nums_list`: list[list[int]], [[60, 48], [62, 52]]
`notes_list`: list[list[str]], [["C4", "C3"], ["D4", "E3"]]

`chord_type`: str, "unison"
`type_num`: int, 1 (todo: add chord* prefix)
`type_id`: int, `type_num` (todo: use only one and add chord* prefix)

`type_num_str`: 1*1 (todo: use only this or type_id_str and add chord* prefix)
`chord_types`: [ "unison", "unison" ]

`duration`: "1m"
`durations`: ["1m", "1m", "1m", "1m"]
`duration_str`: "1m_1m_1m_1m"

`template`: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
`template_str`: '101010101010'

`freq`: 440.0

`chord_index`: 1

`id`: aaaa_bbbb_cccc_dddd

`locks`: str, 00100 (todo: rename to lock_str)

`chord`: {
    "id": `id`,
    "ix": `chord_index`,
    "type": `chord_type`,
    "duration": `duration`,
    "typeId": `type_id`,
    "notes": `notes`,
    "locked": `lock_str`,
    "metrics": `chord_metrics`,
}


`template`: An array of pitch classes in type_templates.
`rotation`: A template transposed by any number of steps.
`voicing`: An array of pitches.

## Usage

See the [Makefile](Makefile) for available actions.

## TODO

-   go alll the way through pitch/chord modules and make `note` and `midi_num` consistent.

##### Tonal evaluation

-   get key for progression
-   get function chord name given key

##### Eventually

-   [feature] output variable chord durations from solver
-   [feature] consider lower and upper structures in select_voicing
-   [feature] add the possibility of a repeated note in a different octave
-   [feature] Generalize `noteNumberToFrequency` to use any periodic tuning https://github.com/soul-lang/SOUL/pull/26/files
-   [feature] use VAE as solver

-   [maintainability] break out the merging of chord types into a function and test it
-   [maintainability] pass midi note numbers everywhere as "notes" and include note names as "noteNames"

##### Maybe

-   [feature] extend interval class vectors to "polychord-content" vectors
-   [feature] `chord_contained_in_type` function
-   [feature] download midi files from Geocities MIDI archive on the Internet Archive & parse into progressions. find the zip of 100k midi files used by bitmidi.com
