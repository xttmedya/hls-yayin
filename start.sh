#!/bin/bash

LOG_FILE="/app/play.log"

echo "Python playlist oynatıcı başlatılıyor..."
# Python foreground’da çalışacak
python3 /app/play.py > "$LOG_FILE" 2>&1