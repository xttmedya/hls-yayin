#!/bin/bash

LOG_FILE="/app/play.log"

# Nginx başlat
service nginx start

echo "Python playlist oynatıcı başlatılıyor..."
nohup python3 /app/play.py > "$LOG_FILE" 2>&1 &

echo "Stream hazır: http://<container-ip>:8080/stream.m3u8"
echo "Log: $LOG_FILE"

wait