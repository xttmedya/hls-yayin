#!/bin/bash

mkdir -p /app/public

service nginx start

INPUT="https://vidmody.com/mm/tt14088510/main_1080/index-v1-a1.gif"
LOGO="/app/xtt_movie.png"

ffmpeg -re -i "$INPUT" -i "$LOGO" \
-filter_complex "overlay=30:20,format=yuv420p" \
-c:v libx264 \
-preset veryfast \
-crf 20 \
-c:a copy \
-f hls \
-hls_time 6 \
-hls_list_size 24 \
-hls_flags delete_segments+append_list \
-hls_segment_filename "/app/public/stream_%03d.ts" \
/app/public/stream.m3u8