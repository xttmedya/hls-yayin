FROM ubuntu:22.04

# Temel paketler
RUN apt update && apt install -y \
    ffmpeg \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Start script ve playlist ekle
COPY start.sh /app/start.sh
COPY playlist.m3u /app/playlist.m3u

RUN chmod +x /app/start.sh
RUN mkdir -p /app/public

# Nginx konfigürasyonu
COPY default.conf /etc/nginx/sites-enabled/default

EXPOSE 8080

CMD ["bash", "/app/start.sh"]