# İki Python betiğini birleştiren ve tüm işlemleri sırasıyla yapan tek dosya.
import requests
from urllib.parse import urlparse
from cryptography.fernet import Fernet
import base64
from html import escape
import re
import os
from datetime import datetime
import shutil
import gzip

# === Ayarlar ===
url = "http://supersports.hdiptv.cam:8000/get.php?username=V91CHnEZGl&password=IUjxwiRK6L&type=m3u_plus&output=m3u8"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
kategori_filtre_listesi = '''
TURK BELGESEL
TURK COCUK
TURK DINI
TURK EGITIM
TURK HABER
TURK MUZIK
TURK SINEMA
TURK SPOR
TURK ULUSAL
TURK YEREL
'''.strip().splitlines()

kanal_filtre_listesi = ''' 
TR: 24 TV
TR: 360 TV
TR: A HABER HD
TR: A HABER HD+
TR: A HABER SD
TR: A PARA
TR: A SPOR HD
TR: A SPOR HD+
TR: A SPOR SD
TR: A2 TV HD
TR: A2 TV HD+
TR: AKASYA DURAGI 7/24
TR: AKIT TV
TR: AKSU TV (K.MARAS)
TR: AL ZAHRA TV
TR: ALANYA POSTA TV
TR: Almanya Türk Tv
TR: ALPER RENDE TV
TR: ANADOLU Dernek Tv
TR: ANADOLU NET TV (KAYSERI)
TR: Angeline Jolie 7/24
TR: ANKARA'NIN DIKMENI 7/24
TR: Arabesk Türk (Radyo)
TR: ARABESK TV
TR: Arabeskin Sesi (Radyo)
TR: ARKA SOKAKLAR 1 7/24
TR: ARKA SOKAKLAR 2 7/24
TR: ARKA SOKAKLAR 3 7/24
TR: ARKA SOKAKLAR 4 7/24
TR: ARKA SOKAKLAR 5 7/24
TR: ARKA SOKAKLAR 6 7/24
TR: ARKADASIM HOSGELDIN 7/24
TR: Arti Tv
TR: AS TV (BURSA)
TR: ASKIM ASKIM 7/24
TR: ATIYE 7/24
TR: ATV AVRUPA
TR: ATV HD
TR: ATV HD+
TR: ATV HD+ (HEVC)
TR: ATV SD
TR: AVIVA TV
TR: AY AY AYICIKLAR
TR: Baba Radyo (Radyo)
TR: BARIS OZCAN TV
TR: BENGUTURK TV
TR: BERAT TV
TR: BEYAZ TV HD
TR: BEYAZ TV HD+
TR: BEYAZ TV SD
TR: BIR TV (IZMIR)
TR: BLOOMBERG HT
TR: BODRUM KENT TV
TR: BOOBA TV
TR: BOX 007 JAMES BOND
TR: BOX 24
TR: BOX ACI HAYAT
TR: BOX AILE SIRKETI
TR: BOX ARIZA
TR: BOX ASKI MEMNU
TR: BOX ASMALI KONAK
TR: BOX AVRUPA YAKASI
TR: BOX AYNEN AYNEN
TR: BOX BEHZAT C
TR: BOX BINBIR GECE
TR: BOX BIZIMKILER
TR: BOX CALIKUSU
TR: BOX CENNET MAHALLESI
TR: BOX CICEK TAKSI
TR: BOX COCUKLAR DUYMASIN
TR: BOX DELI YUREK
TR: BOX DEXTER
TR: BOX EZEL
TR: BOX GAME OF THRONES
TR: BOX GULDUR GULDUR
TR: BOX GUNESIN KIZLARI
TR: BOX HAKAN MUHAFIZ
TR: BOX ISTANBULLU GELIN
TR: BOX KANIT
TR: BOX KARA DAYI
TR: BOX KARA SEVDE
TR: BOX KARDES PAYI
TR: BOX KATARSIS X-TRA
TR: BOX KONUSANLAR
TR: BOX KURTLAR VADISI
TR: BOX KURTLAR VADISI PUSU
TR: BOX KUZEY GUNEY
TR: BOX LEYLA ILE MECNUN
TR: BOX MASKELI BESLER
TR: BOX MERLIN
TR: BOX MUHTESEM YUZYIL
TR: BOX NARCOS
TR: BOX OYLE BIR GECER ZAMAN KI
TR: BOX OZARK
TR: BOX POYRAZ KARAYEL
TR: BOX PRISON BREAK
TR: BOX PUNISHER
TR: BOX RAMO
TR: BOX RECEP IVEDIK
TR: BOX RUHSAR
TR: BOX SAHSIYET
TR: BOX SEN ANLAT KARADENIZ
TR: BOX SIFIR BIR
TR: BOX SUITS
TR: BOX SUSKUNLAR
TR: BOX THE 100
TR: BOX THE HANGOVER
TR: BOX TOLGSHOW FILTRESIZ
TR: BOX TURK MALI
TR: BOX UC KURUS
TR: BOX ULAN İSTANBUL
TR: BOX YABANCI DAMAT
TR: BOX YAHSI CAZIBE
TR: BOX YALANCI YARIM
TR: BOX YAPRAK DOKUMU
TR: BOX YILAN HIKAYESI
TR: BR TV (ZONGULDAK)
TR: Bursa Tv
TR: CAN TV
TR: CAY TV
TR: Cılgın Dershane 7/24
TR: CNBC-E HD
TR: CNN TURK HD
TR: CNN TURK HD+
TR: CNN TURK SD
TR: Cukur 7/24
TR: Damar Fm (Radyo)
TR: Damar Turk (Radyo)
TR: DAMAR TV
TR: Damla Fm (Radyo)
TR: DANLA BILIC TV
TR: DEHA TV (DENIZLI)
TR: DELI MI NE TV
TR: DENIZ POSTASI (KAYSERI)
TR: Derya Fm (Radyo)
TR: DEVA FM ARABESK
TR: DEVA FM NOSTALJI
TR: DEVA FM OYUN HAVASI
TR: DEVA FM POP
TR: DEVA FM RAP
TR: DEVA FM REMIX
TR: DEVA FM TURKU
TR: DEVA FM YABANCI
TR: DHA CANLI 1
TR: DHA CANLI 2
TR: DIM TV (ANTALYA)
TR: Dirilis Ertugrul 7/24
TR: DISCOVERY CHANNEL
TR: DISCOVERY ID HD
TR: DISNEY JUNIOR
TR: DIYANET TV
TR: DIZI TV
TR: DIZIAX ALACAKARANLIK EFSANESI
TR: DIZIAX ALEV ALEV
TR: DIZIAX ALPACINO
TR: DIZIAX AVLU
TR: DIZIAX AYAK ISLERI
TR: DIZIAX BENIM ADIM MELEK
TR: DIZIAX BLINDSPOT
TR: DIZIAX BRAD PITT
TR: DIZIAX BREAKING BAD
TR: DIZIAX BRUCE LEE TV
TR: DIZIAX CEKIC VE GUL
TR: DIZIAX CHICAGO P.D.
TR: DIZIAX DAREDEVIL
TR: DIZIAX EKMEK TEKNESI
TR: DIZIAX LOST
TR: DIZIAX NIKITA
TR: DIZIAX THE BOURNE
TR: DIZIAX THE LAST OF US
TR: Dost TV
TR: DOST TV
TR: Dream Turk Tv
TR: EGE TV
TR: EKOL TV HD
TR: EKOTÜRK TV
TR: ENES BATUR TV
TR: ER TV
TR: Erzurum Web Tv
TR: Es tv
TR: ESKIYA DUNYAYA HUKUMDAR OLMAZ 1
TR: ESKIYA DUNYAYA HUKUMDAR OLMAZ 2
TR: ETV KAYSERI
TR: ETV MANISA
TR: EURO D
TR: EUROSTAR
TR: FB TV
TR: FB TV HD
TR: Fenemon Karisik (Radyo)
TR: FINEST TV
TR: FLASH HABER
TR: FLASH HABER HD+
TR: Fortuna tv
TR: FRT Fethiye Tv
TR: GALIP DERVIS 7/24
TR: GONCA TV
TR: Gozde FM (Radyo)
TR: Gözyasi FM (Radyo)
TR: GRT TV (GAZIANTEP)
TR: GS TV
TR: GULBEYAZ 7/24
TR: HABER GLOBAL HD
TR: HABER GLOBAL HD+
TR: HABER GLOBAL SD
TR: HABER TURK HD
TR: HABER TURK HD+
TR: HABER TURK SD
TR: HALK TV HD
TR: HALK TV HD+
TR: Hayal Fm (Radyo)
TR: Hercai 7/24
TR: HRT Akdeniz
TR: HT 7/24 SPOR
TR: HUNAT TV (KAYSERI)
TR: HZ. YUSUF 7/24
TR: IBB TV
TR: ICERDE 7/24
TR: IKRA TV
TR: ILYAS SALMAN TV
TR: IP-Man 7/24
TR: ISTANBUL MUHAFIZLARI
TR: Istanbul Tv
TR: ISTANBULLU GELIN 7/24
TR: KABE TV
TR: KADIR INANIR TV
TR: KAFA RADYO (Radyo)
TR: KAFALAR TV
TR: Kanal 12
TR: KANAL 15 (BURDUR)
TR: KANAL 19
TR: KANAL 23 (ELAZIG)
TR: KANAL 32 (ISPARTA)
TR: KANAL 58
TR: KANAL 68 (AKSARAY)
TR: KANAL 7 AVRUPA
TR: KANAL 7 HD
TR: KANAL 7 HD+
TR: KANAL AVRUPA
TR: KANAL D HD
TR: KANAL D HD+
TR: KANAL D HD+ (HEVC)
TR: KANAL D SD
TR: Kanal FIRAT
TR: KANAL ON4
TR: KANAL Z (ZONGULDAK)
TR: KARA SEVDA 7/24
TR: Karabük tv
TR: KAY TV (KAYSERI)
TR: Kemence Fm (Radyo)
TR: KOBIM TV
TR: KOCAELI TV
TR: KON TV HD
TR: Konya Olay Tv
TR: KÖY TV
TR: Kral Fm (Radyo)
TR: KRAL POP TV
TR: KRAL SAKIR
TR: KRAL TV
TR: KRT KÜLTÜR TV
TR: KUDÜS TV
TR: La Casa De Papel 7/24
TR: LIFE TV (KAYSERI)
TR: LIMON ILE ZEYTIN
TR: LINE TV
TR: LUGAT TV
TR: M TURK TV
TR: Manisa Ev Tv
TR: MASA ILE KOCA AYI
TR: Mavi Karadeniz
TR: MAX 007 HD
TR: MEKAMELEEN TV
TR: MERCAN TV
TR: MERCAN TV (ADIYAMAN)
TR: MINIKA COCUK
TR: MINIKA GO
TR: MMN TURK TV
TR: MOR TV
TR: NOW TV HD
TR: NOW TV HD+
TR: NOW TV HD+ (HEVC)
TR: NOW TV SD
TR: NTV HABER HD
TR: NTV HABER HD+
TR: NTV HABER SD
TR: Number One Ask
TR: Number One Damar
TR: Number One Dance
TR: Number One Turk
TR: Number One Tv
TR: OGUZHAN UGUR TV
TR: ON6 TV (BURSA)
TR: ORKUN ISITMAK TV
TR: PAW PATROL TV
TR: Power Love
TR: POWER TURK
TR: Power Turk Akustik
TR: Power Turk Slow
TR: Power Turk Taptaze
TR: POWER TV
TR: Radyo 7
TR: Radyo Banko (Radyo)
TR: Radyo Mastika (Radyo)
TR: Radyo Seherli Dini (Radyo)
TR: Radyo Vatan (Radyo)
TR: REHBER TV
TR: RIZE TURK
TR: ROAD RUNNER TV
TR: RUHI CENET TV
TR: Rumeli Tv
TR: SEFA KINDIR TV
TR: SEMERKAND TV
TR: Seymen FM (Radyo)
TR: SHOW TURK
TR: SHOW TV HD
TR: SHOW TV HD+
TR: SHOW TV HD+ (HEVC)
TR: SHOW TV SD
TR: SHOWMAX
TR: SIHIRLI ANNEM
TR: SOKAGIN COCUKLARI 7/24
TR: STAR TV HD
TR: STAR TV HD+
TR: STAR TV HD+ (HEVC)
TR: STAR TV SD
TR: SUN RTV (MERSIN)
TR: SUNNAH TV
TR: SZC TV
TR: SZC TV HD+
TR: TARIK AKAN TV
TR: TARIM TV
TR: TAY TV
TR: TELE 1
TR: TEVE 2
TR: TGRT BELGESEL
TR: TGRT EU
TR: TGRT HABER HD
TR: TGRT HABER HD+
TR: TIVI 6 (ANKARA)
TR: TIVI TURK
TR: TJK TV
TR: TLC
TR: TMB
TR: TON TV (CANAKKALE)
TR: TOP POP TV
TR: TRAKYA TÜRK
TR: TRT 1 HD
TR: TRT 1 HD+
TR: TRT 1 HD+ (HEVC)
TR: TRT 1 SD
TR: TRT 2
TR: TRT 4K
TR: TRT AVAZ
TR: TRT BELGESEL
TR: TRT BELGESEL HD+
TR: TRT COCUK
TR: TRT DIYANET COCUK
TR: TRT EBA TV ILKOKUL
TR: TRT EBA TV LISE
TR: TRT EBA TV ORTAOKUL
TR: TRT HABER HD
TR: TRT HABER HD+
TR: TRT HABER SD
TR: TRT KURDU
TR: TRT MUZIK
TR: TRT SPOR HD
TR: TRT SPOR HD+
TR: TRT SPOR SD
TR: TRT SPOR YILDIZ HD
TR: TRT SPOR YILDIZ SD
TR: TRT TURK
TR: TURKMENELI TV
TR: Türkü Fm (Radyo)
TR: TV 100
TR: TV 100 HD+
TR: TV 4
TR: TV 41 (KOCAELI)
TR: TV 5
TR: TV 52
TR: TV 8 HD
TR: TV 8 HD+
TR: TV 8 HD+ (HEVC)
TR: TV 8 INT
TR: TV 8 SD
TR: TV 8.5 HD+
TR: TV 8.5 SD
TR: TV A (ADANA)
TR: TVNET
TR: TYT TURK
TR: ULKE TV HD
TR: ULUSAL KANAL
TR: ULUSAL RADYO-TURKU (Radyo)
TR: URFANATIK TV
TR: VATAN TV
TR: VIYANA FM (Radyo)
TR: VUSLAT TV (MALATYA)
TR: W SPORTS
TR: Yildiz Tv Sinop
TR: Yildizlar Makami (Radyo)
TR: YOL TV
TR: Yozgat Fm (Radyo)
TR: ZEKI & METIN TV
TR: KRT KÜLTÜR TV
TR: EKOTÜRK TV
TR: KUDÜS TV
TR: KÖY TV
TR: Almanya Türk Tv
TR: TRAKYA TÜRK
'''.strip().splitlines()

# === Yardımcı Fonksiyonlar ===
def turkce_fix(text):
    return text.translate(str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU"))

def ascii_entity_encode(s: str):
    return ''.join(f'&#{ord(c)};' for c in s)

def replacename(x):
    replace_list = [
        '|TR| ', '| TR | ', 'TR VIP*: ', 'TR: ', 'TR| ', 'TR.: ', 'TR - ', '| TR  ', '(TR/ENG)',
        'TR➤ ', 'TR ☪ ', '|TR.SIN| ', 'YEREL | ', 'TR • ', '⚽️', ' Raw', '7/24', '24/7', '(FEED)', '(MAC ZAMANI)',
        'TR | ', 'TR -- ', 'TR : ', '[TR] ', 'TR*: ', '*', 'HD+', '(Minimum 150mbps)', 'SD', 'HD', '4K'
    ]
    for item in replace_list:
        x = x.replace(item, '')
    return x.strip().lstrip()

def replace(x):
    return x.replace('  ', ' ')

# === M3U İşleme ===
def parse_m3u_lines(lines):
    entries, seen, duplicates = [], set(), set()
    i = 0
    while i < len(lines):
        if lines[i].startswith("#EXTINF") and i + 1 < len(lines):
            extinf, video_link = lines[i], lines[i + 1]
            entry = (extinf, video_link)
            if entry in seen:
                duplicates.add(entry)
            else:
                seen.add(entry)
                entries.append(entry)
            i += 1
        i += 1
    return entries

def filtrele_ve_duzenle(entries):
    filtrelenmis, kanal_adlari = [], {}
    passlist_normalize = [turkce_fix(k).lower().replace(" ", "") for k in kanal_filtre_listesi]
    
    for extinf, video_link in entries:
        if any(x in video_link for x in [".mp4", ".mkv", ".---", "###", "***"]):
            continue
        if any(x in extinf for x in [".mp4", ".mkv", ".---", "###", "***", "Radyo"]):
            continue

        for kategori in kategori_filtre_listesi:
            if kategori in extinf:
                tvg_id = re.search(r'tvg-id="(.*?)"', extinf)
                logo = re.search(r'tvg-logo="(.*?)"', extinf)
                grup = re.search(r'group-title="(.*?)"', extinf)
                kanal_adi_eslesme = re.search(r'group-title=".*?"\s*,\s*(.+)', extinf)

                tvg_id_deger = tvg_id.group(1) if tvg_id else ""
                logo_deger = logo.group(1) if logo else ""
                grup_deger = grup.group(1) if grup else ""
                kanal_adi = kanal_adi_eslesme.group(1).strip() if kanal_adi_eslesme else "Bilinmeyen"

                kanal_adi_normalize = turkce_fix(kanal_adi).lower().replace(" ", "")
                if kanal_adi_normalize in passlist_normalize:
                    continue

                kanal_adi = replace(replacename(kanal_adi))
                if kanal_adi in kanal_adlari:
                    kanal_adlari[kanal_adi] += 1
                    kanal_adi_numarali = f"{kanal_adi}_{kanal_adlari[kanal_adi]}"
                else:
                    kanal_adlari[kanal_adi] = 1
                    kanal_adi_numarali = kanal_adi
                proxy_url = "https://xttmc-xttmcproxy.hf.space/proxy/m3u?url="
                yeni_extinf = f'#EXTINF:-1 tvg-id="{tvg_id_deger}" tvg-name="{kanal_adi_numarali}" tvg-logo="{logo_deger}" group-title="{grup_deger}",{kanal_adi_numarali}'
                filtrelenmis.append((yeni_extinf, proxy_url+video_link))
                break
    return filtrelenmis

def kanal_tekrar_sayaci(veri_listesi):
    sayac, yeni_liste = {}, []
    for extinf, link in veri_listesi:
        kanal_adi_eslesme = re.search(r',(.+)$', extinf)
        kanal_adi = kanal_adi_eslesme.group(1) if kanal_adi_eslesme else None
        if kanal_adi:
            sayac.setdefault(kanal_adi, 0)
            sayac[kanal_adi] += 1
            if sayac[kanal_adi] > 1:
                yeni_kanal_adi = f"{kanal_adi} ({sayac[kanal_adi]})"
                extinf = re.sub(r',.+$', f",{yeni_kanal_adi}", extinf)
                extinf = re.sub(r'tvg-name=".*?"', f'tvg-name="{yeni_kanal_adi}"', extinf)
        yeni_liste.append((extinf, link))
    return yeni_liste

def m3u_to_text(entries):
    return '\n'.join([f"{e[0]}\n{e[1]}" for e in entries])

def main():
    # === Ana Akış ===
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    tarih = datetime.now().strftime("%y%m%d_%H%M%S")
    # output_name = f"{host}_{tarih}_encrypted.m3u"
    # output_name = f"p1.xml"
    output_name = f"ressources/xttsearch/p1.xml"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # M3U içeriğini çözümle
        lines = response.text.strip().splitlines()
        entries = parse_m3u_lines(lines)
        filtreli = filtrele_ve_duzenle(entries)
        duzenli = kanal_tekrar_sayaci(filtreli)
        m3u_text = m3u_to_text(duzenli)

        # Şifrele ve encode et
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted = cipher.encrypt(m3u_text.encode("utf-8"))
        final_content = encrypted + f"KKXTT={key.decode()}".encode()
        encoded = base64.b64encode(final_content)
        html_encoded = ascii_entity_encode(encoded.decode())

        # Kaydet
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(html_encoded)

        print(f"\n✅ Tüm işlemler tamamlandı: {output_name} dosyası oluşturuldu ve şifrelendi.")

        # .xml.gz olarak sıkıştır ve .xml dosyasını sil
        with open(output_name, "rb") as f_in:
            with gzip.open(output_name + ".gz", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Orijinal XML dosyasını sil
        os.remove(output_name)

    except requests.RequestException as e:
        print(f"İndirme hatası: {e}")

if __name__ == "__main__":
    main()

