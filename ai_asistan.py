import requests
import json
import base64
import threading
import pygame
import os
import time
from gtts import gTTS


class AIAsistan:
    def __init__(self):
        self.api_key = "AIzaSyCt85FRCdPBvFBrdAsecLp8H7HkcZC27ts"
        self.model_adi = "models/gemini-1.5-flash"  # Varsayılan
        self.model_bul()  # Modeli otomatik bul
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    def model_bul(self):
        """Kullanılabilir modelleri listeleyerek en uygun Flash modelini seçer."""
        try:
            list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
            res = requests.get(list_url, timeout=10)
            veriler = res.json()
            if "models" in veriler:
                for m in veriler["models"]:
                    if "generateContent" in m["supportedGenerationMethods"]:
                        if "flash" in m["name"]:
                            self.model_adi = m["name"]
                            break
        except:
            print("Model arama başarısız, varsayılan modelle devam ediliyor.")

    def seslendir(self, metin):
        """Metni temizleyip gTTS ile akıcı bir şekilde seslendirir."""
        if not metin or metin == "lumina dusunuyor...":
            return

        # Tire ve alt çizgileri siler (akıcı okuma için)
        temiz_metin = metin.replace("-", "").replace("_", "").lower()

        def konus():
            try:
                dosya = f"temp_voice_{int(time.time())}.mp3"
                tts = gTTS(text=temiz_metin, lang='tr')
                tts.save(dosya)

                pygame.mixer.music.load(dosya)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                pygame.mixer.music.unload()
                if os.path.exists(dosya):
                    os.remove(dosya)
            except Exception as e:
                print(f"SES HATASI: {e}")

        threading.Thread(target=konus, daemon=True).start()

    def resim_analiz_et(self, resim_yolu):
        url = f"https://generativelanguage.googleapis.com/v1beta/{self.model_adi}:generateContent?key={self.api_key}"
        try:
            with open(resim_yolu, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')

            prompt = ("Sen bir disleksi uzmanısın. Ödevi doğrudan yapma. "
            "Çocuğun hatasını görmesini sağla, ipuçları ver ve rehberlik et. "
            "En fazla 6 kısa cümle kullan. Sadece küçük harflerle yaz.")

            payload = {"contents": [
                {"parts": [{"text": prompt}, {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}]}]}
            response = requests.post(url, json=payload, timeout=25)
            return response.json()['candidates'][0]['content']['parts'][0]['text'].strip().lower()
        except:
            return "baglanti hatasi."

    def hatayi_analiz_et(self, metin):
        url = f"https://generativelanguage.googleapis.com/v1beta/{self.model_adi}:generateContent?key={self.api_key}"
        payload = {"contents": [
            {"parts": [{"text": f"disleksili çocuğa Türkçe ve küçük harflerle kısa açıklama yap: {metin}"}]}]}
        try:
            res = requests.post(url, json=payload, timeout=10)
            return res.json()['candidates'][0]['content']['parts'][0]['text'].strip().lower()
        except:
            return "baglanti hatasi"