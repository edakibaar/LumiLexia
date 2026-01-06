import pygame
import os


class ProfilSistemi:
    def __init__(self, ekran, font_yolu):
        self.ekran = ekran
        self.font_yolu = font_yolu
        self.kullanici_adi = ""
        self.veli_mail = ""
        self.secilen_avatar_index = 0
        self.avatarlar = []
        # Başlangıçta avatarları yüklüyoruz (Sağ üst köşe için kritik)
        for i in range(1, 6):
            yol = f"assets/images/avatar{i}.png"  # İsimlendirme standardına göre güncellendi
            if os.path.exists(yol):
                img = pygame.image.load(yol).convert_alpha()
                self.avatarlar.append(pygame.transform.scale(img, (100, 100)))
            else:
                self.avatarlar.append(pygame.Surface((100, 100)))

    def ciz_kayit_ekrani(self, aktif_input, motor, arkaplan):
        if arkaplan:
            self.ekran.blit(arkaplan, (0, 0))
        else:
            self.ekran.fill((30, 30, 60))


        motor.ciz(self.ekran, "LUMILEXIA KAYIT", (400, 50), self.font_yolu, boyut=55, statik=False)
        motor.ciz(self.ekran, f"KAPTAN ADI: {self.kullanici_adi}", (350, 200), self.font_yolu, boyut=30, statik=False)
        motor.ciz(self.ekran, f"VELI MAIL: {self.veli_mail}", (350, 300), self.font_yolu, boyut=30, statik=False)

        # --- YENİ AVATAR YERLEŞİMİ (Sola Hizalı ve Büyük) ---
        baslangic_x = 250  # Çizdiğin yeşil alanın sol başı
        y_pos = 400
        kutu_boyutu = 125  # Avatarların daha net görünmesi için büyütüldü
        bosluk = 60  # Yayılması için aralıklar açıldı

        for i in range(5):
            x_pos = baslangic_x + (i * (kutu_boyutu + bosluk))

            # Seçili olanın etrafına Neon Turkuaz kutu çiz (Uzay temasına uygun)
            if self.secilen_avatar_index == i:
                pygame.draw.rect(self.ekran, (0, 255, 255), (x_pos - 8, y_pos - 8, kutu_boyutu + 16, kutu_boyutu + 16),
                                 3, border_radius=15)

            if i < len(self.avatarlar):
                img = pygame.transform.scale(self.avatarlar[i], (kutu_boyutu, kutu_boyutu))
                self.ekran.blit(img, (x_pos, y_pos))
                motor.ciz(self.ekran, str(i + 1), (x_pos + 45, y_pos + kutu_boyutu + 5), self.font_yolu, boyut=20,
                          statik=True)

        motor.ciz(self.ekran, "AVATAR SECMEK ICIN SAYILARA (1-5) BASIN", (360, 610), self.font_yolu, boyut=18,
                  statik=False)
        motor.ciz(self.ekran, "DEVAM ETMEK ICIN ENTER'A BASIN", (350, 660), self.font_yolu, boyut=25, statik=False)

    def profil_ozeti_ciz(self, motor):
        """Sağ üstteki Kaptan Kartı (Avatar ve İsim Yan Yana)"""
        # Şık bir arka plan paneli
        pygame.draw.rect(self.ekran, (40, 40, 80, 200), (1000, 20, 200, 100), border_radius=15)

        # Seçili avatarı küçük ikon olarak çiziyoruz
        if self.secilen_avatar_index < len(self.avatarlar):
            img = pygame.transform.scale(self.avatarlar[self.secilen_avatar_index], (80, 80))
            self.ekran.blit(img, (1015, 30))

        # Kaptan ismini avatarın yanına yazıyoruz
        kaptan_isim = self.kullanici_adi[:10].upper() if self.kullanici_adi else "KAPTAN"
        motor.ciz(self.ekran, kaptan_isim, (1100, 45), self.font_yolu, boyut=25, statik=True)