#!/usr/bin/env python3
import subprocess
import time

playlist_file = "/app/playlist.m3u"
output_m3u8 = "/app/public/stream.m3u8"
segment_pattern = "/app/public/stream_%03d.ts"

def get_links(file_path):
    links = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                links.append(line)
    return links

def play_link(link):
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
        "-hls_segment_filename", segment_pattern,
        output_m3u8
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    links = get_links(playlist_file)
    if not links:
        print("Playlist boş!")
        exit(1)

    while True:
        for link in links:
            try:
                play_link(link)
            except subprocess.CalledProcessError:
                print(f"FFmpeg hata verdi, atlanıyor: {link}")
                time.sleep(1)