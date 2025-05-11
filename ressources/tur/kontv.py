import re
import requests
from bs4 import BeautifulSoup

main_url = "https://www.kontv.com.tr/canli-yayin"
headers = {
    "User-Agent": "Mozilla/5.0"
}
output_lines = ["#EXTM3U"]
m3u8_link = None

try:
    response = requests.get(main_url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    iframe = soup.find("iframe")
    if not iframe or not iframe.get("src"):
        raise Exception("❌ iframe bulunamadı!")

    iframe_src = iframe["src"].replace("canlitv.ws", "canlitv.my")

    iframe_response = requests.get(iframe_src, headers=headers, timeout=10)
    iframe_response.raise_for_status()

    match = re.search(r'file\s*:\s*["\'](https://[^"\']+\.m3u8[^"\']*)["\']', iframe_response.text)
    if match:
        m3u8_link = match.group(1)
        output_lines.append(f"http://127.0.0.1:8000/proxy?url={m3u8_link}")
        print(f"✅ M3U8 linki bulundu: {m3u8_link}")
    else:
        print("❌ m3u8 linki bulunamadı.")

except Exception as e:
    print(f"⚠️ Hata: {e}")

if m3u8_link:
    with open("ressources/tur/kontv.m3u8", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print("✅ M3U8 dosyası kaydedildi.")
