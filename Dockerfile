FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y ffmpeg nginx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY xtt_movie.png /app/
COPY start.sh /app/

RUN chmod +x /app/start.sh

RUN mkdir /app/public

EXPOSE 8080

CMD ["/app/start.sh"]