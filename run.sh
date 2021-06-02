#!/bin/bash

python3 scripts/generate.py \
    --n_segments=5 \
    --pct_notes_common=1 \
    --note_range_low=36 \
    --note_range_high=84 \
    --duration_min=1 \
    --duration_max=1 \
    --duration_interval=0.5 \
    --n_overtones=1
