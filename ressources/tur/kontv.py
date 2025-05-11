import re
import requests
from bs4 import BeautifulSoup

# Ana sayfa
main_url = "https://www.kontv.com.tr/canli-yayin"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
output_lines = ["#EXTM3U"]
m3u8_link = None  # Başlangıçta m3u8 linki None olarak tanımlanıyor.

try:
    # Ana sayfayı çek
    response = requests.get(main_url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # iframe src'sini al
    iframe = soup.find("iframe")
    if not iframe or not iframe.get("src"):
        raise Exception("❌ iframe bulunamadı!")

    iframe_src = iframe["src"]

    # .ws uzantısı SSL hatası veriyor, .my ile değiştir
    fixed_iframe_url = iframe_src.replace("canlitv.ws", "canlitv.my")

    # iframe içeriğini al
    iframe_response = requests.get(fixed_iframe_url, headers=headers, timeout=10)
    iframe_response.raise_for_status()
    iframe_html = iframe_response.text

    # m3u8 linkini ayıkla
    match = re.search(r'file\s*:\s*["\'](https://[^"\']+\.m3u8[^"\']*)["\']', iframe_html)
    if match:
        m3u8_link = match.group(1)
        output_lines.append(m3u8_link)
        print(f"✅ M3U8 linki bulundu: {m3u8_link}")
    else:
        print("❌ m3u8 linki bulunamadı.")
        
except requests.exceptions.RequestException as e:
    print(f"🛑 HTTP hatası: {e}")
except Exception as e:
    print(f"⚠️ Hata: {e}")

# Eğer m3u8 linki başarıyla bulunmuşsa dosyayı yaz
if m3u8_link:
    try:
        with open("kontv.m3u8", "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        print("✅ M3U8 dosyası başarıyla kaydedildi.")
    except Exception as e:
        print(f"⚠️ Dosya kaydedilirken hata oluştu: {e}")
else:
    print("❌ M3U8 linki bulunamadığı için dosya kaydedilmedi.")

