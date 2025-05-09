import requests

# NTV'nin base URL'si
ntv_base_url = "https://mn-nl.mncdn.com/dogusdyg_ntv/"

# Başlangıç URL'si
initial_url = "https://dygvideo.dygdigital.com/live/hls/kralpop?m3u8"

# M3U8 dosyasını almak ve düzenlemek için kullanılan fonksiyon
def fetch_and_save_m3u8(base_url, modified_url, output_file):
    try:
        # URL'den içerik al
        content_response = requests.get(modified_url)
        content_response.raise_for_status()  # Hata varsa burada fırlatılır.
        content = content_response.text

        # İçeriği satırlara ayır ve her bir satırı işle
        lines = content.split("\n")
        modified_content = ""

        for line in lines:
            if line.startswith("live_"):
                # Tam URL'yi oluştur
                full_url = base_url + line
                modified_content += full_url + "\n"
            else:
                modified_content += line + "\n"
        
        # Dosyaya kaydet
        with open(output_file, "w") as f:
            f.write(modified_content)
        print(f"Saved to {output_file}")

    except requests.RequestException as e:
        print(f"Error fetching {output_file}: {e}")

try:
    # Başlangıç URL'sini al
    response = requests.get(initial_url)
    response.raise_for_status()

    # Final URL'yi al
    final_url = response.url
    # NTV için URL'yi düzenle
    ntv_modified_url = final_url.replace("dogusdyg_kralpoptv/dogusdyg_kralpoptv.smil/playlist", "dogusdyg_ntv/live")

    # M3U8 dosyasını al ve kaydet
    fetch_and_save_m3u8(ntv_base_url, ntv_modified_url, "ressources/tur/ntv.m3u8")

except requests.RequestException as e:
    print(f"Initial URL error: {e}")
