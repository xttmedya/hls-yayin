FROM ubuntu:22.04

RUN apt update && apt install -y \
    ffmpeg \
    nginx \
    python3 \
    python3-pip \
    curl \
	&& python3 -m pip install --no-cache-dir requests \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY start.sh /app/start.sh
COPY default.conf /etc/nginx/sites-enabled/default
COPY play.py /app/play.py

RUN chmod +x /app/start.sh
RUN mkdir -p /app/public

EXPOSE 8080

CMD ["bash", "/app/start.sh"]