# Dockerfile
FROM ubuntu:22.04

# Temel paketler
RUN apt update && apt install -y \
    vlc \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Start script ve playlist
COPY start.sh /app/start.sh
COPY playlist.m3u /app/playlist.m3u

RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["bash", "/app/start.sh"]