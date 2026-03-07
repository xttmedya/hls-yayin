#!/bin/bash

# ------------------------------
# VLC GUI olmadan arka planda stream
# ------------------------------
INPUT_PLAYLIST="https://test-streams.mux.dev/x36xhzz/url_8/193039199_mp4_h264_aac_fhd_7.m3u8"

# Log dizini ve dosya
LOG_FILE="/app/vlc.log"

# VLC ile stream başlat (GUI yok, arka planda)
nohup cvlc "$INPUT_PLAYLIST" \
    --no-video-title-show \
    --loop \
    --quiet \
    --sout "#standard{access=http,mux=ts,dst=:8080}" \
    > "$LOG_FILE" 2>&1 &

echo "VLC arka planda başlatıldı. Stream: http://<container-ip>:8080"
echo "Log: $LOG_FILE"