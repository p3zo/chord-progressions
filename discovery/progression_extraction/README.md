# Progression Extraction

Extracts progressions from MIDI files and prepare a dataset for modeling.

<div style="text-align: center">
  <img src="docs/progression_extraction.png" width=800>
</div>

## Data

Uses the `LMD-matched` and `LMD-matched metadata` datasets from [The Lakh MIDI Dataset v0.1](https://colinraffel.com/projects/lmd).

`LMD-matched` contains LMD midi files which have been matched to entries in the the [Million Song Dataset](millionsongdataset.com).

Arrangements in the LMD are matched to tracks in the MSD.

For example, for the track ID `TRPKJMG12903CC6F88`, the path to the MSD data for the track is `DATA_DIR/lmd_matched_h5/P/K/J/TRPKJMG12903CC6F88/` and the path to all the MIDI arrangements available for the track is `DATA_DIR/lmd_matched/P/K/J/TRPKJMG12903CC6F88/`.

## Contents

Scripts

-   [label_arrangement.py](label_arrangement.py): Extracts chords from a midi file
-   [label_arrangements.py](label_arrangements.py): Extracts chords from multiple midi files
-   [aggregate_lmd_matched.py](aggregate_lmd_matched.py): Aggregates LMD arrangements from `LMD-matched` with MSD metadata from `LMD-matched metadata`
-   [plot_extracted_chords.py](plot_extracted_chords.py): Visualizes the output of chord extraction
-   [test_label_arrangement.py](test_label_arrangement.py): Unit tests for chord extraction functions

Modules

-   [hdf5_getters.py](hdf5_getters.py): Functions for extracting metadata from .h5 files
-   [parallel.py](parallel.py): Functions for parallel processing

Notes

-   [Notes on the MIR task of chord extraction](docs/chord_extraction.md)
-   [Progression VAE Dataset](docs/dataset.md)

## TODO

##### Prioritized

-   [bug] notes are double-counting during segmentation & labeling
-   close the loop of [processing steps](dataset.md##processing-steps) for one track

##### Eventually

-   use artist as label instead of genre for first draft
-   extract all chords for a single artist
-   aggregate chords into progressions
-   get genre labels on LMD
-   run extraction on entire LMD
-   use hierarchical genre relationships from [Tagtraum](https://www.tagtraum.com/msd_genre_datasets.html)
-   compile VAE dataset

##### Maybe

-   [maintainability] get bars:beats:sixteenths in outfiles
-   [feature] give link to spotify playlist, gives progressions like playlist tracks
