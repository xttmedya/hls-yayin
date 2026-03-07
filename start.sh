#!/bin/bash

# Log dosyası
LOG_FILE="/app/vlc.log"

# Playlist
INPUT_PLAYLIST="/app/playlist.m3u"

echo "VLC arka planda başlatılıyor..."
echo "Log: $LOG_FILE"

# Render'da otomatik port $PORT kullanılıyor
nohup cvlc "$INPUT_PLAYLIST" \
    --no-video-title-show \
    --loop \
    --quiet \
    --sout "#standard{access=http,mux=ts,dst=:$PORT}" \
    > "$LOG_FILE" 2>&1 &

echo "Stream hazır: http://<container-ip>:$PORT"
tail -f "$LOG_FILE"