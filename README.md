# Chord progressions

Use this package to generate and describe chord progressions.

##### Run units tests:

```bash
pytest
```

##### Generate a progression locally

```bash
./run.sh
```

## TODO

##### Eventually

-   [feature] output variable chord durations from solver
-   [feature] consider lower and upper structures in select_voicing
-   [feature] add the possibility of a repeated note in a different octave
-   [feature] Generalize `noteNumberToFrequency` to use any periodic tuning https://github.com/soul-lang/SOUL/pull/26/files
-   [feature] use VAE as solver

-   [maintainability] merge together chord_strings and duration_strings
-   [maintainability] break out the merging of chord types into a function and test it
-   [maintainability] pass midi note numbers everywhere as "notes" and include note names as "noteNames"

##### Maybe

-   [feature] extend interval class vectors to "polychord-content" vectors
-   [feature] `chord_contained_in_type` function
-   [feature] download midi files from Geocities MIDI archive on the Internet Archive & parse into progressions. find the zip of 100k midi files used by bitmidi.com
