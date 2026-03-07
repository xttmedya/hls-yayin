#!/bin/bash

mkdir -p /app/public

# Nginx başlat
service nginx start

# Kaynak listesi
PLAYLIST="/app/playlist.m3u"

# HLS output
OUTPUT_DIR="/app/public"
OUTPUT_FILE="$OUTPUT_DIR/stream.m3u8"

# Sonsuz döngü ile ard arda oynatma
while true; do
    while read -r line; do
        # Satır boş veya yorumsa geç
        [[ -z "$line" || "$line" =~ ^# ]] && continue

        echo "Processing: $line"

        # Mevcut playlist sıfırlanır
        rm -f "$OUTPUT_FILE"

        # FFmpeg ile direkt copy, encode yok
        ffmpeg -re -i "$line" \
            -c copy \
            -f hls \
            -hls_time 6 \
            -hls_list_size 24 \
            -hls_flags delete_segments+append_list \
            -hls_segment_filename "$OUTPUT_DIR/stream_%03d.ts" \
            "$OUTPUT_FILE"

        echo "Finished: $line"
    done < "$PLAYLIST"
done