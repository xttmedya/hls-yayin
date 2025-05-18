import os
import re

film_liste = r"""
# Yenilmezler
https://vidmody.com/vs/tt2207090
# Yenilmezler 2 Ultron Çağı
https://p1.photofunny.org/v/v2w7dxo0f12d/master.m3u8
# Yenilmezler 3 Sonsuzluk Savaşı
https://p1.photomag.biz/v/zm8megwu2bfj/master.m3u8
# Yenilmezler 4 Son Oyun
https://vidmody.com/vs/tt4154796
"""

def normalize(text):
    return re.sub(r'\s+', ' ', text.strip())

# Filmleri (ad, link) çiftlerine ayır
satirlar = [normalize(s) for s in film_liste.strip().splitlines() if s.strip()]
film_index = [(satirlar[i], satirlar[i + 1]) for i in range(0, len(satirlar), 2)]

m3u8_path = os.path.join(os.path.dirname(__file__), "yenilmezler.m3u8")

def get_current_index():
    if not os.path.exists(m3u8_path):
        return -1
    with open(m3u8_path, "r", encoding="utf-8") as f:
        current_link = f.read().strip()
    for i, (_, link) in enumerate(film_index):
        if link == current_link:
            return i
    return -1

def get_next_index():
    current = get_current_index()
    return 0 if current == -1 else (current + 1) % len(film_index)

def update_m3u8():
    idx = get_next_index()
    ad, link = film_index[idx]
    with open(m3u8_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n" + link + "\n")
    print(f"🎬 Playlist güncellendi → {ad[2:]}")

if __name__ == "__main__":
    update_m3u8()
