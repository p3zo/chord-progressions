"""
Aggregates LMD arrangements from `LMD-matched` with MSD metadata from `LMD-matched metadata`.
"""

import glob
import os
import time
import warnings

import pretty_midi

import hdf5_getters
from chord_progressions import logger
from progression_extraction import (
    LMD_PATH,
    SMALL_LMD_PATH,
    SMALL_LMDH5_PATH,
    OUTPUT_LABEL_DIR,
)
from progression_extraction.msd import get_metadata_msd
from progression_extraction.parallel import process_parallel


def summarize_track(track_id):
    """
    Takes an ID for track in the MSD.
    Prints metadata from both the MSD and LMD.

    Follows https://nbviewer.jupyter.org/github/craffel/midi-ground-truth/blob/master/Statistics.ipynb
    """

    logger.info(f"TRACK: {track_id}")

    lmd_path = os.path.join(SMALL_LMD_PATH, "/".join(track_id[2:5]), track_id)
    lmd_mids = glob.glob(os.path.join(lmd_path, "*.mid"))

    msd_path = lmd_path.replace(SMALL_LMD_PATH, SMALL_LMDH5_PATH) + ".h5"

    try:
        msd_info = get_metadata_msd(msd_path)
        logger.info(msd_info)
    except:
        logger.info("No h5 file")

    logger.info(f"{len(lmd_mids)} arrangements at {lmd_path}")

    for m in lmd_mids:
        stats = get_metadata_lmd(m)
        logger.info(stats)

        label_path = m.replace(SMALL_LMD_PATH, OUTPUT_LABEL_DIR).replace(".mid", ".csv")
        print(f"label path {label_path}")
        if os.path.exists(label_path):
            logger.info("Labels exist")
        else:
            logger.info("No labels")


def get_metadata_lmd(midi_file):
    """
    Get metadata for a .mid file in the LMD dataset

    Takes a path to a MIDI file as input.
    Returns a dictionary containing information about the file.

    TODO: generalize this to not fail when run on any midi file
    """

    try:
        # for some files, pretty_midi throws a `RuntimeWarning: Tempo, Key or Time signature change events found on non-zero tracks.`
        # suppress these so as to maintain a clean tqdm progress bar
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            pm = pretty_midi.PrettyMIDI(midi_file)

            return {
                "n_instruments": len(pm.instruments),
                "program_numbers": [i.program for i in pm.instruments if not i.is_drum],
                "drums": [ix for ix, i in enumerate(pm.instruments) if i.is_drum],
                "key_numbers": [k.key_number for k in pm.key_signature_changes],
                "tempos": list(pm.get_tempo_changes()[1]),
                "time_signature_changes": pm.time_signature_changes,
                "end_time": pm.get_end_time(),
                "lyrics": [i.text for i in pm.lyrics],
            }

    # skip MIDI files if they are invalid.
    except Exception as e:
        print(f"Exception {e}")
        pass


def get_metadata_lmd_collection(glob_str=None):
    """
    Iterates over a set of midi files from the LMD dataset matching `glob_str`.

    If no `glob_str` is provided, iterates over the entire collection.
    """

    if not glob_str:
        glob_str = os.path.join(LMD_PATH, "*/*/*/*", "*.mid")

    midi_files = glob.glob(glob_str)
    print(f"# files: {len(midi_files)}")

    statistics = process_parallel(midi_files, get_metadata_lmd)

    # if an error occurred, None will be returned; filter those out
    statistics = [s for s in statistics if s is not None]
    print(f"# files parsed: {len(statistics)}")

    return statistics


def get_metadata_msd(filepath):
    """
    Get metadata for an .h5 file in the MSD dataset

    Takes a path to an. h5 file as input.
    Returns a dictionary containing information about the file.

    Follows http://millionsongdataset.com/pages/tutorial
    """

    h5 = hdf5_getters.open_h5_file_read(filepath)

    artist_name = hdf5_getters.get_artist_name(h5)
    artist_id = hdf5_getters.get_artist_id(h5)
    artist_terms = hdf5_getters.get_artist_terms(h5)

    # TODO: consider artist_terms_freq and artist_terms_weight
    # TODO: track-level terms instead of artist-level terms

    track_title = hdf5_getters.get_title(h5)
    track_id = hdf5_getters.get_track_id(h5)
    tempo = hdf5_getters.get_tempo(h5)

    h5.close()

    # TODO: some track_ids have multiple midi files in LMD - how to choose?
    # e.g. track_id TRRRUFD12903CD7092 has two midi files in LMD that are nearly the same
    # only diff I can see is instrument names on midi tracks
    print(f"Artist: {artist_name.decode()} ({artist_id.decode()})")
    print(f"Track: {track_title.decode()} ({track_id.decode()})")
    print(f"  {tempo} BPM")

    # TODO: lmd/small_lmd_matched_h5/P/R/R/TRPRRGW128F4265567.h5 does not match lmd/small_lmd_matched/P/R/R/TRPRRGW128F4265567/*

    return {
        "filepath": filepath,
        "artist_name": artist_name,
        "artist_id": artist_id,
        "artist_terms": artist_terms,
        "track_title": track_title,
        "track_id": track_id,
        "tempo": tempo,
    }


def get_metadata_lmd_collection(glob_str=None):
    """
    Iterates over a set of .h5 files from the MSD dataset matching `glob_str`.

    If no `glob_str` is provided, iterates over the entire collection.
    """

    if not glob_str:
        glob_str = os.path.join(SMALL_LMDH5_PATH, "*/*/*/*", "*.mid")

    assert os.path.isdir(SMALL_LMDH5_PATH), "Invalid path to MSD Data"

    t0 = time.time()

    filepaths = []
    for root, dirs, files in os.walk(SMALL_LMDH5_PATH):
        filepaths.extend(glob.glob(os.path.join(root, "*.h5")))

    print(f"Loaded filepaths in {time.time() - t0} seconds")

    fp = filepaths[1]

    return get_metadata_msd(fp)


def process_track(h5fp):
    result = {}

    result["meta"] = get_metadata_msd(h5fp)

    # TODO: join with lmd labels

    return result


if __name__ == "__main__":

    assert os.path.isdir(SMALL_LMDH5_PATH), "Invalid path to MSD Data"

    # t0 = time.time()

    # h5_filepaths = []
    # for root, dirs, files in os.walk(SMALL_LMDH5_PATH):
    #     h5_filepaths.extend(glob.glob(os.path.join(root, "*.h5")))
    # logger.info(f"Loaded {len(h5_filepaths)} filepaths in {time.time() - t0} seconds")

    # t0 = time.time()

    # results = process_parallel(h5_filepaths, process_track, n_jobs=10)

    # logger.info(f"Processed {len(results)} tracks in {time.time() - t0} seconds")
