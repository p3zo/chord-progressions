# Chord progressions

## Usage

See the [Makefile](Makefile) for available actions.

## Docs

The documentation uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) to build a static site from
Markdown files. Use `mkdocs serve` to start a live preview server of the site that automatically rebuilds upon saving.
Use `mkdocs build` to build the site.

## TODO

- [bug] `extract.midi_harman.segment_and_label()` gets really slow for many consecutive segments. test that a maximum of
  six segment evaluations occur per note

- [feature] define __getitem__ for progressions to select e.g. the first chord using progression[0]
- [feature] allow Progressions to be initialized `from_audio` and `from_midi` via extraction from a filepath
- [feature] mk progressions from extracted harman labels
- [feature] get key for progression
- [feature] get functional names for chords given key
- [feature] output variable chord durations from solver
- [feature] consider lower and upper structures in select_voicing
- [feature] add the possibility of a repeated note in a different octave
- [feature] Generalize `noteNumberToFrequency` to use any periodic
  tuning https://github.com/soul-lang/SOUL/pull/26/files
- [feature] use VAE as solver
- [feature] implement `is_partial_circular_match`, `chord_contained_in_type`, and `get_possible_types_of_chord`
- [feature] `io.midi.get_midi_from_progression` needs an `offset` param for when the first chord isn't at 0
- [feature] use `bars:beats:sixteenths` format for progression duration

- [maintainability] mk `pitch_class` refer to "C" and call 0 `pitch_class_ix`
- [maintainability] use a singular method of counting in `extract_harman.py`
    - `get_segment_label` uses counter
    - `get_segment_pc_weights` uses defaultdict
    - `MinimalSegment.get_pitch_class_weights` uses list.count()
- [maintainability] break out the merging of chord types into a function and test it
- [maintainability] pass midi note numbers everywhere as "notes" and include note names as "noteNames"
- [maintainability] break `select_notes_list` apart into smaller functions

##### Maybe

- [feature] extend interval class vectors to "polychord-content" vectors
- [feature] `chord_contained_in_type` function
