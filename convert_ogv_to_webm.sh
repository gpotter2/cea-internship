#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./convert_ogv_to_mp4.sh <input.ogv> <output.webm>"
    exit 1
fi

ffmpeg -i $1 \
       -c:v libx264 -preset veryslow -crf 22 \
       $2

ffmpeg -i $1 \
       -c:v libvpx -g 52 -b:v 4000k \
       -maxrate 4000k -bufsize 8000k -force_key_frames 00:00:00.000 \
       -f webm $2
