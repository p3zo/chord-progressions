"""
Construct and evaluate graphs of a chord progression.


# Definitions
Index
    int
    Position of the chord in the progression

Note
    int
    midi note number

Chord graph
    networkx.Graph
    As described in section 2.1 of A Graph-Theoretic Approach to Efficient Voice-Leading.
    Vertices represent triads, and edges represents parsimonious voice-leading.


# Graphs

## Chord-to-chord, directed

1
    Nodes are indices
    Edges are notes in common between chords

2
    Nodes are notes
    Edges are notes in common within chords

## All chords, undirected

1
    Nodes are notes in entire progression
    Edges are notes in common within chords
        Edge weights are num co-occurences

2
    Nodes are notes in entire progression
    Edges are notes in common between chords

## Graph of graphs, directed

    Nodes are chord graphs
        Node IDs are indices

    Edges are common triads
        Edge weights are

# Metrics

- Connectivity
- Traversability
- Centrality
- Communicability
- Coloring
- Group structure
- Eccentricity
- Diameter
- Voice-leading size
- Self-centerd
- Voice crossing
- Spacing
- Open / closed ratio
- Two-voice efficiency
- Four-voice efficiency
"""

import networkx as nx

from chord_progressions.chord import get_template_from_notes, get_type_num_from_type


def get_chord_graph(chord):

    G = nx.Graph()

    return G


if __name__ == "__main__":

    chord_type = "major chord"
    chord = {
        "id": "0",
        "ix": 0,
        "type": chord_type,
        "typeId": get_type_num_from_type(chord_type),
        "notes": ["C4", "E4", "G4"],
        "locked": 0,
    }

    template = get_template_from_notes(chord["notes"])

    pitch_class_set = set([ix for ix, i in enumerate(template) if i == 1])
