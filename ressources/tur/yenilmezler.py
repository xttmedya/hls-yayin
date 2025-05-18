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

# Başlık + link çiftleri
satirlar = [normalize(s) for s in film_liste.strip().splitlines() if s.strip()]
film_index = [(satirlar[i], satirlar[i+1]) for i in range(0, len(satirlar), 2)]

m3u8_path = os.path.join(os.path.dirname(__file__), "yenilmezler.m3u8")

def get_current_index_from_m3u8():
    if not os.path.exists(m3u8_path):
        return -1  # hiç yoksa baştan başla
    with open(m3u8_path, "r") as f:
        content = f.read()
    match = re.search(r'#EXTINF:-1,(.*)', content)
    if match:
        current_title = match.group(1).strip()
        for i, (title, _) in enumerate(film_index):
            if title[2:].strip() == current_title:
                return i
    return -1  # eşleşme yoksa baştan başla

def update_m3u8():
    idx = get_current_index_from_m3u8()
    next_idx = (idx + 1) % len(film_index)
    title, link = film_index[next_idx]
    content = f"#EXTM3U\n#EXTINF:-1,{title[2:]}\n{link}"
    with open(m3u8_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    update_m3u8()
