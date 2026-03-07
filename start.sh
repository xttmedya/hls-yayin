#!/bin/bash
LOG_FILE="/app/play.log"

# Nginx başlat
service nginx start

echo "Python playlist oynatıcı başlatılıyor..."
exec python3 /app/play.py