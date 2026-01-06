import math
import pygame


class DyslexiFlow:  # İsim değiştirildi
    def __init__(self):
        self.sesli_harfler = "aeıioöuüAEIİOÖUÜ"
        self.renk_paleti = [(70, 130, 180), (107, 142, 35), (188, 143, 143), (153, 101, 21), (102, 102, 153),
                            (85, 107, 47)]
        self.son_cizilen_heceler = []

    def hecele(self, kelime):
        # Orijinal algoritman dokunulmadan korundu
        if not kelime: return []
        heceler = []
        gecici = ""
        i = 0
        while i < len(kelime):
            gecici += kelime[i]
            if kelime[i] in self.sesli_harfler:
                if i + 1 < len(kelime):
                    if kelime[i + 1] not in self.sesli_harfler:
                        if i + 2 < len(kelime) and kelime[i + 2] not in self.sesli_harfler:
                            gecici += kelime[i + 1]
                            heceler.append(gecici)
                            gecici = ""
                            i += 1
                        elif i + 2 < len(kelime) and kelime[i + 2] in self.sesli_harfler:
                            heceler.append(gecici)
                            gecici = ""
                        elif i + 2 >= len(kelime):
                            gecici += kelime[i + 1:]
                            heceler.append(gecici)
                            gecici = ""
                            break
                else:
                    heceler.append(gecici)
                    gecici = ""
            i += 1
        if gecici:
            if heceler:
                heceler[-1] += gecici
            else:
                heceler.append(gecici)
        return [h for h in heceler if h]

    def ciz(self, ekran, metin, pos, font_yolu, boyut=45, zaman=0, statik=False):
        if not metin: return

        # EKLEME: Eğer zaman verilmediyse Pygame'in kendi saatini kullan
        if zaman == 0:
            zaman = pygame.time.get_ticks() / 1000.0

        font = pygame.font.Font(font_yolu, boyut)
        x, y = pos
        gecici_x = x
        self.son_cizilen_heceler = []

        yavas_zaman = zaman * 2.5

        for kelime in metin.split():
            hece_listesi = self.hecele(kelime)
            for i, hece in enumerate(hece_listesi):
                renk = self.renk_paleti[i % len(self.renk_paleti)]
                y_off = 0 if statik else math.sin(yavas_zaman + gecici_x * 0.05) * 2

                yuzey = font.render(hece, True, renk)
                hece_rect = yuzey.get_rect(topleft=(gecici_x, y + y_off))

                ekran.blit(yuzey, hece_rect)
                self.son_cizilen_heceler.append({"rect": hece_rect, "metin": hece})
                gecici_x += yuzey.get_width()

            gecici_x += font.size(" ")[0]

    def etkilesim_kontrol(self, fare_pos, asistan):
        for h in self.son_cizilen_heceler:
            if h["rect"].collidepoint(fare_pos):
                asistan.seslendir(h["metin"])
                return h["metin"]
        return None