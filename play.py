import requests
import time
import os
from urllib.parse import urlparse, urljoin

SOURCE_M3U8 = "http://5.175.206.47/renderplaylist/playlist.m3u"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "public")
PLAYLIST = os.path.join(OUTPUT_DIR, "stream.m3u8")

SEGMENT_LIMIT = 10

seen_segments = []
media_sequence = 0

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_movie_list(url):

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        lines = r.text.splitlines()
    except Exception as e:
        print("Liste okunamadı:", e)
        return []

    movies = []

    for line in lines:
        line = line.strip()

        if line and not line.startswith("#"):
            movies.append(line)

    return movies


def parse_m3u8(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        lines = r.text.splitlines()
    except Exception as e:
        print("M3U8 okunamadı:", e)
        return []

    segments = []
    duration = None

    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"  # sadece domain + /

    for line in lines:
        line = line.strip()

        if line.startswith("#EXTINF"):
            try:
                duration = float(line.split(":")[1].split(",")[0])
            except:
                duration = 6
        elif line and not line.startswith("#"):
            # mutlak mı değil mi kontrol et
            if line.startswith("http"):
                seg_url = line
            else:
                # base_url ile birleştir ama sadece domain ile
                seg_url = urljoin(base_url, line)

            segments.append((duration, seg_url))

    return segments


def write_playlist():

    global media_sequence

    with open(PLAYLIST, "w") as f:

        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write("#EXT-X-TARGETDURATION:12\n")
        f.write("#EXT-X-PLAYLIST-TYPE:EVENT\n")
        f.write(f"#EXT-X-MEDIA-SEQUENCE:{media_sequence}\n")

        for seg in seen_segments:
            f.write(f"#EXTINF:{seg['duration']},\n")
            f.write(f"{seg['file']}\n")


def download_segment(url, filename):

    try:

        r = requests.get(url, timeout=10)
        r.raise_for_status()

        with open(filename, "wb") as f:
            f.write(r.content)

        return True

    except Exception as e:

        print("Segment indirilemedi:", url, e)
        return False


def reset_stream():

    global seen_segments, media_sequence
    if os.path.exists(PLAYLIST):
        os.remove(PLAYLIST)
    seen_segments.clear()
    media_sequence = 0

    # eski segmentleri sil
    for f in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, f)
        try:
            os.remove(path)
        except:
            pass

    # boş playlist oluştur
    with open(PLAYLIST, "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write("#EXT-X-TARGETDURATION:12\n")
        f.write("#EXT-X-PLAYLIST-TYPE:EVENT\n")
        f.write("#EXT-X-MEDIA-SEQUENCE:0\n")


movies = load_movie_list(SOURCE_M3U8)

if not movies:
    print("Film listesi boş.")
    exit()

movie_index = 0

while True:

    current_movie = movies[movie_index]

    print("\n===== Yeni Film Başlıyor =====")
    print(current_movie)

    reset_stream()
    time.sleep(1)

    finished = False

    while not finished:

        segments = parse_m3u8(current_movie)

        if not segments:
            print("Segment listesi alınamadı, sonraki filme geçiliyor.")
            break

        for duration, seg_url in segments:

            if any(s["url"] == seg_url for s in seen_segments):
                continue

            name = os.path.basename(urlparse(seg_url).path)
            out_file = os.path.join(OUTPUT_DIR, name)

            print("İndiriliyor:", seg_url)

            start = time.time()

            success = download_segment(seg_url, out_file)

            download_time = time.time() - start

            if not success:
                print("Segment hatası -> film atlanıyor")
                finished = True
                break

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

            wait_time = duration - download_time

            if wait_time > 0:
                time.sleep(wait_time)

        if finished:
            break

        # film bitti kontrolü
        if segments[-1][1] in [s["url"] for s in seen_segments]:
            finished = True

    movie_index += 1

    if movie_index >= len(movies):
        movie_index = 0
        print("\n===== LİSTE BAŞA DÖNDÜ =====")