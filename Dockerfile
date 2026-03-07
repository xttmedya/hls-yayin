FROM ubuntu:22.04

# Temel paketler
RUN apt update && apt install -y \
    ffmpeg \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Scriptler
COPY start.sh /app/start.sh
COPY play.py /app/play.py

# HLS dosyaları için klasör
RUN mkdir -p /app/public
RUN chmod +x /app/start.sh

EXPOSE 8080

# Python player foreground'da çalışacak
CMD ["bash", "/app/start.sh"]