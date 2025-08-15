# Chord Progressions

[![PyPI Latest Release](https://img.shields.io/pypi/v/chord-progressions.svg)](https://pypi.org/project/chord-progressions/)

A library for working with chord progressions.

## Installation

```
pip install chord-progressions
```

## Usage

See documentation at https://p3zo.github.io/chord-progressions.

## Development

Configuration for local development with Docker is provided. Run `make build` to build the container, `make shell` to
get a shell inside of it for ad-hoc usage, and `make test` to run all unit tests inside the container. See
the [Makefile](Makefile) for all available actions.

To upgrade the version and trigger a new release, use `bump-my-version bump minor chord_progressions/__init__.py`.

The documentation uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) to build a static site from
Markdown files. Use `mkdocs serve` to start a live preview server of the site that automatically rebuilds upon saving.
Build the site with `mkdocs build` and deploy with `mkdocs gh-deploy`.
