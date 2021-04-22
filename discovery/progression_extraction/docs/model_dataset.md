# Model Dataset

-   [Model Dataset Schema](https://docs.google.com/spreadsheets/d/1fOrfkWwWzhdxB01SpzN4jGegZIXpVyUPXHkWTa7b1Fs/edit#gid=793237640)

## Processing steps

1.  Parse MIDI tracks from the [Lakh MIDI dataset](https://colinraffel.com/projects/lmd) matched with the [Million Song Dataset](millionsongdataset.com).

2.  Extract chords from MIDI tracks

3.  Aggregate chords into [progressions](###progressions)

4.  Create [chord and progression features](https://docs.google.com/spreadsheets/d/1fOrfkWwWzhdxB01SpzN4jGegZIXpVyUPXHkWTa7b1Fs/edit#gid=793237640)

### Progressions

-   section tracks, then chords within sections = progressions

    -   [spotify api](https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-audio-analysis) sections. Defined by large variations in rhythm/timbre. Each section has its own tempo, key, mode, time_signature, and loudness

        -   according to the spotify data eng team, sections are not great (https://www.youtube.com/watch?v=goUzHd7cTuA)

    -   could use repeating chord orders to define own sections. What this paper calls "recurrent structural analysis for semantic segmentation" https://alumni.media.mit.edu/~chaiwei/papers/Chai_music_final.pdf

-   see https://github.com/magenta/magenta/blob/master/magenta/pipelines/chord_pipelines.py

### LMD issues

-   Some MSD track_ids have multiple MIDI arrangements - how to choose best one?

-   `lmd/small_lmd_matched_h5/P/R/R/TRPRRGW128F4265567.h5` does not match `lmd/small_lmd_matched/P/R/R/TRPRRGW128F4265567/*` - MSD song is Venus by The Ventures - LMD song is Venus by Shocking Blue

### Perceptual qualities

Could use genre labels as a bridge to perceptual features

-   darkness, as defined by `dark` subgenres on [everynoise](http://everynoise.com)
-   serenity, as defined by keywords from playlist names, e.g. `ambient relaxing music`
-   tension, as defined by Elaine Chew's spiral model

### References

-   [List of MIR Datasets](https://docs.google.com/spreadsheets/d/1a7faC5RA-NjRUAZRg1DUrxz8mOP0_agyhaxcdq8YlNA/edit#gid=0)

-   Section C.7 in [Learning a Latent Space of Multitrack Measures](https://nips2018creativity.github.io/doc/Learning_a_Latent_Space_of_Multitrack_Measures.pdf)
