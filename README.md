# Chord Progressions

[![PyPI Latest Release](https://img.shields.io/pypi/v/chord-progressions.svg)](https://pypi.org/project/chord-progressions/)

A library for working with chord progressions.

## Installation

Requires Python 3.12 or newer.

```
pip install chord-progressions
```

## Usage

See documentation at https://p3zo.github.io/chord-progressions.

## Development

Configuration for local development with Docker is provided. Run `make build` to build the container, `make shell` to
get a shell inside of it for ad-hoc usage, and `make test` to run all unit tests inside the container. See
the [Makefile](Makefile) for all available actions.

Every merge to `main` publishes a new release to PyPI. The version is the latest `vX.Y.Z` tag with its minor number
raised; label the pull request `release:patch` or `release:major` to raise that number instead, or `no-release` to skip
the release.

The documentation uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) to build a static site from
Markdown files. Use `mkdocs serve` to start a live preview server of the site that automatically rebuilds upon saving.
Pushes to `main` that touch the docs build and deploy the site to GitHub Pages.
