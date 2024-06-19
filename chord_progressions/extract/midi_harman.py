"""
Implements a method for extracting chords from symbolic music that is based on
the HarmAn algorithm by Pardo & Birmingham:

https://interactiveaudiolab.github.io/assets/papers/pardo-birmingham-cmj02.pdf
"""

import os
import time
from collections import Counter, defaultdict
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
    get_note_from_midi_num,
    get_pitch_class_from_midi_num,
)
from chord_progressions.progression import Progression
from chord_progressions.type_templates import (
    TYPE_TEMPLATES,
    get_template_from_template_str,
    get_type_num_from_type,
)
from chord_progressions.utils import shift_arr_by_one

# We pre-calculate all the templates we want to use as labels
# TEMPLATE_LABELS will be {chord_type_id: (rotations, one_indices)}
MIN_NUM_NOTES = 3
MAX_NUM_NOTES = 6
TEMPLATE_LABELS = {}


def get_template_str(template):
    return "".join([str(i) for i in template])


def get_all_rotations_of_template(template):
    rotation_strs = set()
    rotation_strs.add(get_template_str(template))

    prev = template

    for i in range(len(template) - 1):
        rotated = shift_arr_by_one(prev)
        rotation_strs.add(get_template_str(rotated))

        prev = rotated

    return [[int(j) for j in list(i)] for i in rotation_strs]


for template_name, template_str in TYPE_TEMPLATES.items():

    template_id = get_type_num_from_type(template_name)
    template = get_template_from_template_str(template_str)

    if sum(template) >= MIN_NUM_NOTES and sum(template) <= MAX_NUM_NOTES:
        if template_id not in TEMPLATE_LABELS:
            TEMPLATE_LABELS[template_id] = []

        rotations = get_all_rotations_of_template(template)

        one_indices = []
        for rotation in rotations:
            one_indices.append([ix for ix, i in enumerate(rotation) if i == 1])

        TEMPLATE_LABELS[template_id] = (rotations, one_indices)


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
        self.template_scores = {}

    def update_midi_nums(self, midi_nums, add):
        if add:
            self.midi_nums.extend(midi_nums)
        else:
            for p in midi_nums:
                self.midi_nums.remove(p)

    def get_pitch_classes(self):
        return [get_pitch_class_from_midi_num(p) for p in self.midi_nums]

    def get_pitch_class_weights(self):
        pcs = self.get_pitch_classes()
        return {pc: pcs.count(pc) for pc in pcs}

    def get_template_scores(self):
        pcs = self.get_pitch_classes()
        pc_weights = {pc: pcs.count(pc) for pc in pcs}
        return get_template_scores(pc_weights)

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


def get_segment_pc_weights(segment):
    """Aggregates the pitch class weights of all minimal segments within a segment."""

    segment_pc_weights = defaultdict(int)

    for s in segment:
        pc_weights = s.get_pitch_class_weights()

        for pc, weight in pc_weights.items():
            print(pc, weight)
            segment_pc_weights[pc] += weight

    return segment_pc_weights


def get_template_score(pc_weights, template, oix):
    """Scores a weighted set of pitch classes against a single template.

    Uses the algorithm defined in Pardo 2002 Fig 4.

    Input:
        pc_weights, a dict of {pc: weight}
        template, the template against which to score. Example: [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        oix, the one-indices for the template, pre-computed for performance. Example: [0, 4, 9]

    Returns:
        S, an integer score
    """

    P = 0  # positive evidence
    N = 0  # negative evidence
    M = 0  # misses

    for pc, weight in pc_weights.items():
        if template[pc]:
            P += weight
        else:
            N += weight

    for _ in set(oix) - set(pc_weights):
        M += 1

    return P - (M + N)


def get_template_scores(pc_weights):
    """Scores a weighted set of pitch classes against all template labels.

    Returns a dict of {label: score}
    """
    scores = {}

    for template_name, (rotations, one_indices) in TEMPLATE_LABELS.items():

        rotation_scores = []

        for ix, rotation in enumerate(rotations):
            score = get_template_score(pc_weights, rotation, one_indices[ix])

            rotation_scores.append(score)

        # TODO: use dim7 resolution as tiebreaker (see Fig 4 in Pardo 2002)
        best_rotation_score = max(rotation_scores)

        if template_name not in scores:
            scores[template_name] = best_rotation_score
        else:
            scores[template_name] += best_rotation_score

    return scores


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

    ## Uncomment for debug output
    # for ix, sm in enumerate(s_m):
    #     logger.debug(f"  sm{ix}")
    #     # sm.pprint()
    #     pc_weights = sm.get_pitch_class_weights()
    #     sm.template_scores = get_template_scores(pc_weights)

    return s_m


def get_segment_label(segment):
    """Aggregates the template scores of all minimal segments within a segment and returns the best label.

    See Figure 3 in Pardo 2002
    """

    if not len(segment) > 0:
        raise ValueError("Empty segment")

    counter = Counter(segment[0].get_template_scores())

    for ms in segment[1:]:
        counter.update(Counter(ms.get_template_scores()))

    if not len(counter) > 0:
        raise ValueError("No scores for segment")

    # TODO: it's common for multiple templates to have the same score. How should we tiebreak?
    best_template, best_score = counter.most_common(1)[0]

    return best_score, best_template


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

    ui = 0  # index of the preceding vertex

    for vi, p in enumerate(p_all):

        if vi in [0, final_ix]:
            G.add_node(vi, marked=1, time=p.time)
            continue

        uv_segment = s_m[ui:vi]  # preceding segment
        uv_midi_nums = get_segment_midi_nums(uv_segment)
        uv_notes = [get_note_from_midi_num(n) for n in uv_midi_nums]

        # a minimal segment without notes is a rest for all instruments
        if len(uv_midi_nums) == 0:
            logger.debug(f"  {vi}/{final_ix} - Continue: No notes in segment")
            continue

        uv_score, uv_label = get_segment_label(uv_segment)

        wi = vi + 1  # index of the succeeding vertex
        vw_score, vw_label = get_segment_label(s_m[vi:wi])  # succeeding segment
        uw_score, uw_label = get_segment_label(s_m[ui:wi])  # full segment

        if uw_score < (uv_score + vw_score):
            logger.debug(
                f"  {vi}/{final_ix} - New: {uw_label} ({uw_score}) < {uv_label} ({uv_score}) + {vw_label} ({vw_score})"
            )

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
        else:
            logger.debug(
                f"  {vi}/{final_ix} - Continue: {uw_label} ({uw_score}) >= {uv_label} ({uv_score}) + {vw_label} ({vw_score})"
            )

    final_segment = s_m[ui:final_ix]
    final_segment_midi_nums = get_segment_midi_nums(uv_segment)
    final_segment_notes = [get_note_from_midi_num(n) for n in final_segment_midi_nums]

    final_score, final_label = get_segment_label(final_segment)

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
            "label_id": edge["label"],
            "label": template_names[edge["label"]],
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
