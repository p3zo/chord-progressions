#!/bin/bash

: '
melody name, bpm
00_forgiveness-chorus, 125
01_D-2-of-3-2-poly, 84
02_hbd-in-c, 85
03_chorale, 65
what_a_sin, 97.77
'
python harmonize.py \
    --melody_filepath="input_melodies/02_hbd-in-c.mid" \
    --bpm=85 \
    --output_dir="output_harmonies" \
    --n_progressions=15
