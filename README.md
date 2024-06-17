# Chord progressions

`chord-progressions` provides utility functions for extracting, analyzing, and generating chord progressions.

It can be installed from PyPI:

```
pip install chord-progressions
```

See documentation at https://p3zo.github.io/chord-progressions/.

## Development

Configuration for local development with Docker is provided. Run `make build` to build the container, `make shell` to
get a shell inside of it for ad-hoc usage, and `make test` to run all unit tests inside the container. See
the [Makefile](Makefile) for all available actions.

To upgrade the version and trigger a new release, use `bump-my-version bump minor chord_progressions/__init__.py`.

## Docs

The documentation uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) to build a static site from
Markdown files. Use `mkdocs serve` to start a live preview server of the site that automatically rebuilds upon saving.
Use `mkdocs build` to build the site.

## TODO

Analysis

- [feature] get key for progression
- [feature] get functional names for chords given key
- [feature] extend interval class vectors to "polychord content" vectors

I/O

- [feature] add `from_audio` and `from_midi` constructors to Progression class to enable
  e.g. `progression = chord_progressions.Progression.from_midi('my_file.mid')`
- [maintainability] use a singular method of counting in `extract_harman.py`
    - `get_segment_label` uses counter
    - `get_segment_pc_weights` uses defaultdict
    - `MinimalSegment.get_pitch_class_weights` uses list.count()
- [performance] `extract.midi_harman.segment_and_label()` gets really slow for many consecutive segments. test that a
  maximum of six segment evaluations occur per note

Generation

- [feature] VAE solver
- [feature] use variable chord durations
- [feature] consider lower and upper structures in select_voicing
- [feature] add the possibility of repeated notes in different octaves
- [feature] ability to constrain key

Misc

- [feature] Host docs site
- [feature] Generalize `noteNumberToFrequency` to use any periodic
  tuning (see https://github.com/soul-lang/SOUL/pull/26/files)
- [feature] implement `is_partial_circular_match`, `chord_contained_in_type`, and `get_possible_types_of_chord`
- [maintainability] mk `pitch_class` refer to "C" and call 0 `pitch_class_ix`
- [maintainability] pass midi note numbers everywhere as "notes" and include note names as "noteNames"
- [maintainability] test the merging of chord types
