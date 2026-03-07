#!/usr/bin/env python3
import subprocess
import time
import requests

PLAYLIST_FILE = "/app/playlist.m3u"
OUTPUT_M3U8 = "/app/public/stream.m3u8"
SEGMENT_PATTERN = "/app/public/stream_%03d.ts"
RETRY_COUNT = 3
TIMEOUT = 5

def get_links(file_path):
    links = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                links.append(line)
    return links

def is_alive(url, timeout=TIMEOUT):
    """Link erişilebilir mi kontrol et"""
    for _ in range(RETRY_COUNT):
        try:
            r = requests.head(url, timeout=timeout, allow_redirects=True)
            if r.status_code == 200:
                return True
        except requests.RequestException:
            time.sleep(0.5)
    return False

def play_links(links):
    """Sadece erişilebilir linkleri HLS’e dönüştür"""
    alive_links = [l for l in links if is_alive(l)]
    if not alive_links:
        print("Hiçbir link erişilebilir değil, bekleniyor...")
        return

    # FFmpeg input dosyası oluştur
    with open("/tmp/temp_playlist.txt", "w") as f:
        for l in alive_links:
            f.write(f"{l}\n")

    cmd = [
        "ffmpeg",
        "-protocol_whitelist", "file,http,https,tcp,tls,crypto",
        "-re",
        "-f", "concat",
        "-safe", "0",
        "-i", "/tmp/temp_playlist.txt",
        "-c", "copy",
        "-f", "hls",
        "-hls_time", "6",
        "-hls_list_size", "24",
        "-hls_flags", "delete_segments+append_list",
        "-hls_segment_filename", SEGMENT_PATTERN,
        OUTPUT_M3U8
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg hata verdi: {e}")

if __name__ == "__main__":
    while True:
        links = get_links(PLAYLIST_FILE)
        play_links(links)
        # Playlist’in başına dönüp sürekli döngü
        time.sleep(1)