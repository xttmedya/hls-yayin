#!/usr/bin/env python3
import requests
import subprocess
import time
import os
from urllib.parse import urljoin

# Remote playlist URL
SOURCE_M3U8 = "http://5.175.206.47/renderplaylist/playlist.m3u"
OUTPUT_DIR = "/app/public"
PLAYLIST = os.path.join(OUTPUT_DIR, "stream.m3u8")

SEGMENT_LIMIT = 20
FFMPEG = "ffmpeg"  # PATH'ten kullan

seen_segments = []
media_sequence = 0

os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_m3u8(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        lines = r.text.splitlines()
    except Exception as e:
        print("Playlist okunamadı:", e)
        return []

    segments = []
    duration = None

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            try:
                duration = float(line.split(":")[1].split(",")[0])
            except:
                duration = 6
        elif line and not line.startswith("#"):
            seg_url = urljoin(url, line)
            segments.append((duration, seg_url))
    return segments

def write_playlist():
    global media_sequence
    with open(PLAYLIST, "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write("#EXT-X-TARGETDURATION:6\n")
        f.write(f"#EXT-X-MEDIA-SEQUENCE:{media_sequence}\n")
        for seg in seen_segments:
            f.write(f"#EXTINF:{seg['duration']},\n")
            f.write(f"{seg['file']}\n")

def download_segment(url, filename):
    try:
        cmd = [
            FFMPEG,
            "-y",
            "-loglevel","error",
            "-i", url,
            "-c", "copy",
            filename
        ]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"Kullanılamayan segment: {url}")

while True:
    segments = parse_m3u8(SOURCE_M3U8)
    if not segments:
        time.sleep(3)
        continue

    for duration, seg_url in segments:
        name = os.path.basename(seg_url)
        if any(s["url"] == seg_url for s in seen_segments):
            continue

        out_file = os.path.join(OUTPUT_DIR, name)
        print("İndiriliyor:", seg_url)
        download_segment(seg_url, out_file)

        seen_segments.append({
            "url": seg_url,
            "file": name,
            "duration": duration
        })

        if len(seen_segments) > SEGMENT_LIMIT:
            old = seen_segments.pop(0)
            try:
                os.remove(os.path.join(OUTPUT_DIR, old["file"]))
            except:
                pass
            media_sequence += 1

        write_playlist()
        time.sleep(duration)