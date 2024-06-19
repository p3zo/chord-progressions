# Chord Progressions

[![PyPI Latest Release](https://img.shields.io/pypi/v/chord-progressions.svg)](https://pypi.org/project/chord-progressions/)

A library for working with chord progressions.

## Installation

```
pip install chord-progressions
```

## Usage

See documentation at https://p3zo.github.io/chord-progressions/.

## Development

Configuration for local development with Docker is provided. Run `make build` to build the container, `make shell` to
get a shell inside of it for ad-hoc usage, and `make test` to run all unit tests inside the container. See
the [Makefile](Makefile) for all available actions.

To upgrade the version and trigger a new release, use `bump-my-version bump minor chord_progressions/__init__.py`.

The documentation uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) to build a static site from
Markdown files. Use `mkdocs serve` to start a live preview server of the site that automatically rebuilds upon saving. Build the site with `mkdocs build` and deploy with `mkdocs gh-deploy`.

### TODO

Analysis

- [feature] get key for progression
- [feature] get functional names for chords given key
- [feature] extend interval class vectors to "polychord content" vectors

I/O

- [maintainability] use a singular method of counting in `extract_harman.py`
    - `get_segment_label` uses counter
    - `get_segment_pc_weights` uses defaultdict
    - `MinimalSegment.get_pitch_class_weights` uses list.count()
- [performance] `extract.midi_harman.segment_and_label()` is slow for many consecutive segments. test that a
  maximum of six segment evaluations occur per note

Misc

- [feature] Generalize `noteNumberToFrequency` to use any periodic tuning (see https://github.com/soul-lang/SOUL/pull/26/files)
- [feature] implement `is_partial_circular_match`, `chord_contained_in_type`, and `get_possible_types_of_chord`
- [maintainability] mk `pitch_class` refer to "C" and call 0 `pitch_class_ix`
- [maintainability] pass midi note numbers everywhere as "notes" and include note names as "noteNames"
- [maintainability] test the merging of chord types
- [maintainability] github action to build & deploy docs
