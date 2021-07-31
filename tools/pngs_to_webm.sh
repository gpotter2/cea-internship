#!/bin/bash

ffmpeg -framerate 24 -pattern_type glob -i '*.png' \
  -pix_fmt yuv420p \
  -c:v libvpx \
  -qmin 0 -qmax 25 \
  -crf 4 -b:v 1M -vf scale=1280:-2 -an -threads 0 \
  -movflags +faststart \
  out.webm
