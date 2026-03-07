#!/bin/bash

# ------------------------------
# Dizinler
# ------------------------------
mkdir -p /app/public
TEMP_DIR="/app/temp"
mkdir -p "$TEMP_DIR"

# Nginx başlat
service nginx start

# ------------------------------
# Kaynak HLS
# ------------------------------
INPUT="https://test-streams.mux.dev/x36xhzz/url_8/193039199_mp4_h264_aac_fhd_7.m3u8"
OUTPUT_M3U8="/app/public/stream.m3u8"

# ------------------------------
# Orijinal playlist indir
# ------------------------------
curl -s "$INPUT" -o "$TEMP_DIR/original.m3u8"

# ------------------------------
# Playlist başlat
# ------------------------------
echo "#EXTM3U" > "$OUTPUT_M3U8"
echo "#EXT-X-VERSION:3" >> "$OUTPUT_M3U8"
echo "#EXT-X-PLAYLIST-TYPE:LIVE" >> "$OUTPUT_M3U8"

# Target duration otomatik ayarla (en uzun segment)
MAX_DURATION=$(grep "#EXTINF" "$TEMP_DIR/original.m3u8" \
               | sed 's/#EXTINF:\(.*\),/\1/' \
               | awk '{if($1>max){max=$1}}END{print int(max+1)}')
echo "#EXT-X-TARGETDURATION:$MAX_DURATION" >> "$OUTPUT_M3U8"

# ------------------------------
# Segmentleri sırayla indir ve kopyala
# ------------------------------
SEGMENTS=($(grep -v "#" "$TEMP_DIR/original.m3u8"))
SEGMENT_INDEX=0

for SEGMENT_URL in "${SEGMENTS[@]}"; do
    SEGMENT_NAME=$(printf "stream_%03d.ts" "$SEGMENT_INDEX")
    echo "Processing segment $SEGMENT_INDEX: $SEGMENT_URL"

    # Segmenti indir
    curl -s -f -o "$TEMP_DIR/$SEGMENT_NAME.orig" "$SEGMENT_URL"

    if [ ! -f "$TEMP_DIR/$SEGMENT_NAME.orig" ]; then
        echo "!!! Segment indirilemedi: $SEGMENT_URL"
        continue
    fi

    # FFmpeg ile sadece copy
    ffmpeg -y -i "$TEMP_DIR/$SEGMENT_NAME.orig" -c copy "/app/public/$SEGMENT_NAME"

    # Süreyi al (orijinal segment süresini korumak için)
    DURATION=$(ffprobe -v error -select_streams v:0 -show_entries format=duration -of csv=p=0 "/app/public/$SEGMENT_NAME")
    DURATION=$(printf "%.3f" "$DURATION")

    # Playlist’e ekle
    echo "#EXTINF:$DURATION," >> "$OUTPUT_M3U8"
    echo "$SEGMENT_NAME" >> "$OUTPUT_M3U8"

    SEGMENT_INDEX=$((SEGMENT_INDEX + 1))
done

# Playlist’i bitir
echo "#EXT-X-ENDLIST" >> "$OUTPUT_M3U8"

# ------------------------------
# Temp temizle
# ------------------------------
rm -rf "$TEMP_DIR"

echo "Live-like stream hazır: $OUTPUT_M3U8"