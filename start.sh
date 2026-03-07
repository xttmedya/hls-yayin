#!/bin/bash

mkdir -p /app/public

service nginx start

INPUT="https://test-streams.mux.dev/x36xhzz/url_0/193039199_mp4_h264_aac_hd_7.m3u8"
LOGO="/app/xtt_movie.png"

ffmpeg -re -i "$INPUT" -i "$LOGO" \
-filter_complex "overlay=10:10,format=yuv420p" \
-c:v libx264 \
-preset superfast \
-tune zerolatency \
-profile:v main \
-level 4.0 \
-r 25 \
-g 50 \
-b:v 1000k \
-maxrate 1200k \
-bufsize 1500k \
-c:a aac \
-b:a 96k \
-ac 2 \
-ar 44100 \
-f hls \
-hls_time 6 \
-hls_list_size 12 \
-hls_flags delete_segments \
-hls_segment_filename "/app/public/stream_%03d.ts" \
/app/public/stream.m3u8