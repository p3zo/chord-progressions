"""
Implements a method for extracting chords from symbolic music that is based on
the HarmAn algorithm by Pardo & Birmingham:

https://interactiveaudiolab.github.io/assets/papers/pardo-birmingham-cmj02.pdf
"""

import os
import time
from copy import deepcopy

import networkx as nx
import numpy as np
import pandas as pd
from chord_progressions import logger
from chord_progressions.chord import Chord
from chord_progressions.extract.midi import (
    DEFAULT_QUANTIZE_BEAT,
    DEFAULT_SHORTEST_NOTE,
    DEFAULT_SMOOTH_BEAT,
)
from chord_progressions.extract.midi import simplify_harmony
from chord_progressions.io.midi import load_midi_file
from chord_progressions.pitch import (
    NOTE_NAMES,
    get_note_from_midi_num,
    get_pitch_class_from_midi_num,
)
from chord_progressions.progression import Progression
from chord_progressions.type_templates import (
    TYPE_TEMPLATES,
    get_template_from_template_str,
    get_type_num_from_type,
)

# Each label is a chord type at one transposition, so C major and F major are different labels.
# Row i of LABEL_TEMPLATES is the template of type LABEL_TYPE_IDS[i] transposed up by
# LABEL_TRANSPOSITIONS[i] semitones. The transposition is not the musical root: the dominant-seventh
# template, for example, starts on its third.
MIN_NUM_NOTES = 3
MAX_NUM_NOTES = 6

label_type_ids = []
label_transpositions = []
label_templates = []

for template_name, template_str in TYPE_TEMPLATES.items():
    template = get_template_from_template_str(template_str)

    if not MIN_NUM_NOTES <= sum(template) <= MAX_NUM_NOTES:
        continue

    seen = set()
    for transposition in range(12):
        transposed = template[-transposition:] + template[:-transposition]

        # Symmetric chords like the augmented triad repeat under transposition
        if tuple(transposed) in seen:
            continue
        seen.add(tuple(transposed))

        label_type_ids.append(get_type_num_from_type(template_name))
        label_transpositions.append(transposition)
        label_templates.append(transposed)

LABEL_TYPE_IDS = np.array(label_type_ids)
LABEL_TRANSPOSITIONS = np.array(label_transpositions)
LABEL_TEMPLATES = np.array(label_templates)


class PartitionPoint:
    """A partition point occurs where the set of sounding notes changes by the onset or offset of one or more notes."""

    def __init__(self, start):
        self.time = start
        self.onsets = []
        self.offsets = []

    def add_event(self, note, is_onset):
        if is_onset:
            self.onsets.append(note)
        else:
            self.offsets.append(note)

    def pprint(self):
        logger.debug(f"    time {self.time}")
        logger.debug(f"    onsets {[get_note_from_midi_num(i) for i in self.onsets]}")
        logger.debug(
            f"    offsets, {[get_note_from_midi_num(i) for i in self.offsets]}"
        )


class MinimalSegment:
    """A minimal segment is the interval between two sequential partition points."""

    def __init__(self):
        self.start = 0  # seconds
        self.end = 0  # seconds
        self.midi_nums = []  # midi note numbers

    def update_midi_nums(self, midi_nums, add):
        if add:
            self.midi_nums.extend(midi_nums)
        else:
            for p in midi_nums:
                self.midi_nums.remove(p)

    def get_pitch_class_weights(self):
        """Returns the number of sounding notes of each pitch class as a length-12 array"""
        pcs = [get_pitch_class_from_midi_num(p) for p in self.midi_nums]
        return np.bincount(pcs, minlength=12)

    def get_notes(self):
        return [get_note_from_midi_num(n) for n in self.midi_nums]

    def get_note_occurences(self):
        midi_nums = self.midi_nums
        return {n: midi_nums.count(n) for n in midi_nums}

    def pprint(self):
        logger.debug(f"    start {self.start}")
        logger.debug(f"    end {self.end}")
        logger.debug(f"    midi_nums {self.get_notes()}")


def parse_events(pmid):
    """Parses a PrettyMIDI object into a 2D array with (time, note, is_onset) columns."""

    points = []

    for instrument in pmid.instruments:

        if instrument.is_drum:
            continue

        for note in instrument.notes:
            points.append((note.start, note.pitch, 1))
            points.append((note.end, note.pitch, 0))

    dtype = np.dtype([("time", float), ("note", int), ("is_onset", bool)])
    events = np.array(points, dtype=dtype)

    return np.sort(events, order="time")


def get_partition_points(events):
    """Returns the partition points for a set of events, ordered by time."""

    p_all = []

    time_cursor = events[0][0]
    point = PartitionPoint(time_cursor)

    for event in events:
        t = event["time"]
        note = event["note"]
        is_onset = event["is_onset"]

        if time_cursor == t:
            point.add_event(note, is_onset)

        else:
            p_all.append(deepcopy(point))

            time_cursor = t

            point = PartitionPoint(t)
            point.add_event(note, is_onset)

    p_all.append(deepcopy(point))

    # Uncomment for debug output
    logger.debug(f"--- {len(p_all)} partition points ---")
    for ix, p in enumerate(p_all):
        logger.debug(f"  p{ix}")
        p.pprint()

    return p_all


def get_label_scores(pc_weights):
    """Scores the weighted pitch classes of a minimal segment against all labels.

    Uses the algorithm defined in Pardo 2002 Fig 4: S = P - (M + N), where P is the weight of
    notes in the template, N the weight of notes outside it, and M the number of template notes
    that are not sounding.

    Input:
        pc_weights, a length-12 array of the number of sounding notes of each pitch class

    Returns:
        an array with one score per label
    """
    positive = LABEL_TEMPLATES @ pc_weights
    negative = pc_weights.sum() - positive
    misses = LABEL_TEMPLATES @ (pc_weights == 0)

    return positive - (misses + negative)


def get_minimal_segments(p_all):
    """Returns the minimal segments for a set of partition points, ordered by time."""

    s_m = []

    s = MinimalSegment()

    s.start = p_all[0].time
    s.update_midi_nums(p_all[0].onsets, 1)

    for point in p_all[1:]:
        s.end = point.time

        midi_nums = s.midi_nums

        s_m.append(deepcopy(s))

        s = MinimalSegment()

        s.start = point.time

        s.update_midi_nums(midi_nums, 1)
        s.update_midi_nums(point.onsets, 1)

        s.update_midi_nums(point.offsets, 0)

    logger.debug(f"\n--- {len(s_m)} minimal segments ---")

    return s_m


def get_segment_label(label_scores):
    """Returns the best score and label of a segment, given its summed label scores.

    See Figure 3 in Pardo 2002
    """
    # TODO: tiebreak by root weight, template probability, and dim7 resolution (Pardo 2002 Fig 4).
    # Until then the first maximum wins, i.e. the earliest entry in TYPE_TEMPLATES.
    best_label = int(np.argmax(label_scores))

    return int(label_scores[best_label]), best_label


def describe_label(label):
    chord_type = list(TYPE_TEMPLATES)[LABEL_TYPE_IDS[label]]
    return f"{chord_type} transposed to {NOTE_NAMES[LABEL_TRANSPOSITIONS[label]]}"


def get_segment_midi_nums(segment):
    """Aggregates the notes in all the minimal segments that comprise a segment"""

    midi_nums = []

    for ms in segment:
        midi_nums.extend(ms.get_note_occurences())

    return midi_nums


def segment_and_label(p_all, s_m):
    """
    Based on the HarmAn algorithm by Pardo & Birmingham:
        https://interactiveaudiolab.github.io/assets/papers/pardo-birmingham-cmj02.pdf

    Implementations to reference:
        - https://github.com/salilgupta1/chordal_analysis/blob/c290dda5684c1d63d37867abdf0008cff41b2e5f/chordal_analysis/main.py
        - https://github.com/tomthecollins/wimir-eurovision/blob/68b1fa8bc616b751c0681dcc07fe0dc3079caabb/public/lib/maia-util_r0.2.12.js#L2817
    """

    logger.debug("\n--- Segmentation ---")

    t0 = time.time()

    # in the graph, nodes are partition points and edges are segments
    G = nx.DiGraph()

    final_ix = len(p_all) - 1

    # A segment scores the sum of its minimal segment scores rather than the score of its summed
    # pitch class weights as in Pardo 2002. The templates go up to six notes, so with summed
    # weights two neighboring triads always fit some hexachord perfectly and would merge.
    # Summed scores also let each minimal segment be scored only once.
    G.add_node(0, marked=1, time=p_all[0].time)

    ui = 0  # index of the preceding vertex
    uv_scores = np.zeros(len(LABEL_TEMPLATES), dtype=int)  # summed scores of s_m[ui:vi]
    uv_num_notes = 0

    vw_scores = get_label_scores(s_m[0].get_pitch_class_weights())  # scores of s_m[vi]
    vw_num_notes = len(s_m[0].midi_nums)

    for vi in range(1, final_ix):
        p = p_all[vi]

        # the minimal segment that ended at this point joins the preceding segment
        uv_scores = uv_scores + vw_scores
        uv_num_notes += vw_num_notes

        vw_scores = get_label_scores(s_m[vi].get_pitch_class_weights())  # succeeding segment
        vw_num_notes = len(s_m[vi].midi_nums)

        # a minimal segment without notes is a rest for all instruments
        if uv_num_notes == 0:
            logger.debug(f"  {vi}/{final_ix} - Continue: No notes in segment")
            continue

        uv_score, uv_label = get_segment_label(uv_scores)
        vw_score, vw_label = get_segment_label(vw_scores)
        uw_score, uw_label = get_segment_label(uv_scores + vw_scores)  # full segment

        if uw_score < (uv_score + vw_score):
            logger.debug(
                f"  {vi}/{final_ix} - New: {describe_label(uw_label)} ({uw_score}) < {describe_label(uv_label)} ({uv_score}) + {describe_label(vw_label)} ({vw_score})"
            )

            uv_midi_nums = get_segment_midi_nums(s_m[ui:vi])
            uv_notes = [get_note_from_midi_num(n) for n in uv_midi_nums]

            edge_attributes = {
                "start_segment": ui,
                "end_segment": vi,
                "label": uv_label,
                "score": uv_score,
                "midi_nums": uv_midi_nums,
                "notes": uv_notes,
            }

            G.add_node(vi, marked=1, time=p.time)
            G.add_edge(ui, vi, **edge_attributes)

            ui = vi
            uv_scores = np.zeros(len(LABEL_TEMPLATES), dtype=int)
            uv_num_notes = 0
        else:
            logger.debug(
                f"  {vi}/{final_ix} - Continue: {describe_label(uw_label)} ({uw_score}) >= {describe_label(uv_label)} ({uv_score}) + {describe_label(vw_label)} ({vw_score})"
            )

    G.add_node(final_ix, marked=1, time=p_all[final_ix].time)

    # the last minimal segment closes the final segment
    uv_scores = uv_scores + vw_scores

    final_segment = s_m[ui:final_ix]
    final_segment_midi_nums = get_segment_midi_nums(final_segment)
    final_segment_notes = [get_note_from_midi_num(n) for n in final_segment_midi_nums]

    final_score, final_label = get_segment_label(uv_scores)

    final_edge_attributes = {
        "start_segment": ui,
        "end_segment": final_ix,
        "label": final_label,
        "score": final_score,
        "midi_nums": final_segment_midi_nums,
        "notes": final_segment_notes,
    }

    G.add_edge(ui, final_ix, **final_edge_attributes)

    logger.debug("\n--- Results ---")
    logger.debug(f"{len(G.edges)} segments")

    rows = []

    template_names = list(TYPE_TEMPLATES)

    for e in G.edges:
        edge = G[e[0]][e[1]]

        start = G.nodes[e[0]]["time"]
        end = G.nodes[e[1]]["time"]

        row = {
            "start_segment": edge["start_segment"],
            "start_time": start,
            "end_segment": edge["end_segment"],
            "end_time": end,
            "duration": end - start,
            "label_id": int(LABEL_TYPE_IDS[edge["label"]]),
            "label": template_names[LABEL_TYPE_IDS[edge["label"]]],
            "midi_nums": edge["midi_nums"],
            "notes": edge["notes"],
            "chord": Chord(edge["midi_nums"]),
        }
        rows.append(row)

    logger.debug(f"segment_and_label done in {time.time() - t0} seconds")

    return rows


def label_midi(midi):
    events = parse_events(midi)

    p_all = get_partition_points(events)

    s_m = get_minimal_segments(p_all)

    return segment_and_label(p_all, s_m)


def label_file(filepath):
    logger.debug(f"Labeling {filepath}")

    midi = load_midi_file(filepath)

    if not midi:
        return None

    return label_midi(midi)


def write_labels(labels, inpath, outpath, arrangement_id=None):
    if not labels:
        logger.error(f"Failed for {inpath}")
        return {inpath: None}

    if not arrangement_id:
        arrangement_id = os.path.splitext(os.path.basename(inpath))[0]

    df = pd.DataFrame(labels)
    df["arrangement_id"] = arrangement_id
    df.to_csv(outpath, sep="\t", index=False)

    # js_outpath = outpath.replace("csv", "json")
    # df.to_json(js_outpath, orient="records")

    logger.info(f"Labels saved to {outpath}")

    return {inpath: labels}


def extract_progression_from_midi(
    filepath,
    shortest_note=DEFAULT_SHORTEST_NOTE,
    smooth_beat=DEFAULT_SMOOTH_BEAT,
    quantize_beat=DEFAULT_QUANTIZE_BEAT,
    simplified_path=None,
    harman_labels_path=None,
):
    """
    Params
        filepath: str, Path to a midi file
        shortest_note: float, see params for `simplify_harmony()`
        smooth_beat: float, see params for `simplify_harmony()`
        quantize_beat: float, see params for `simplify_harmony()`
        simplified_path: str, if passed writes a midi file with simplified harmony. Useful for debugging.
        simplified_path: str, if passed writes a csv file with the output harman labels. Useful for debugging.

    Returns
        progression: Progression, the extracted progression object
        segment_start_times: list(float): the start times of each chord in seconds
    """

    midi = load_midi_file(filepath)

    simplified = simplify_harmony(midi, shortest_note, smooth_beat, quantize_beat)

    if simplified_path:
        simplified.write(simplified_path)
        print(f"Wrote simplified midi to {simplified_path}")

    harman_labels = label_midi(simplified)

    if harman_labels_path:
        _ = write_labels(harman_labels, filepath, harman_labels_path)

    chords = [i["chord"] for i in harman_labels]
    durations = [i["end_time"] - i["start_time"] for i in harman_labels]

    bpms = [i[0] for i in midi.get_tempo_changes() if i[0] > 0]

    # TODO: support tempo changes in progressions
    return Progression(chords, durations, bpm=bpms[0], name=filepath)
