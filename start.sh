#!/bin/bash

mkdir -p /app/public

cat <<EOF > /etc/nginx/sites-enabled/default
server {
    listen 8080;
    location / {
        root /app/public;
        add_header Cache-Control no-cache;
    }
}
EOF

nginx

INPUT="https://test-streams.mux.dev/x36xhzz/url_0/193039199_mp4_h264_aac_hd_7.m3u8"

ffmpeg -re -i "$INPUT" -i xtt_movie.png \
-filter_complex "overlay=W-w-20:H-h-20" \
-c:a copy \
-c:v libx264 -preset veryfast -crf 23 \
-f hls \
-hls_time 6 \
-hls_list_size 6 \
-hls_flags delete_segments \
/app/public/stream.m3u8