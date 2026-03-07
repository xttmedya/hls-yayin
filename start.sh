#!/bin/bash

mkdir -p /app/public
service nginx start

INPUT="https://test-streams.mux.dev/x36xhzz/url_0/193039199_mp4_h264_aac_hd_7.m3u8"
LOGO="/app/xtt_movie.png"
TEMP_DIR="/app/temp"
mkdir -p "$TEMP_DIR"

# Orijinal playlist’i indir
curl -s "$INPUT" -o "$TEMP_DIR/original.m3u8"

# Yeni playlist başlat
OUTPUT_M3U8="/app/public/stream.m3u8"
echo "#EXTM3U" > "$OUTPUT_M3U8"
echo "#EXT-X-VERSION:3" >> "$OUTPUT_M3U8"
echo "#EXT-X-PLAYLIST-TYPE:VOD" >> "$OUTPUT_M3U8"

# Target duration otomatik ayarlanacak (en uzun segment)
MAX_DURATION=$(grep "#EXTINF" "$TEMP_DIR/original.m3u8" | sed 's/#EXTINF:\(.*\),/\1/' | awk '{if($1>max){max=$1}}END{print int(max+1)}')
echo "#EXT-X-TARGETDURATION:$MAX_DURATION" >> "$OUTPUT_M3U8"

# Segmentleri sırayla işle
SEGMENT_INDEX=0
grep -v "#" "$TEMP_DIR/original.m3u8" | while read -r SEGMENT_URL; do
    SEGMENT_NAME=$(printf "stream_%03d.ts" "$SEGMENT_INDEX")
    echo "Processing segment $SEGMENT_INDEX: $SEGMENT_URL"

    # İndir
    curl -s -o "$TEMP_DIR/$SEGMENT_NAME.orig" "$SEGMENT_URL"

    # Logo ekle
    ffmpeg -y -i "$TEMP_DIR/$SEGMENT_NAME.orig" -i "$LOGO" \
        -filter_complex "overlay=10:10,format=yuv420p" \
        -c:v libx264 -preset superfast -tune zerolatency -profile:v main -level 4.0 \
        -r 25 -g 50 -b:v 1000k -maxrate 1200k -bufsize 1500k \
        -c:a aac -b:a 96k -ac 2 -ar 44100 \
        "/app/public/$SEGMENT_NAME"

    # Segment süresini al
    DURATION=$(ffprobe -v error -select_streams v:0 -show_entries format=duration -of csv=p=0 "/app/public/$SEGMENT_NAME")
    DURATION=$(printf "%.3f" "$DURATION")

    # Playlist’e ekle
    echo "#EXTINF:$DURATION," >> "$OUTPUT_M3U8"
    echo "$SEGMENT_NAME" >> "$OUTPUT_M3U8"

    SEGMENT_INDEX=$((SEGMENT_INDEX + 1))
done

echo "#EXT-X-ENDLIST" >> "$OUTPUT_M3U8"

# Temp temizle
rm -rf "$TEMP_DIR"

echo "Stream hazır: $OUTPUT_M3U8"