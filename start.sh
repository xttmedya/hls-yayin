#!/bin/bash

# Log dosyası
LOG_FILE="/app/vlc.log"

# Kaynak HLS playlist
INPUT_PLAYLIST="https://test-streams.mux.dev/x36xhzz/url_8/193039199_mp4_h264_aac_fhd_7.m3u8"

# VLC arka planda başlatılıyor
echo "VLC arka planda başlatılıyor..."
nohup cvlc "$INPUT_PLAYLIST" \
    --no-video-title-show \
    --loop \
    --quiet \
    --sout "#standard{access=http,mux=ts,dst=:8080}" \
    > "$LOG_FILE" 2>&1 &

echo "Stream hazır: http://<container-ip>:8080"
echo "Log: $LOG_FILE"

# Container ömrünü VLC’ye bağla
wait