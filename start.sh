#!/bin/bash

# Log dosyası
LOG_FILE="/app/vlc.log"

# Playlist URL veya dosya
INPUT_PLAYLIST="https://test-streams.mux.dev/x36xhzz/url_8/193039199_mp4_h264_aac_fhd_7.m3u8"

# Render otomatik port
PORT=${PORT:-8080}

echo "VLC arka planda başlatılıyor..."
nohup cvlc "$INPUT_PLAYLIST" \
    --no-video-title-show \
    --loop \
    --quiet \
    --no-rt \
    --sout "#standard{access=http,mux=ts,dst=:$PORT}" \
    > "$LOG_FILE" 2>&1 &

echo "Stream hazır: http://<container-ip>:$PORT"
echo "Log: $LOG_FILE"

# Container’in ömrünü VLC’ye bağla
wait