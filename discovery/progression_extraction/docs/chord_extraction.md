### Tasks aided by chord extraction

Automated arranging, accompaniment, and phrasing are all aided by an understanding of the chordal structure of a piece.

1. Arranging - Understanding the relationships between progressions helps inform the order of progressions in a composition

    - relationship of progression to other progressions in track
    - role of progression in track

    - in Chordico: arrangement mode, track blueprints

2. Accompaniment - Understanding how a progression relates to the melody helps inform reharmonization possibilities

    - relationship between progression and melody
    - role of progression in track

    - in Chordico: generate chords given melody, reharmonization

3. Phrasing - Understanding where a progression begins, climaxes, and ends helps inform the dynamics, articulation, and inflection of melodic phrases

    - relationship of progression chord to other progression chords
    - role of chord in progression

    - in Chordico: storyboards, Chordico performer

### Notes on chord extraction from MIDI

-   [Learning-Based Methods for Comparing Sequences, with Applications to Audio-to-MIDI Alignment and Matching](https://colinraffel.com/publications/thesis.pdf), Colin Raffel, 2016
-   [Automatic Analysis of Music in Standard MIDI Files (2019)](https://www.cs.cmu.edu/~music/papers/zheng_jiang_thesis.pdf), Zheng Jiang, 2019

###### Learning a Latent Space of Multitrack Measures

2018
Ian Simon, Adam Roberts, Colin Raffel, Jesse Engel, Curtis Hawthorne & Douglas Eck
Google Brain
https://nips2018creativity.github.io/doc/Learning_a_Latent_Space_of_Multitrack_Measures.pdf
Section C.8

```
When conditioning on chords, we would ideally train using ground-truth labels. Since MIDI files donot typically contain such labels [32], we automatically infer chord labels using a heuristic process.

First, each MIDI file is split into segments with a consistent tempo and time signature.  For each segment, we infer chords at a frequency of 2 per measure using the Viterbi algorithm [39] over aheuristically-defined probability distribution; as a byproduct we also infer the time-varying key ofthe sequence. This algorithm takes time quadratic in the number of measures, so for efficiency wediscard MIDI segments longer than 500 measures.

We infer 8 different chord types (major, minor, augmented, diminished, dominant-seventh, major-seventh, minor-seventh, and half-diminished) rooted at each of the 12 pitch classes plus a single“no-chord” designation, for a total of 97 chord classes. After chord inference is complete, the 8 chordtypes are projected down to the 4 triad types (49 total classes) used as model input
```

###### COCHONUT: Recognizing complex chords from MIDI guitar sequences

Scholz, Ricardo and Ramalho, Geber
2008
ISMIR

###### Musical keys and chords recognition using unsupervised learning with infinite Gaussian mixture

Wang, Yun-Sheng and Wechsler, Harry
2012
2nd ACM International Conference on Multimedia Retrieval

###### Chord recognition in symbolic music using semi-Markov conditional random fields

Masada, Kristen and Bunescu, Razvan C
2017
ISMIR

Since harmonic changes may occur only when notes be-gin or end, we first create a sorted list of all the note on-sets and offsets in the input music, i.e. the list of partitionpoints[8].

###### Algorithms for Chordal Analysis

Pardo and Birmingham
Articial Intelligence Laboratory
University of Michigan

https://interactiveaudiolab.github.io/assets/papers/pardo-birmingham-cmj02.pdf

We define two major tasks in harmonic analysis: segmentation (i.e. identifying thos e places in themusic where the harmony changes) and labeling(i.e. giving each segment the proper quality and root)

Harmonic change can only occurwhen at least one note begins or ends. A partition point occurs where the set of pitches currently sounding in the music changes by the onset or offset of one or more notes. A segment is a contiguous interval between two partition points. A minimal segment is the interval between two sequential partition points.

Given a segment containing a collection of notes,the score for a particular template is calculatedfrom th e steps:

1. Determine the weight of each note in the segment by counting the number of minimal segments in which the note is present between the start and end of the current segment.

2. Sum the weights of the notes whose pitch class matches a template element. Call this the Positive Evidence, P.

3. Sum the weights of the notes not matching any template element. Call this Negative Evidence, N.

4. Sum the count of template elements not matched by any note. Call these the Misses, M.

5. Calculate the score for a template, S, with the formula S = P - (M + N)

Tie breaking:

1. ROOT WEIGHT: Choose the template whose root pitch class has the greatest weight of notes present in the segment.

2. PRIOR PROBABILITY: Choose the template with the higher prior probability of occurence.

3. DIM7 RESOLUTION: If all top templates are fully diminished 7th chords, select the template whose root is one half-step below the root of the top scoring template in the following segment.

To label a segment, al l 72 templates ar e scored,and the highest scoring template determines thesegment label.

###### BREVE: An HMPerceptron-based chord recognition system

Daniele P. Radicioni and Roberto Esposito.

###### Harmonic Analysis with Probabilistic Graphical Models

Christopher Raphael and Josh Stoddard
https://jscholarship.library.jhu.edu/bitstream/handle/1774.2/25/paper.pdf?sequence%3D1

###### Many others

https://scholar.google.com/scholar?cites=2951790455746358142&as_sdt=2005&sciodt=0,5&hl=en
