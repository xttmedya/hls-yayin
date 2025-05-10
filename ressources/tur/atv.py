import streamlink
import ast

# Yayın adresi
streams = streamlink.streams('https://www.atv.com.tr/canli-yayin')
unique_urls = set()

# URL'leri topla
for stream in streams.values():
    stream_str = str(stream)
    if stream_str.startswith("<HLSStream [") and stream_str.endswith("]>"):
        list_str = stream_str[len("<HLSStream "):-1]
        try:
            urls = ast.literal_eval(list_str)
            for url in urls:
                if url.startswith("http"):
                    unique_urls.add(url)
        except Exception as e:
            print(f"Hata: Liste ayrıştırılamadı -> {e}")

# Kaliteli ve kalitesiz linkleri ayır
with_quality = []
without_quality = []

for url in sorted(unique_urls):
    if any(q in url for q in ['240p', '360p', '480p', '720p', '1080p']):
        with_quality.append(url)
    else:
        without_quality.append(url)

# Çözünürlük bilgileri
quality_map = {
    '1080p': ('1920x1080', 3000000),
    '720p':  ('1280x720', 1500000),
    '480p':  ('854x480', 900000),
    '360p':  ('640x360', 800000),
    '240p': ('426x240', 500000),
}

# .m3u8 içeriği
output_lines = ["#EXTM3U", "#EXT-X-VERSION:3"]

# Öncelik sırasına göre yaz (yüksek çözünürlükler önce)
if with_quality:
    for quality in ['1080p', '720p', '480p', '360p']:
        res, bw = quality_map[quality]
        for url in with_quality:
            if quality in url:
                output_lines.append(f"#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH={bw},RESOLUTION={res}")
                output_lines.append(url)
# Kalitesiz varsa sadece onu yaz
elif without_quality:
    for url in without_quality:
        output_lines.append("#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1000000")
        output_lines.append(url)

# Dosyaya yaz
with open("ressources/tur/atv.m3u8", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(".m3u8 dosyası oluşturuldu.")
