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

# Yardımcı fonksiyon: boşlukları temizler
def normalize(text):
    return re.sub(r'\s+', ' ', text.strip())

# Filmleri (başlık + link) şeklinde grupla
satirlar = [normalize(s) for s in film_liste.strip().splitlines() if s.strip()]
film_index = [(satirlar[i], satirlar[i+1]) for i in range(0, len(satirlar), 2)]

# Dosya yolları
m3u8_path = os.path.join(os.path.dirname(__file__), "yenilmezler.m3u8")
state_path = os.path.join(os.path.dirname(__file__), "yenilmezler_state.txt")

def get_next_index():
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            try:
                idx = int(f.read().strip())
            except:
                idx = 0
    else:
        idx = 0
    next_idx = (idx + 1) % len(film_index)
    with open(state_path, "w") as f:
        f.write(str(next_idx))
    return next_idx

def update_m3u8():
    idx = get_next_index()
    ad, link = film_index[idx]
    content = f"#EXTM3U\n#EXTINF:-1,{ad[2:]}\n{link}"
    with open(m3u8_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    update_m3u8()
