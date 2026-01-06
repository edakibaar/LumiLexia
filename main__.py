import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pygame
import math
import threading
import traceback
import random
from profil import ProfilSistemi
from raporlama import RaporlamaSistemi
from tkinter import filedialog, Tk
from moduller import RadarModule, TerminalModule, SinyalModule

root = Tk()
root.withdraw()

try:
    from DyslexiFlow import DyslexiFlow
    from dislekaptan_motoru.ai_asistan import AIAsistan
except Exception as e:
    print(f"HATA: {e}")
    sys.exit()

GENISLIK, YUKSEKLIK = 1280, 720
FPS = 60
FONT_YOLU = os.path.join("assets", "fonts", "OpenDyslexic-Regular.otf")

KOYU_KREM = (210, 200, 170)
METIN_RENGI = (40, 40, 40)


def draw_speech_bubble(surface, text, font, color, x, y):
    if not text or text == "LUMINA DUSUNUYOR...": return
    text = "".join(c for c in text if c.isalnum() or c.isspace() or c in ".,!?-")
    MAX_BALON_GENISLIK = 320
    PADDING = 20
    SATIR_ARALIGI = 10
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < (MAX_BALON_GENISLIK - PADDING * 2):
            current_line = test_line
        else:
            if current_line: lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    text_height = font.get_height()
    bubble_width = MAX_BALON_GENISLIK
    bubble_height = len(lines) * (text_height + SATIR_ARALIGI) + (PADDING * 2)
    bubble_rect = pygame.Rect(x - bubble_width - 10, y - bubble_height - 10, bubble_width, bubble_height)
    pygame.draw.rect(surface, (150, 140, 110),
                     (bubble_rect.x + 3, bubble_rect.y + 3, bubble_rect.width, bubble_rect.height), border_radius=15)
    pygame.draw.rect(surface, (210, 200, 170), bubble_rect, border_radius=15)
    pygame.draw.rect(surface, (80, 70, 50), bubble_rect, 2, border_radius=15)
    for i, line in enumerate(lines):
        line_surf = font.render(line.strip(), True, (0, 0, 0))
        surface.blit(line_surf, (bubble_rect.x + PADDING, bubble_rect.y + PADDING + i * (text_height + SATIR_ARALIGI)))


class YildizKaymasi:
    def __init__(self):
        self.yildizlar = []

    def patlat(self, x, y):
        for _ in range(25):
            self.yildizlar.append({
                "pos": [x, y],
                "vel": [random.uniform(-6, 6), random.uniform(-6, 6)],
                "renk": (255, 255, random.randint(150, 255)),
                "omur": 255
            })

    def guncelle_ve_ciz(self, ekran):
        for y in self.yildizlar[:]:
            y["pos"][0] += y["vel"][0]
            y["pos"][1] += y["vel"][1]
            y["omur"] -= 8
            if y["omur"] <= 0:
                self.yildizlar.remove(y)
            else:
                pygame.draw.circle(ekran, y["renk"], (int(y["pos"][0]), int(y["pos"][1])), 3)


class UzayModulu:
    def __init__(self, isim):
        self.isim = isim
        self.puan = 0

    def basarili_islem(self):
        self.puan += 10


class Uygulama:
    def __init__(self):
        pygame.init()
        self.ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
        pygame.display.set_caption("DİS-KAPTAN: Uzay Macerası")
        self.saat = pygame.time.Clock()
        self.motor = DyslexiFlow()
        self.asistan = AIAsistan()
        self.profil = ProfilSistemi(self.ekran, FONT_YOLU)
        self.rapor = RaporlamaSistemi(self.asistan)
        self.durum = "GIRIS"
        self.input_sirasi = "isim"
        self.modul_baslangic = 0
        self.sayac = 0
        self.kullanici_yazisi = ""
        self.ai_cevabi = ""
        self.secilen_resim_yolu = ""
        self.yildiz_efekti = YildizKaymasi()
        self.radar_modulu = RadarModule(self.ekran, self.asistan, self.motor, FONT_YOLU)
        self.terminal_modulu = TerminalModule(self.ekran, self.asistan, self.motor, FONT_YOLU)
        self.sinyal_modulu = SinyalModule(self.ekran, self.asistan, self.motor, FONT_YOLU)
        self.radar_modulu.rapor = self.rapor
        self.terminal_modulu.rapor = self.rapor
        self.sinyal_modulu.rapor = self.rapor
        try:
            self.bg = pygame.image.load("assets/images/uzaygemisi.png").convert()
            self.bg = pygame.transform.scale(self.bg, (GENISLIK, YUKSEKLIK))
            self.kayit_bg = pygame.image.load("assets/images/kayit_bg.png").convert()
            self.kayit_bg = pygame.transform.scale(self.kayit_bg, (GENISLIK, YUKSEKLIK))
            self.lumina = pygame.image.load("assets/images/uzayli.png").convert_alpha()
            self.lumina = pygame.transform.scale(self.lumina,
                                                 (250, int(self.lumina.get_height() * (250 / self.lumina.get_width()))))
        except:
            self.bg = self.kayit_bg = self.lumina = None

    def dosya_sec(self):
        try:
            dosya_yolu = filedialog.askopenfilename(filetypes=[("Resim Dosyaları", "*.jpg *.jpeg *.png")])
            if dosya_yolu:
                self.ai_cevabi = "LUMINA FOTOGRAFI INCELEMEYE BASLADI..."
                self.secilen_resim_yolu = dosya_yolu
                threading.Thread(
                    target=lambda: setattr(self, 'ai_cevabi', self.asistan.resim_analiz_et(dosya_yolu).upper()),
                    daemon=True).start()
        except:
            pass

    def uzun_metin_ciz(self, metin, x, y, boyut=18):
        if not metin: return
        test_font = pygame.font.Font(FONT_YOLU, boyut) if os.path.exists(FONT_YOLU) else pygame.font.SysFont("Arial",
                                                                                                             boyut)
        satirlar = self.metni_satirlara_bol(metin, test_font, 550)
        panel_yukseklik = len(satirlar) * 35 + 20
        pygame.draw.rect(self.ekran, (210, 200, 170), (380, y - 10, 640, panel_yukseklik), border_radius=10)
        pygame.draw.rect(self.ekran, (80, 70, 50), (380, y - 10, 640, panel_yukseklik), 2, border_radius=10)
        for i, satir in enumerate(satirlar):
         self.motor.ciz(self.ekran, satir, (380, y + (i * 25)), FONT_YOLU, boyut=boyut, zaman=self.sayac,
                           statik=False)

    def metni_satirlara_bol(self, metin, font, max_genislik):
        kelimeler = metin.split(' ')
        satirlar, su_anki_satir = [], ""
        for kelime in kelimeler:
            if font.size(su_anki_satir + kelime)[0] < max_genislik - 20:
                su_anki_satir += kelime + " "
            else:
                satirlar.append(su_anki_satir.strip())
                su_anki_satir = kelime + " "
        satirlar.append(su_anki_satir.strip())
        return satirlar

    def arayuz_ciz(self):
        if self.bg: self.ekran.blit(self.bg, (0, 0))
        s = pygame.Surface((320, YUKSEKLIK), pygame.SRCALPHA)
        s.fill((40, 40, 80, 150))
        self.ekran.blit(s, (0, 0))
        moduller = ["RADAR: MUTASYON AVI", "SINYAL: HECE BAGI", "ISINLAMA TERMINALI", "ODEV KAPTANI"]
        for i, mod in enumerate(moduller):
            y_pos = 160 + (i * 100)
            pygame.draw.rect(self.ekran, KOYU_KREM, (20, y_pos, 275, 70), border_radius=12)
            self.motor.ciz(self.ekran, mod, (40, y_pos + 15), FONT_YOLU, boyut=20, zaman=self.sayac, statik=False)

    def calistir(self):
        while True:
            self.saat.tick(FPS)
            self.sayac += 0.05
            for olay in pygame.event.get():
                if olay.type == pygame.QUIT:
                    if len(self.profil.veli_mail) > 5:
                        t = threading.Thread(target=self.rapor.rapor_hazirla_ve_gonder, args=(self.profil,))
                        t.start()
                        pygame.time.delay(1000)
                    pygame.quit()
                    sys.exit()

                if self.durum == "GIRIS":
                    if olay.type == pygame.KEYDOWN:
                        if olay.key == pygame.K_RETURN:
                            if len(self.profil.kullanici_adi) >= 2 and len(self.profil.veli_mail) >= 2:
                                self.durum = "ANA_MENU"
                                threading.Thread(target=lambda: self.asistan.seslendir(
                                    f"Hoş geldin Kaptan {self.profil.kullanici_adi}"), daemon=True).start()
                        elif olay.key == pygame.K_UP or olay.key == pygame.K_DOWN:
                            self.input_sirasi = "mail" if self.input_sirasi == "isim" else "isim"
                        elif olay.key == pygame.K_BACKSPACE:
                            if self.input_sirasi == "isim":
                                self.profil.kullanici_adi = self.profil.kullanici_adi[:-1]
                            else:
                                self.profil.veli_mail = self.profil.veli_mail[:-1]
                        elif olay.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                            self.profil.secilen_avatar_index = int(olay.unicode) - 1
                        else:
                            if olay.unicode.isprintable():
                                if self.input_sirasi == "isim":
                                    self.profil.kullanici_adi += olay.unicode
                                else:
                                    self.profil.veli_mail += olay.unicode

                else:  # OYUN İÇİ OLAYLAR (GİRİŞ DIŞI)
                    if olay.type == pygame.MOUSEBUTTONDOWN:
                        self.motor.etkilesim_kontrol(olay.pos, self.asistan)
                        mx, my = olay.pos
                        if 20 < mx < 295:
                            if 160 < my < 230:
                                # Her tıklamada eski AI yazılarını ve cevaplarını temizle
                                self.ai_cevabi = ""
                                self.secilen_resim_yolu = ""  # Ödev resmini de sıfırla
                                self.durum = "RADAR"
                                self.modul_baslangic = pygame.time.get_ticks()
                            elif 260 < my < 330:
                                self.durum = "SINYAL"
                                self.modul_baslangic = pygame.time.get_ticks()
                            elif 360 < my < 430:
                                self.durum = "TERMINAL"
                                self.terminal_modulu.sifirla()
                                self.modul_baslangic = pygame.time.get_ticks()
                            elif 460 < my < 530:
                                self.durum = "ODEV"

                        if self.durum == "RADAR":
                            if self.radar_modulu.handle_event(olay):
                                self.yildiz_efekti.patlat(mx, my)
                                self.rapor.veri_ekle("radar_sureler",
                                                     (pygame.time.get_ticks() - self.modul_baslangic) / 1000)
                                self.modul_baslangic = pygame.time.get_ticks()
                        elif self.durum == "TERMINAL":
                            if self.terminal_modulu.handle_event(olay) == "DOGRU_TERMINAL":
                                self.yildiz_efekti.patlat(mx, my)
                                self.rapor.veri_ekle("terminal_sureler",
                                                     (pygame.time.get_ticks() - self.modul_baslangic) / 1000)
                                self.modul_baslangic = pygame.time.get_ticks()
                        elif self.durum == "SINYAL":
                            if self.sinyal_modulu.handle_event(olay):
                                self.rapor.veri_ekle("sinyal_sureler",
                                                     (pygame.time.get_ticks() - self.modul_baslangic) / 1000)
                                self.modul_baslangic = pygame.time.get_ticks()

                        if self.durum == "ODEV" and 420 < mx < 670 and 120 < my < 170:
                            self.dosya_sec()

                    if olay.type == pygame.KEYDOWN and self.durum in ["OKUYUCU", "ODEV"]:
                        if olay.key == pygame.K_BACKSPACE:
                            self.kullanici_yazisi = self.kullanici_yazisi[:-1]
                        elif olay.key == pygame.K_RETURN:
                            mesaj = self.kullanici_yazisi
                            self.ai_cevabi = "LUMINA DUSUNUYOR..."
                            self.kullanici_yazisi = ""
                            threading.Thread(target=lambda: self.ai_gorevi(mesaj), daemon=True).start()
                        else:
                            if olay.unicode.isprintable(): self.kullanici_yazisi += olay.unicode

            if self.durum == "GIRIS":
                self.profil.ciz_kayit_ekrani(self.input_sirasi, self.motor, self.kayit_bg)
            else:
                self.arayuz_ciz()
                self.profil.profil_ozeti_ciz(self.motor)
                if self.durum == "ANA_MENU":
                    self.motor.ciz(self.ekran, f"HOSGELDIN KAPTAN {self.profil.kullanici_adi.upper()}", (420, 120),
                                   FONT_YOLU, zaman=self.sayac)
                elif self.durum == "RADAR":
                    self.radar_modulu.update();
                    self.radar_modulu.draw()
                elif self.durum == "TERMINAL":
                    self.terminal_modulu.update();
                    self.terminal_modulu.draw()
                elif self.durum == "SINYAL":
                    self.sinyal_modulu.update();
                    self.sinyal_modulu.draw()
                elif self.durum == "ODEV":
                    pygame.draw.rect(self.ekran, KOYU_KREM, (420, 120, 250, 50), border_radius=10)
                    self.motor.ciz(self.ekran, "FOTOGRAF YUKLE", (440, 130), FONT_YOLU, boyut=20, statik=True)
                if self.ai_cevabi: self.uzun_metin_ciz(self.ai_cevabi, 380, 250)
                if self.lumina:
                    self.ekran.blit(self.lumina, (980, 450 + math.sin(self.sayac * 1.5) * 10))
                self.yildiz_efekti.guncelle_ve_ciz(self.ekran)

            pygame.display.flip()

    def ai_gorevi(self, mesaj):
        yanit = self.asistan.resim_analiz_et(
            self.secilen_resim_yolu) if self.durum == "ODEV" and self.secilen_resim_yolu else self.asistan.hatayi_analiz_et(
            mesaj)
        self.ai_cevabi = yanit.upper()
        self.asistan.seslendir(yanit)


if __name__ == "__main__":
    Uygulama().calistir()