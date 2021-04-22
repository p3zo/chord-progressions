import os

DATA_DIR = "/opt/chord-progressions/progression_extraction/data"
OUTPUT_LABEL_DIR = "/opt/chord-progressions/progression_extraction/output"
PLOT_DIR = "/opt/chord-progressions/progression_extraction/output/plots"

LMD_PATH = os.path.join(DATA_DIR, "lmd/lmd_matched")
LMDH5_PATH = os.path.join(DATA_DIR, "lmd/lmd_matched_h5")
SMALL_LMD_PATH = os.path.join(DATA_DIR, "lmd/small_lmd_matched")
SMALL_LMDH5_PATH = os.path.join(DATA_DIR, "lmd/small_lmd_matched_h5")
