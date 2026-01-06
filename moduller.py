import pygame
import random
import os
import math
import threading



class BaseModule:
    def __init__(self, ekran, asistan, motor, font_yolu, rapor=None):
        self.ekran = ekran
        self.asistan = asistan
        self.motor = motor
        self.font_yolu = font_yolu
        self.rapor = rapor
        self.sayac = 0
        self.aktif = True

    def update(self):
        self.sayac += 0.05

    def metin_ciz(self, metin, x, y, boyut=35, statik=False):

        self.motor.ciz(self.ekran, metin, (x, y), self.font_yolu, boyut=boyut, statik=statik)

class RadarModule(BaseModule):
    def __init__(self, *args):
        super().__init__(*args)

        self.font = pygame.font.Font(self.font_yolu, 35)
        self.sorular = [
            {"dogru": "UZAY GEMISI YILDIZLARA GIDIYOR", "hata": "YILDIZALRA",
             "bozuk": "UZAY GEMISI YILDIZALRA GIDIYOR"},
            {"dogru": "MAVI GEZEGEN COK GUZEL", "hata": "AMVI", "bozuk": "AMVI GEZEGEN COK GUZEL"},
            {"dogru": "ROKET AYIN YANINDAN GECTI", "hata": "YAIN", "bozuk": "ROKET YAIN YANINDAN GECTI"}
        ]
        self.hedef_alan = None
        self.yeni_soru()


    def yeni_soru(self):
        # 1. Yeni soruyu rastgele seç
        self.soru = random.choice(self.sorular)

        # 2. TIKLAMA ALANINI (RECT) BURADA HESAPLA (Statik ve Sağlam)

        curr_x = 380
        kelimeler = self.soru["bozuk"].split()

        for k in kelimeler:
            if k == self.soru["hata"]:
                genislik, yukseklik = self.font.size(k)
                # Tıklama kutusunu burada bir kez oluşturuyoruz
                self.hedef_alan = pygame.Rect(curr_x, 250, genislik, yukseklik)
                break  # Kutuyu bulduk, döngüden çıkabiliriz
            curr_x += self.font.size(k)[0] + 30

    def draw(self):
        self.metin_ciz("RADAR: MUTASYON TESPITI", 420, 50, statik=False)
        # Soru Paneli
        pygame.draw.rect(self.ekran, (210, 200, 170), (350, 200, 750, 150), border_radius=15)
        pygame.draw.rect(self.ekran, (80, 70, 50), (350, 200, 750, 150), 2, border_radius=15)

        curr_x = 380
        kelimeler = self.soru["bozuk"].split()


        for k in kelimeler:
            self.metin_ciz(k, curr_x, 250, boyut=35, statik=True)
            curr_x += self.font.size(k)[0] + 30

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # Artık hedef_alan çok daha stabil
            if self.hedef_alan and self.hedef_alan.collidepoint(mx, my):
                try:
                    pygame.mixer.Sound("assets/sounds/basari.wav").play()
                except:
                    pass

                if hasattr(self, 'rapor'):
                    self.rapor.veri_ekle("radar_sureler", 5.0)

                self.yeni_soru()  # Yeni soruyu ve yeni RECT'i hazırlar
                return True
        return False

class TerminalModule(BaseModule):
    def __init__(self, *args):
        super().__init__(*args)
        self.veriseti = [
            {"kelime": "ROKET", "dogru": "roket.png", "diger": ["araba.png", "ay.png"]},
            {"kelime": "BAL", "dogru": "bal.png", "diger": ["dal.png", "pasta.png"]},
            {"kelime": "SOBA", "dogru": "soba.png", "diger": ["sopa.png", "ay.png"]},
            {"kelime": "İNCİR", "dogru": "incir.png", "diger": ["zincir.png", "balik.png"]},
            {"kelime": "AYAKKABI", "dogru": "ayakkabi.png", "diger": ["sandalye.png", "agac.png"]},
            {"kelime": "YILDIZ", "dogru": "yildiz.png", "diger": ["bulut.png", "cicek.png"]},
            {"kelime": "UZAYLI", "dogru": "uzayli.png", "diger": ["balik.png", "elma.png"]},
            {"kelime": "ARABA", "dogru": "araba.png", "diger": ["ev.png", "pasta.png"]},
            {"kelime": "BALIK", "dogru": "balik.png", "diger": ["cicek.png", "agac.png"]},
            {"kelime": "BULUT", "dogru": "bulut.png", "diger": ["ay.png", "ev.png"]},
            {"kelime": "CICEK", "dogru": "cicek.png", "diger": ["elma.png", "sandalye.png"]},
            {"kelime": "ELMA", "dogru": "elma.png", "diger": ["pasta.png", "agac.png"]},
            {"kelime": "PASTA", "dogru": "pasta.png", "diger": ["ev.png", "uzayli.png"]}
        ]
        self.image_cache = {}
        self.son_kelime = ""
        self.efekt_halkalar = []
        self.load_images()
        self.yeni_soru()

    def load_images(self):
        path = os.path.join("assets", "images", "terminal")
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.lower().endswith((".png", ".jpg")):
                    img = pygame.image.load(os.path.join(path, file)).convert_alpha()
                    self.image_cache[file] = pygame.transform.scale(img, (180, 180))

    def yeni_soru(self):
        yeni = random.choice(self.veriseti)
        self.soru = yeni
        self.secenekler = [self.soru["dogru"]] + self.soru["diger"]
        random.shuffle(self.secenekler)
        self.durum = "KELIME"
        self.zamanlayici = pygame.time.get_ticks()
        self.dogru_bildi_mi = False

    def sifirla(self):
        """Modüller arası geçişte Terminal'i kelime moduna zorlar."""
        self.yeni_soru()

    def update(self):
        super().update()
        zaman_farki = pygame.time.get_ticks() - self.zamanlayici

        if self.durum == "KELIME" and zaman_farki > 2000:
            self.durum = "SECIM"

        if self.dogru_bildi_mi and zaman_farki > 1000:
            self.dogru_bildi_mi = False
            self.yeni_soru()

        for h in self.efekt_halkalar[:]:
            h["a"] -= 5
            if h["a"] <= 0:
                self.efekt_halkalar.remove(h)

    def draw(self):
        """Hizalaması düzeltilmiş ve neon halkaları içeren draw metodu."""
        self.metin_ciz("ISINLAMA TERMINALI", 450, 50, statik=False)

        if self.durum == "KELIME":
            self.metin_ciz(self.soru["kelime"], 600, 300, boyut=60, statik=False)

        elif self.durum == "SECIM":
            self.metin_ciz("DOGRU RESMI SEC!", 550, 150, boyut=30, statik=True)

            for i, r_adi in enumerate(self.secenekler):
                x_pos = 400 + (i * 240)

                # Neon halkalar
                for h in self.efekt_halkalar:
                    if h["kutu_x"] == x_pos:
                        for j in range(5):
                            s = pygame.Surface((210 + j * 4, 210 + j * 4), pygame.SRCALPHA)
                            alpha = max(0, h["a"] // (j + 1))
                            pygame.draw.rect(s, (0, 150, 255, alpha), s.get_rect(), 3, border_radius=15)
                            self.ekran.blit(s, (x_pos - 5 - j * 2, 245 - j * 2))

                # Kutular ve Resimler
                pygame.draw.rect(self.ekran, (210, 200, 170), (x_pos, 250, 200, 200), border_radius=15)
                pygame.draw.rect(self.ekran, (80, 70, 50), (x_pos, 250, 200, 200), 3, border_radius=15)

                if r_adi in self.image_cache:
                    self.ekran.blit(self.image_cache[r_adi], (x_pos + 10, 260))

    def handle_event(self, event):
        """Tıklamaları yakalayan ve neonu başlatan metod."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.durum == "SECIM" and not self.dogru_bildi_mi:
            mx, my = event.pos
            for i, r_adi in enumerate(self.secenekler):
                x_pos = 400 + (i * 240)
                if x_pos < mx < x_pos + 200 and 250 < my < 450:
                    if r_adi == self.soru["dogru"]:
                        self.dogru_bildi_mi = True
                        self.zamanlayici = pygame.time.get_ticks()
                        self.efekt_halkalar.append({"kutu_x": x_pos, "a": 255})
                        try:
                            pygame.mixer.Sound("assets/sounds/terminalbasari.mp3").play()
                        except:
                            pass
                        return "DOGRU_TERMINAL"
        return False


class SinyalModule(BaseModule):
    def __init__(self, *args):
        super().__init__(*args)
        self.son_kelime = ""
        self.heceler_liste = [
            {"text": "papatya", "parcalar": ["pa", "pat", "ya"]},
            {"text": "domates", "parcalar": ["do", "ma", "tes"]},
            {"text": "bardakçı", "parcalar": ["bar", "dak", "çı"]},
            {"text": "balıkçı", "parcalar": ["ba", "lık", "çı"]},
            {"text": "bilgisayar", "parcalar": ["bil", "gi", "sa", "yar"]},
            {"text": "kelebek", "parcalar": ["ke", "le", "bek"]},
            {"text": "pervane", "parcalar": ["per", "va", "ne"]},
        ]

        # --- RESİMLERİ BURADA YÜKLÜYORUZ ---
        self.konfeti_resimleri = []
        for i in range(1, 4):
            yol = f"assets/images/konfeti{i}.png"
            if os.path.exists(yol):
                img = pygame.image.load(yol).convert_alpha()
                self.konfeti_resimleri.append(pygame.transform.scale(img, (100, 100)))

        self.konfeti_parcaciklari = []
        self.yeni_oyun()

    def yeni_oyun(self):
        self.soru = random.choice(self.heceler_liste)
        self.parca_objeleri = []
        self.tamamlandi = False

        self.sayac = 0
        alanlar = [(400, 200), (950, 200), (400, 550), (950, 550)]
        random.shuffle(alanlar)
        for i, p in enumerate(self.soru["parcalar"]):
            self.parca_objeleri.append({
                "id": i, "text": p, "pos": list(alanlar[i]),
                "drag": False, "bagli": True if i == 0 else False,
                "color": (200, 200, 200)
            })

    def update(self):
        super().update()
        mx, my = pygame.mouse.get_pos()
        sol_tik = pygame.mouse.get_pressed()[0]

        # 1. Konfeti Hareket Mantığı
        for k in self.konfeti_parcaciklari[:]:
            k["pos"][0] += k["vel"][0]
            k["pos"][1] += k["vel"][1]
            k["vel"][1] += 0.3
            k["omur"] -= 1
            if k["omur"] <= 0: self.konfeti_parcaciklari.remove(k)

        if not sol_tik:
            for p in self.parca_objeleri: p["drag"] = False

        # 2. Sürükleme ve Mıknatıs Sistemi (Gelişmiş)
        for p in self.parca_objeleri:
            if p["drag"]:
                dx = mx - 60 - p["pos"][0]
                dy = my - 40 - p["pos"][1]
                p["pos"][0] += dx
                p["pos"][1] += dy
                # Bağlı olan diğer parçaları da beraber sürükle
                for p_diger in self.parca_objeleri:
                    if p != p_diger and self.bagli_mi(p, p_diger):
                        p_diger["pos"][0] += dx
                        p_diger["pos"][1] += dy

        # 3. Mıknatıs Yapışma Kontrolü
        for i in range(len(self.parca_objeleri) - 1):
            h1 = self.parca_objeleri[i]
            h2 = self.parca_objeleri[i + 1]
            if not h2["bagli"]:
                dist = math.sqrt((h1["pos"][0] + 120 - h2["pos"][0]) ** 2 + (h1["pos"][1] - h2["pos"][1]) ** 2)
                if dist < 45:
                    h2["bagli"] = True
                    h2["pos"] = [h1["pos"][0] + 120, h1["pos"][1]]

        # 4. SİNYAL BİTİŞ KONTROLÜ
        hepsi_tamam = all(p["bagli"] for p in self.parca_objeleri)
        if hepsi_tamam and not self.tamamlandi:
            self.tamamlandi = True
            self.bekleme_sayaci = pygame.time.get_ticks()

            # Başarı Sesi ve Kelime Okuma
            try:
                pygame.mixer.Sound("assets/sounds/sinyalbasari.mp3").play()
                self.asistan.seslendir(self.soru["text"].lower())
            except:
                pass


            self.konfeti_patlat()

        # 5. Yeni Kelimeye Geçiş Zamanlaması
        if self.tamamlandi and pygame.time.get_ticks() - self.bekleme_sayaci > 3500:
            self.yeni_oyun()

    def draw(self):
        self.metin_ciz("SINYAL: HECE BAGLAMA", 420, 50, statik=False)
        # Font yolu hatasını burada da düzelttik
        font = pygame.font.Font(self.font_yolu, 30)
        for p in self.parca_objeleri:
            rect = pygame.Rect(p["pos"][0], p["pos"][1], 120, 80)

            # Arka plan ve senin istediğin o koyu gri çerçeve (60, 60, 60)
            pygame.draw.rect(self.ekran, p["color"], rect, border_radius=15)
            pygame.draw.rect(self.ekran, (60, 60, 60), rect, 3, border_radius=15)

            yuzey = font.render(p["text"], True, (0, 0, 0))
            self.ekran.blit(yuzey, yuzey.get_rect(center=rect.center))

        for k in self.konfeti_parcaciklari:
            self.ekran.blit(k["img"], k["pos"])

    def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # 1. Tıklanan parçayı bul (Döngü ile tüm parçalara bakıyoruz)
                for p in reversed(self.parca_objeleri):
                    # Parçanın koordinatlarını kontrol et
                    if p["pos"][0] < mx < p["pos"][0] + 120 and p["pos"][1] < my < p["pos"][1] + 80:
                        p["drag"] = True
                        # Seslendirme işlemini asistan üzerinden yap
                        hece = p['text'].lower()
                        threading.Thread(target=lambda: self.asistan.seslendir(hece), daemon=True).start()
                        # Parçayı bulduğumuz için döngüden çıkabiliriz ama return etmiyoruz!
                        break

                        # 2. KRİTİK NOKTA: Eğer kelime bittiyse main__.py'ye haber ver
                if self.tamamlandi:
                    return True

            # 3. Eğer olay bir tıklama değilse veya kelime henüz bitmediyse False dön
            return False


    def bagli_mi(self, p1, p2):
        """İki hecenin birbirine bağlı olup olmadığını kontrol eder."""
        start = min(p1["id"], p2["id"])
        end = max(p1["id"], p2["id"])
        for i in range(start, end):
            if not self.parca_objeleri[i + 1]["bagli"]:
                return False
        return True

    def konfeti_patlat(self):
        """Oyun bitince konfetileri başlatır."""
        for _ in range(50):
            if self.konfeti_resimleri:
                self.konfeti_parcaciklari.append({
                    "pos": [random.randint(400, 1100), 720],
                    "vel": [random.uniform(-3, 3), random.uniform(-12, -18)],
                    "img": random.choice(self.konfeti_resimleri),
                    "omur": 150
                })