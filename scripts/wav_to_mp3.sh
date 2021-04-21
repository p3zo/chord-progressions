#!/bin/bash

WAV_DIR=output/wavs

for f in $WAV_DIR/*.wav
do
  BASE=${f%.wav}
  ffmpeg -i $f -vn -ar 44100 -ac 2 -ab 192k -f mp3 $BASE.mp3
done
