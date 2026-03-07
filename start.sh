#!/bin/bash

LOG_FILE="/app/play.log"

echo "Python playlist oynatıcı başlatılıyor..."
# Play.py'i background’da çalıştır
nohup python3 /app/play.py > "$LOG_FILE" 2>&1 &

echo "HTTP server başlatılıyor..."
# HTTP server foreground’da, Render container için
exec python3 -m http.server 8080 --directory /app/public