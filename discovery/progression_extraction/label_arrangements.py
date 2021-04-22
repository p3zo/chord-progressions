"""Extracts chords from multiple midi files"""

import argparse
import csv
import glob
import os
import time
from functools import partial

from chord_progressions import logger
from progression_extraction import OUTPUT_LABEL_DIR, SMALL_LMD_PATH
from progression_extraction.label_arrangement import write_labels
from progression_extraction.parallel import process_parallel

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--relabel",
        type=bool,
        default=False,
        help="Relabel arrangements that have already been labeled",
    )
    parser.add_argument(
        "--parallel",
        type=bool,
        default=True,
        help="Parallelize labeling",
    )

    args = parser.parse_args()

    assert os.path.isdir(SMALL_LMD_PATH), "Invalid path to LMD Data"

    t0 = time.time()

    midi_filepaths = []
    for root, dirs, files in os.walk(SMALL_LMD_PATH):
        midi_filepaths.extend(glob.glob(os.path.join(root, "*.mid")))

    logger.info(f"Loaded {len(midi_filepaths)} filepaths in {time.time() - t0} seconds")

    t0 = time.time()

    func = partial(write_labels, args.relabel)

    if args.parallel:
        results = process_parallel(midi_filepaths, func, n_jobs=10)
    else:
        results = [func(i) for i in midi_filepaths]

    valids = [i for i in results if i]

    logger.info(f"Processed {len(valids)} tracks in {time.time() - t0} seconds")

    invalids = [i[None] for i in results if None in i]

    invalids_path = os.path.join(OUTPUT_LABEL_DIR, "invalids.csv")
    with open(invalids_path, "w") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(invalids)

    logger.info(f"Failure list saved to {invalids_path}")
