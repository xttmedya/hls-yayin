#!/bin/bash

mkdir -p /app/public

# Nginx başlat
service nginx start

# Playlist dosyası
PLAYLIST="/app/playlist.m3u"

# Segment sıralı stream
while true; do
    while IFS= read -r LINE; do
        # Yorum satırlarını atla
        [[ "$LINE" =~ ^# ]] && continue
        # Boş satırları atla
        [[ -z "$LINE" ]] && continue

        echo "Oynatılıyor: $LINE"

        ffmpeg -re -i "$LINE" \
            -c copy \
            -f hls \
            -hls_time 6 \
            -hls_list_size 24 \
            -hls_flags delete_segments+append_list \
            -hls_segment_filename "/app/public/stream_%03d.ts" \
            /app/public/stream.m3u8
    done < "$PLAYLIST"
done