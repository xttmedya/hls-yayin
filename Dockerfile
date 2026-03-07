FROM ubuntu:22.04

RUN apt update && apt install -y \
    ffmpeg \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# requests modülünü yükle
RUN python3 -m pip install --no-cache-dir requests

WORKDIR /app

COPY start.sh /app/start.sh
COPY play.py /app/play.py

RUN mkdir -p /app/public
RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["bash", "/app/start.sh"]