#!/usr/bin/env python3
import subprocess
import time
import requests

# Remote playlist URL
REMOTE_PLAYLIST = "http://5.175.206.47/renderplaylist/playlist.m3u"

# Local playback / HLS ayarları
OUTPUT_M3U8 = "/app/public/stream.m3u8"
SEGMENT_PATTERN = "/app/public/stream_%03d.ts"

# Oynatılan son film indeksi
last_index = -1
current_links = []

def fetch_playlist():
    """Uzak playlisti indirir ve linkleri döndürür."""
    try:
        resp = requests.get(REMOTE_PLAYLIST, timeout=10)
        resp.raise_for_status()
        links = []
        for line in resp.text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                links.append(line)
        return links
    except Exception as e:
        print(f"Playlist indirilemedi: {e}")
        return []

def play_link(link):
    """FFmpeg ile HLS stream oluşturur."""
    print(f"Oynatılıyor: {link}")
    cmd = [
        "ffmpeg",
        "-re",
        "-i", link,
        "-c", "copy",
        "-f", "hls",
        "-hls_time", "6",
        "-hls_list_size", "24",
        "-hls_flags", "delete_segments+append_list",
        "-hls_segment_filename", SEGMENT_PATTERN,
        OUTPUT_M3U8
    ]
    subprocess.run(cmd, check=True)

def find_start_index(old_links, new_links, last_index):
    """Oynatılan filmi bul, yoksa baştan başlat."""
    if last_index >= len(old_links):
        return 0
    if last_index == -1:
        return 0
    last_link = old_links[last_index]
    if last_link in new_links:
        return new_links.index(last_link) + 1
    else:
        return 0

if __name__ == "__main__":
    current_links = fetch_playlist()
    if not current_links:
        print("Playlist boş! Çıkılıyor.")
        exit(1)

    while True:
        # Playlisti güncelle
        new_links = fetch_playlist()
        if new_links:
            start_index = find_start_index(current_links, new_links, last_index)
            current_links = new_links
        else:
            start_index = 0

        # Oynatma döngüsü
        for idx in range(start_index, len(current_links)):
            link = current_links[idx]
            try:
                play_link(link)
            except subprocess.CalledProcessError:
                print(f"FFmpeg hata verdi, atlanıyor: {link}")
                time.sleep(1)
            last_index = idx

        # Tüm liste bitti, tekrar başa dönmeden önce bekle
        time.sleep(5)