<div align="center">
  <img src="LumiLexia Disleksi Gelişim Takip ve Eğitim Platformu.jpg" alt="LumiLexia İnfografik" width="100%">
</div>

---

# LumiLexia: Disleksi Gelişim Takip ve Eğitim Platformu

**Ders:** BOZ213 Nesne Yönelimli Programlama (OOP)  
**Proje Türü:** Final Projesi  
**Geliştirici:** Eda Kibar  
**Durum:** Tamamlandı (v1.0)

## Proje Vizyonu

LumiLexia, disleksili çocukların okuma akıcılığını ve görsel dikkatlerini artırmak amacıyla tasarlanmış, uzay temalı bir eğitsel oyun motorudur. Projenin kalbinde, dış kaynaklı kütüphanelere bağımlı kalmadan geliştirilmiş **özgün DyslexiFlow kütüphanesi** yer almaktadır.

## Yazılım Mimarisi ve OOP Prensipleri

Proje, akademik seviyede bir mimariyle, Nesne Yönelimli Programlamanın (OOP) temel direkleri üzerine inşa edilmiştir:

* **İleri Seviye Kalıtım (Inheritance):** Uygulama, `BaseModule` adında soyut bir temel sınıftan türetilmiştir. Radar, Sinyal ve Terminal gibi tüm alt modüller bu sınıftan kalıtım alarak kod tekrarını önler ve merkezi bir yönetim sağlar.
* **Dinamik Çok Biçimlilik (Polymorphism):** Her modül, ana motordan gelen `draw()` ve `handle_event()` komutlarını kendi özel mantığına göre **override** eder.
* **Kapsülleme (Encapsulation) ve Güvenlik:** `DyslexiFlow` motorunun iç mantığı ve kullanıcı verileri sınıflar içinde kapsüllenmiştir. Verilere doğrudan müdahale engellenmiştir.
* **Modüler Tasarım:** Raporlama, AI asistan bağlantısı ve profil yönetimi gibi her sorumluluk ayrı bir sınıfa (Single Responsibility) atanarak sürdürülebilir bir yapı kurulmuştur.

## Teknik Özellikler ve Bileşenler

| Bileşen | Teknik Karşılığı | Fonksiyonu |
| :--- | :--- | :--- |
| **DyslexiFlow** | **Özgün Motor** | **Metinlerin hecelenmesi, hecelerin disleksiye uygun renk paletiyle renklendirilmesi ve "Visual Crowding" önleyici dalgalanma efekti.** |
| **Phonetic Audio** | **Threaded Sound** | **Hecelerle etkileşime girildiğinde fonolojik farkındalık için anlık seslendirme.** |
| **Automated Report** | **SMTP Integration** | **Performans verilerinin HTML formatında veli e-posta adresine iletilmesi.** |
| **Lumina Assistant** | **API Collaboration** | **Kullanıcı süreçlerinin AI altyapısıyla (Gemini) teorik analiz hazırlığı.** |

## Kurulum ve Çalıştırma

Uygulamayı yerel ortamınızda ayağa kaldırmak için aşağıdaki adımları izleyebilirsiniz:

1. **Depoyu Klonlayın:**

```bash
git clone https://github.com/edakibaar/LumiLexia.git
```

2. **Gereksinimleri Yükleyin:**
```bash
pip install pygame google-generativeai python-dotenv
```
3. **Uygulamayı Başlatın:**
```bash
python main__.py
``` 

## Gelecek Vizyonu (Roadmap)
Sürekli gelişim ilkemiz doğrultusunda v2.0 sürümü için planlanan AR-GE çalışmaları:

Pedagojik AI Rehberliği: Hatalı işlemlerde yapay zekanın sesli ve anlık pedagojik ipuçları vermesi.

Kişiselleştirilmiş Müfredat: Algoritmalarımızın, çocuğun disleksi türüne göre zorluk seviyesini dinamik olarak ayarlaması.

## Lisans
Bu proje eğitim amaçlı geliştirilmiştir. Tüm hakları saklıdır.
