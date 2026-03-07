#!/bin/bash

mkdir -p /app/public

# Nginx başlat
service nginx start

# HLS kaynağı
INPUT="https://test-streams.mux.dev/x36xhzz/url_0/193039199_mp4_h264_aac_hd_7.m3u8"

# Direkt copy, encode yok, sadece HLS segmentlerini repack ediyor
ffmpeg -re -i "$INPUT" \
-c copy \
-f hls \
-hls_time 6 \
-hls_list_size 12 \
-hls_flags delete_segments+append_list \
-hls_segment_filename "/app/public/stream_%03d.ts" \
/app/public/stream.m3u8