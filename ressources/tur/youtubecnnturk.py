import yt_dlp

def get_youtube_live_m3u8(video_url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'force_generic_extractor': False,
        'simulate': True,
        'format': 'best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        if 'url' in info:
            return info['url']
        elif 'formats' in info:
            for fmt in info['formats']:
                if fmt.get('ext') == 'mp4' and 'url' in fmt:
                    return fmt['url']
    return None

# YouTube canlı yayın linki
video_url = 'https://www.youtube.com/watch?v=VXMR3YQ7W3s'  # Bunu değiştirebilirsiniz
m3u8_url = get_youtube_live_m3u8(video_url)

# .m3u8 dosyasına kaydet
with open("ressources/tur/youtube.m3u8", "w") as f:
    f.write(m3u8_url)

print(f"Canlı yayın m3u8 URL'si kaydedildi: {m3u8_url}")
