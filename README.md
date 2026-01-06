LumiLexia: Disleksi Gelişim Takip Platformu

LumiLexia, disleksili çocukların okuma akıcılığını ve fonolojik farkındalıklarını artırmak amacıyla geliştirilmiş, oyunlaştırma tabanlı bir eğitsel oyun motorudur. Proje, öğrenme sürecini bir uzay görevine dönüştürerek disleksiyle ilişkilendirilen stres ve kaygıyı minimize etmeyi hedefler.

Proje Amacı ve Vizyonu

Temel hedef, oyunlaştırılmış bir ortamda görsel dikkat ve fonetik işleme süreçlerini takip etmektir. Uygulama, kullanıcının farklı bilişsel görevlerdeki tepki sürelerini ve doğruluk oranlarını hassas bir şekilde ölçer. Elde edilen veriler sadece kaydedilmekle kalmaz, aynı zamanda veliler ve eğitimciler için anlamlı içgörülere dönüştürülür. Bu sayede oyun ile klinik gözlem arasında dijital bir köprü kurulur.

Öne Çıkan Özellikler

DyslexiFlow Kütüphanesi: Bu proje için özel olarak geliştirilen bir motordur. Kelimeleri dinamik olarak hecelerine ayırır ve metne dalgalanma efekti verir. Bu sayede disleksili bireylerin sıkça yaşadığı görsel kalabalık (visual crowding) etkisini azaltarak okumayı kolaylaştırır.

İşitsel Geri Bildirim: Kullanıcı hecelere tıkladığında veya heceleri birleştirdiğinde, sistem ilgili ses birimlerini seslendirerek fonolojik farkındalığı destekler.

AI İşbirliği ve Pair Programming: Proje geliştirme süreci, yapay zeka asistanı ile interaktif bir şekilde yürütülmüştür. Gemini API entegrasyonu sayesinde kullanıcı hataları analiz edilir ve Lumina karakteri üzerinden rehberlik sağlanır.

Otomatik Raporlama: Oturum sonunda Radar, Sinyal ve Terminal modüllerinden gelen performans verileri işlenir. Bu veriler profesyonel bir HTML raporuna dönüştürülerek velinin e-posta adresine otomatik olarak iletilir.

Teknik Mimari (OOP)

Yazılımın temeli Nesne Yönelimli Programlama (OOP) prensiplerine dayanmaktadır. BaseModule sınıfı kullanılarak Inheritance ve Polymorphism ilkeleri etkin bir şekilde uygulanmıştır. Her oyun modülü temel özellikleri bu sınıftan devralırken, kendi özgün mantığını aşağıdaki görevler üzerinden yürütür:

Radar: Yanlış yazılmış kelimeleri tespit ederek görsel ayırt etme yeteneğini geliştirir.

Sinyal: Mıknatıs mekanizmasıyla heceleri birleştirerek fonetik bağ kurmayı güçlendirir.

Terminal: Hızlı isimlendirme ve nesne-kelime eşleştirmesini destekler.

Kurulum ve Gereksinimler

Uygulamayı çalıştırmak için aşağıdaki kütüphanelerin yüklü olması gerekmektedir: pip install pygame google-generativeai python-dotenv

Önemli Not: Projenin çalışması için gerekli olan Gemini API key ve e-posta gönderimi için kullanılan App Password bilgileri, geliştirme sürecindeki teknik zorunluluklar nedeniyle doğrudan ilgili kod blokları içerisinde tanımlanmıştır. .env dosyasının konfigürasyon aşamasında yaşanabilecek olası erişim hatalarını önlemek adına bu yöntem tercih edilmiştir. Kurulumdan sonra main__.py dosyasını çalıştırarak uzay görevine başlayabilirsiniz.
