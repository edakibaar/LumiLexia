import os
import smtplib
import threading
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MAIL_AYARLARI = {
    "ADRES": "MAİL-ADRESİN",
    "SIFRE": "MAİL-SİFREN"
}


class RaporlamaSistemi:
    def __init__(self, asistan):
        self.asistan = asistan
        self.veriler = {
            "radar_sureler": [],
            "sinyal_sureler": [],
            "terminal_sureler": [],
            "hatalar": []
        }

    def veri_ekle(self, tur, deger):
        if tur in self.veriler:
            self.veriler[tur].append(deger)

    def rapor_hazirla_ve_gonder(self, profil):
        try:
            # 1. Veri Analizi
            radar_avg = sum(self.veriler["radar_sureler"]) / len(self.veriler["radar_sureler"]) if self.veriler[
                "radar_sureler"] else 0
            sinyal_avg = sum(self.veriler["sinyal_sureler"]) / len(self.veriler["sinyal_sureler"]) if self.veriler[
                "sinyal_sureler"] else 0
            terminal_avg = sum(self.veriler["terminal_sureler"]) / len(self.veriler["terminal_sureler"]) if \
            self.veriler["terminal_sureler"] else 0

            # 2. AI Analizi (Retry Mekanizması Eklendi)
            prompt = f"""
            Kaptan {profil.kullanici_adi} için profesyonel disleksi gelişim raporu:
            - Radar (Görsel Dikkat) Hızı: {radar_avg:.2f}s
            - Sinyal (Fonolojik Farkındalık) Hızı: {sinyal_avg:.2f}s
            - Terminal (Sıralama/Hız): {terminal_avg:.2f}s
            Lumina olarak; ebeveyne yönelik, nörobilimsel temelli ama umut verici bir özet yaz. 
            Kelime karıştırma (p-b-d) eğilimlerini ve akıcı okuma potansiyelini değerlendir.
            """

            ai_analizi = "bağlantı hatası"
            for _ in range(3):  # 3 kez deneme yapar
                try:
                    yanit = self.asistan.hatayi_analiz_et(prompt)
                    if yanit and "hata" not in yanit.lower():
                        ai_analizi = yanit
                        break
                except:
                    time.sleep(1)  #

            # 3. HTML Mail Tasarımı
            mesaj = MIMEMultipart("alternative")
            mesaj["From"] = MAIL_AYARLARI["ADRES"]
            mesaj["To"] = profil.veli_mail
            mesaj["Subject"] = f"LumiLexia Gelişim Raporu: Kaptan {profil.kullanici_adi}"

            html_icerik = f"""
            <html>
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #2c3e50; line-height: 1.6;">
                <div style="max-width: 600px; margin: auto; border: 1px solid #e0e0e0; border-radius: 10px; overflow: hidden;">
                    <div style="background-color: #1a1a2e; color: #ffffff; padding: 20px; text-align: center;">
                        <h1 style="margin: 0;">LumiLexia </h1>
                        <p style="margin: 5px 0 0 0;">Disleksi Takip Sistemi</p>
                    </div>

                    <div style="padding: 30px;">
                        <h2 style="color: #3498db; border-bottom: 2px solid #f1f1f1; padding-bottom: 10px;">Sayın Veli,</h2>
                        <p>Kaptan <strong>{profil.kullanici_adi}</strong> bugün galaksimizdeki kritik görevlerini tamamladı. Elde edilen performans verileri aşağıda analiz edilmiştir:</p>

                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr style="background-color: #f8f9fa;">
                                <th style="text-align: left; padding: 12px; border: 1px solid #dee2e6;">Görev Alanı</th>
                                <th style="text-align: center; padding: 12px; border: 1px solid #dee2e6;">Ortalama Performans</th>
                            </tr>
                            <tr>
                                <td style="padding: 12px; border: 1px solid #dee2e6;">Görsel Ayrıştırma (Radar)</td>
                                <td style="text-align: center; padding: 12px; border: 1px solid #dee2e6;">{radar_avg:.2f} Saniye</td>
                            </tr>
                            <tr>
                                <td style="padding: 12px; border: 1px solid #dee2e6;">Fonolojik Birleştirme (Sinyal)</td>
                                <td style="text-align: center; padding: 12px; border: 1px solid #dee2e6;">{sinyal_avg:.2f} Saniye</td>
                            </tr>
                            <tr>
                                 <td style="padding: 12px; border: 1px solid #dee2e6;">Hız ve Sıralama (Terminal)</td>
                                 <td style="text-align: center; padding: 12px; border: 1px solid #dee2e6;">{terminal_avg:.2f} Saniye</td>
                            </tr>
                        </table>

                        <div style="background-color: #e8f4fd; padding: 20px; border-left: 5px solid #3498db; margin-top: 20px;">
                            <h3 style="margin-top: 0; color: #2980b9;">LUMINA Yapay Zeka Analizi</h3>
                            <p style="font-style: italic;">"{ai_analizi}"</p>
                        </div>

                        <p style="margin-top: 25px; font-size: 14px; color: #7f8c8d;">
                            *Bu rapor LumiLexia oyun motoru tarafından otomatik olarak oluşturulmuştur. Bilimsel veriler oyun sırasındaki tepki hızlarına dayanmaktadır.
                        </p>
                    </div>

                    <div style="background-color: #f1f1f1; padding: 15px; text-align: center; font-size: 12px; color: #95a5a6;">
                        LumiLexia Projesi - Disleksi Farkındalık ve Eğitim Platformu
                    </div>
                </div>
            </body>
            </html>
            """

            mesaj.attach(MIMEText(html_icerik, "html"))

            # 4. Gönderim
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(MAIL_AYARLARI["ADRES"], MAIL_AYARLARI["SIFRE"])
                server.send_message(mesaj)
                print(f"PROFESYONEL RAPOR: {profil.veli_mail} adresine iletildi!")

        except Exception as e:
            print(f"RAPORLAMA HATASI: {e}")