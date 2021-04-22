import os

import pretty_midi
from progression_extraction.label_arrangement import (
    DATA_DIR,
    get_minimal_segments,
    get_partition_points,
    parse_events,
)

# TODO: test that a maxiumum of six segment evaluations occur per note


def test_get_minimal_segments():

    filename = os.path.join(DATA_DIR, "test_1.mid")

    midi = pretty_midi.PrettyMIDI(filename)

    events = parse_events(midi)

    p_all = get_partition_points(events)

    s_m = get_minimal_segments(p_all)

    assert len(s_m) == 3

    assert s_m[0].start == 0
    assert s_m[0].end == 1
    assert s_m[0].pitches == [60, 64, 67]

    assert s_m[1].start == 1
    assert s_m[1].end == 2
    assert s_m[1].pitches == [60, 64, 69]

    assert s_m[2].start == 2
    assert s_m[2].end == 2.9947916666666665
    assert s_m[2].pitches == [60, 69, 65]
