# ntv.py
import requests
import os

# Base URL (mutlaka slash ile biter!)
ntv_base_url = "https://mn-nl.mncdn.com/dogusdyg_ntv/"
initial_url = "https://dygvideo.dygdigital.com/live/hls/kralpop?m3u8"

def fetch_and_save_m3u8(base_url, modified_url, output_file):
    try:
        response = requests.get(modified_url, timeout=10)
        response.raise_for_status()
        content = response.text

        modified_lines = []
        for line in content.splitlines():
            if line.startswith("live_"):
                full_url = base_url + line
                modified_lines.append(full_url)
            else:
                modified_lines.append(line)

        # Hedef klasör yoksa oluştur
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(modified_lines) + "\n")

        print(f"[✓] Saved to {output_file}")

    except requests.RequestException as e:
        print(f"[!] Error fetching {output_file}: {e}")

try:
    # İlk URL'den yönlendirme al
    response = requests.get(initial_url, timeout=10)
    response.raise_for_status()

    # Final URL (redirect edilen)
    final_url = response.url

    # NTV URL’sine çevir
    if "dogusdyg_kralpoptv" in final_url:
        ntv_modified_url = final_url.replace(
            "dogusdyg_kralpoptv/dogusdyg_kralpoptv.smil/playlist",
            "dogusdyg_ntv/live"
        )
        fetch_and_save_m3u8(ntv_base_url, ntv_modified_url, "ressources/tur/ntv.m3u8")
    else:
        print("[!] Unexpected final URL structure")

except requests.RequestException as e:
    print(f"[!] Initial URL error: {e}")
