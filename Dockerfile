FROM ubuntu:22.04

# Temel paketler
RUN apt update && apt install -y \
    ffmpeg \
    nginx \
    python3 \
    python3-pip \
    curl \
    && python3 -m pip install --no-cache-dir requests \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Scriptler ve nginx config
COPY start.sh /app/start.sh
COPY default.conf /etc/nginx/sites-enabled/default
COPY play.py /app/play.py

# HLS dosyaları için klasör
RUN mkdir -p /app/public
RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]