#!/bin/bash

LOG_FILE="/app/play.log"

# Nginx başlatılıyor
service nginx start

# Python playlist oynatıcı arka planda
nohup python3 /app/play.py > "$LOG_FILE" 2>&1 &

echo "Stream hazır: http://localhost:8080/stream.m3u8"

# Foreground’da Nginx’i çalıştır
exec nginx -g 'daemon off;'