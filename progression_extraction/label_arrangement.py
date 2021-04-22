"""Extracts chords from a midi file"""

import csv
import os
import time
import warnings
from collections import Counter
from copy import deepcopy

import networkx as nx
import numpy as np
import pandas as pd
import pretty_midi

from progression_extraction import DATA_DIR, SMALL_LMD_PATH, OUTPUT_LABEL_DIR
from chord_progressions import logger
from chord_progressions.chord import (
    get_template_from_template_string,
    get_type_num_from_type,
)
from chord_progressions.db import load_type_templates
from chord_progressions.evaluator import evaluate_chord
from chord_progressions.pitch import (
    get_note_from_midi_num,
    get_pitch_class_from_midi_num,
)
from chord_progressions.solver import get_all_rotations_of_template

ALL_TEMPLATES = load_type_templates()

MIN_NUM_NOTES = 2
MAX_NUM_NOTES = 9
ALL_TEMPLATE_ROTATIONS = {}


for template_name, template_str in ALL_TEMPLATES.items():

    template_id = get_type_num_from_type(template_name)
    template = get_template_from_template_string(template_str)

    if sum(template) >= MIN_NUM_NOTES and sum(template) <= MAX_NUM_NOTES:
        if template_id not in ALL_TEMPLATE_ROTATIONS:
            ALL_TEMPLATE_ROTATIONS[template_id] = []

        rotations = get_all_rotations_of_template(template)

        one_indices = []
        for rotation in rotations:
            one_indices.append([ix for ix, i in enumerate(rotation) if i == 1])

        ALL_TEMPLATE_ROTATIONS[template_id] = (rotations, one_indices)


class PartitionPoint:
    def __init__(self, start):
        self.time = start
        self.onsets = []
        self.offsets = []

    def add_event(self, pitch, is_onset):
        if is_onset:
            self.onsets.append(pitch)
        else:
            self.offsets.append(pitch)

    def pprint(self):
        logger.debug(f"    time {self.time}")
        logger.debug(f"    onsets {[get_note_from_midi_num(i) for i in self.onsets]}")
        logger.debug(
            f"    offsets, {[get_note_from_midi_num(i) for i in self.offsets]}"
        )


class MinimalSegment:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.pitches = []
        self.template_scores = {}

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end

    def update_pitches(self, pitches, add):
        if add:
            self.pitches.extend(pitches)
        else:
            for p in pitches:
                self.pitches.remove(p)

    def get_pitches(self):
        return self.pitches

    def get_pitch_classes(self):
        return [get_pitch_class_from_midi_num(p) for p in self.pitches]

    def get_pitch_class_occurrences(self):
        pcs = self.get_pitch_classes()
        return {pc: pcs.count(pc) for pc in pcs}

    def get_notes(self):
        return [get_note_from_midi_num(p) for p in self.pitches]

    def get_note_occurences(self):
        notes = self.get_notes()
        return {note: notes.count(note) for note in notes}

    def pprint(self):
        logger.debug(f"    start {self.start}")
        logger.debug(f"    end {self.end}")
        logger.debug(f"    pitches {self.get_notes()}")


def parse_events(midi):
    """Parses a pretty_midi object into a 2D array with (time, pitch, onset) columns."""

    points = []

    for instrument in midi.instruments:

        if instrument.is_drum:
            continue

        for note in instrument.notes:
            points.append((note.start, note.pitch, 1))
            points.append((note.end, note.pitch, 0))

    dtype = np.dtype([("time", float), ("pitch", int), ("onset", bool)])
    p_all = np.array(points, dtype=dtype)

    return np.sort(p_all, order="time")


def get_partition_points(events):
    """
    A partition point occurs where the set of pitches currently sounding in the music
    changes by the onset or offset of one or more notes.

    This function returns the ordered set (start to end) of all partition points for a piece.
    """

    p_all = []

    time_cursor = events[0][0]
    point = PartitionPoint(time_cursor)

    for event in events:
        time = event["time"]
        pitch = event["pitch"]
        is_onset = event["onset"]

        if time == time_cursor:
            point.add_event(pitch, is_onset)

        else:
            p_all.append(deepcopy(point))

            time_cursor = time

            point = PartitionPoint(time)
            point.add_event(pitch, is_onset)

    p_all.append(deepcopy(point))

    # logger.debug(f"--- {len(p_all)} partition points ---")
    # for ix, p in enumerate(p_all):
    #     logger.debug(f"  p{ix}")
    #     p.pprint()

    return p_all


def score_minimal_segment(minimal_segment):
    scores = {}

    pc_occurrences = minimal_segment.get_pitch_class_occurrences()

    for template_name, (rotations, one_indices) in ALL_TEMPLATE_ROTATIONS.items():

        rotation_scores = []

        for ix, rotation in enumerate(rotations):
            P = 0  # positive evidence
            N = 0  # negative evidence
            M = 0  # misses

            for pc, n_occurences in pc_occurrences.items():
                if rotation[pc] == 1:
                    P += n_occurences

                elif rotation[pc] == 0:
                    N += n_occurences

            for el in set(one_indices[ix]) - set(pc_occurrences):
                M += 1

            S = P - (M + N)

            rotation_scores.append(S)

        # TODO: use dim7 resolution as tiebreaker (see fig 4 in Pardo 2002)
        best_rotation_score = max(rotation_scores)

        if template_name not in scores:
            scores[template_name] = best_rotation_score
        else:
            scores[template_name] += best_rotation_score

    return scores


def get_minimal_segments(p_all):
    """
    A minimal segment is the interval between two sequential partition points.
    """

    s_m = []

    s = MinimalSegment()

    s.set_start(p_all[0].time)
    s.update_pitches(p_all[0].onsets, 1)

    for point in p_all[1:]:
        s.set_end(point.time)

        pitches = s.pitches

        s_m.append(deepcopy(s))

        s = MinimalSegment()

        s.set_start(point.time)

        s.update_pitches(pitches, 1)
        s.update_pitches(point.onsets, 1)

        s.update_pitches(point.offsets, 0)

    logger.debug(f"\n--- {len(s_m)} minimal segments ---")
    for ix, s in enumerate(s_m):
        logger.debug(f"  s{ix}")
        # s.pprint()
        s.template_scores = score_minimal_segment(s)

    return s_m


def score_segment(segment):
    """Calculate the match scores between a segment and all templates.

    Returns the highest match.

    See Figure 3 in Pardo 2002
    """

    assert len(segment) > 0, "Empty segment"

    counter = Counter(segment[0].template_scores)
    for ms in segment[1:]:
        counter.update(Counter(ms.template_scores))

    # TODO: it's common for multiple templates to have the same score. How should be tiebreak?
    best_template, best_score = counter.most_common(1)[0]

    return best_score, best_template


def get_segment_notes(segment):
    notes = []

    for ms in segment:
        notes.extend(ms.get_note_occurences())

    return notes


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

    # In the graph, nodes are partition points and edges are segments
    G = nx.DiGraph()

    final_ix = len(p_all) - 1

    ui = 0  # index of the preceeding vertex

    for vi, p in enumerate(p_all):

        if vi in [0, final_ix]:
            G.add_node(vi, marked=1, time=p.time)
            continue

        uv_segment = s_m[ui:vi]  # preceding segment
        uv_notes = get_segment_notes(uv_segment)

        # Note: a minimal segment without pitches could be a drum break or a grand rest
        if len(uv_notes) == 0:
            logger.debug(f"  {vi}/{final_ix} - Continue: No pitches in segment")
            continue

        metrics = evaluate_chord(uv_notes)

        uv_score, uv_label = score_segment(uv_segment)

        wi = vi + 1  # index of the succeeding vertex
        vw_score, vw_label = score_segment(s_m[vi:wi])  # succeeding segment
        uw_score, uw_label = score_segment(s_m[ui:wi])  # full segment

        if uw_score < (uv_score + vw_score):
            logger.debug(
                f"  {vi}/{final_ix} - New: {uw_label} ({uw_score}) < {uv_label} ({uv_score}) + {vw_label} ({vw_score})"
            )

            edge_attributes = {
                "start_segment": ui,
                "end_segment": vi,
                "label": uv_label,
                "score": uv_score,
                "notes": uv_notes,  # TODO: add a str of midi notes?
                "metrics": metrics,
            }

            G.add_node(vi, marked=1, time=p.time)
            G.add_edge(ui, vi, **edge_attributes)

            ui = vi
        else:
            logger.debug(
                f"  {vi}/{final_ix} - Continue: {uw_label} ({uw_score}) >= {uv_label} ({uv_score}) + {vw_label} ({vw_score})"
            )

    final_segment = s_m[ui:final_ix]
    final_segment_notes = get_segment_notes(uv_segment)
    final_segment_metrics = {}

    if len(final_segment_notes) > 0:
        final_segment_metrics = evaluate_chord(final_segment_notes)

    final_score, final_label = score_segment(final_segment)

    final_edge_attributes = {
        "start_segment": ui,
        "end_segment": final_ix,
        "label": final_label,
        "score": final_score,
        "notes": final_segment_notes,
        "metrics": final_segment_metrics,
    }

    G.add_edge(ui, final_ix, **final_edge_attributes)

    logger.debug("\n--- Results ---")
    logger.debug(f"{len(G.edges)} segments")

    rows = []

    template_names = list(ALL_TEMPLATES)

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
            "notes": edge["notes"],
        }
        row.update(edge["metrics"])

        rows.append(row)

    logger.debug(f"Done in {time.time() - t0} seconds")

    return rows


def label_arrangement(filepath):
    logger.info(f"Labeling {filepath}")

    # for some files, pretty_midi throws a `RuntimeWarning: Tempo, Key or Time signature change events found on non-zero tracks.`
    # suppress these so as to maintain a clean tqdm progress bar
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        try:
            midi = pretty_midi.PrettyMIDI(filepath)
        except:
            logger.info(f"Failed loading file {filepath}")
            return None

    events = parse_events(midi)

    p_all = get_partition_points(events)

    s_m = get_minimal_segments(p_all)

    labels = segment_and_label(p_all, s_m)

    return labels


def write_labels(filepath, relabel):
    outpath = (
        os.path.splitext(filepath)[0]
        .replace(SMALL_LMD_PATH, OUTPUT_LABEL_DIR)
        .replace(DATA_DIR, OUTPUT_LABEL_DIR)
        + ".csv"
    )

    if os.path.exists(outpath) and not relabel:
        logger.info(f"Label for {filepath} exists. Skipping...")
        return {True: filepath}

    try:
        labels = label_arrangement(filepath)
    except:
        logger.info(f"Failed to label {filepath}")
        return {None: filepath}

    if not labels:
        logger.info(f"Failed for {filepath}")
        return {None: filepath}

    df = pd.DataFrame(labels)

    df[[f"icv{i}" for i in range(6)]] = pd.DataFrame(
        df.interval_class_vector.tolist(), index=df.index
    )

    df.to_csv(outpath, sep="\t")

    logger.debug(f"Labels saved to {outpath}")

    return {filepath: labels}


if __name__ == "__main__":

    if not os.path.isdir(OUTPUT_LABEL_DIR):
        os.makedirs(OUTPUT_LABEL_DIR)

    # Track TRPEWWD128F4263146
    # Me Quedaré Solo - Amistades Peligrosas
    # filepath = os.path.join(DATA_DIR, "e6abf19ddfb14f3ebe1a529b2c6d0061.mid")

    # Track TRPXORO128F4277D59
    # Roger And Out - Crosby_ Stills_ Nash & Young
    # filepath = os.path.join(DATA_DIR, "f8d865f301804304b33c5341371e4ee8.mid")

    # Track: Zillertaler Hochzeitsmarsch (TRPKJMG12903CC6F88)
    # Artist: Lichtensteiner (ARKJYIH124207824A3)
    filepath = os.path.join(DATA_DIR, "a59a9adf2605cafb505b125c45284159.mid")

    # filepath = os.path.join(DATA_DIR, "test_1.mid")
    # filepath = os.path.join(DATA_DIR, "test_2.mid")
    # filepath = os.path.join(DATA_DIR, "test_3.mid")
    # filepath = os.path.join(DATA_DIR, "2bar_1s_blocks.mid")
    # filepath = os.path.join(DATA_DIR, "3bar_1s_blocks.mid")
    # filepath = os.path.join(DATA_DIR, "4bar_1s_blocks.mid")
    # filepath = os.path.join(DATA_DIR, "16bar_1s_blocks.mid")

    labels = write_labels(filepath, relabel=True)
