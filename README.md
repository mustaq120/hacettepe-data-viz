# Hacettepe İl Dağılımı

Hacettepe öğrencilerini il bazında keşfetmek için hazırlanmış, **bağımlılıksız** ve mobil uyumlu statik dashboard. Yalnızca `index.html`, `styles.css` ve `app.js` ile çalışır; derleme veya sunucu gerektirmez.

## Çalıştırma

`index.html` dosyasını tarayıcıda açın. İsterseniz klasörü herhangi bir statik sunucuyla servis edin (ör. `python -m http.server`). İnternet bağlantısı gerekmez.

## Veri formatları

CSV veya JSON yükleyebilirsiniz. Zorunlu alanlar:

```csv
il,ogrenci_sayisi
Ankara,980
```

İsteğe bağlı alanlar `yil` ve `kaynak`tır. JSON, nesne dizisi olmalıdır: `[{"il":"Ankara","ogrenci_sayisi":980,"yil":"2024-2025","kaynak":"YÖK Atlas"}]`. Aynı il birden fazla satırda varsa değerler birleştirilir. `sample-data.csv` örnek dosyadır.

## VarAtlas kullanımı ve sınırlar

VarAtlas'ın kamuya açık açıklama sayfası, program detaylarında yerleşenlerin geldikleri iller ve coğrafi dağılım özetleri sunduğunu belirtiyor. Hacettepe için bu veri **program bazında** görünüyor; sitede tüm üniversite öğrencilerinin tek, doğrulanmış il toplamını bu proje adına sağlayan bir kamu API'si doğrulanmadı.

7 Ekim 2026 tarihinde kontrol edilen `https://varatlas.com/robots.txt` dosyası genel sayfalara izin verirken `kontenjan_data.json`, `kontenjan_search.json` ve `.gz` veri dökümlerini `Disallow` ediyor. Ana sayfa ve üniversite sayfaları dinamik içerik yüklediği için doğrudan tarayıcıdan güvenilir, CORS uyumlu bir veri akışı da bulunamadı. Kullanım koşullarının otomatik scraping için açık bir izin verdiği doğrulanamadı.

Bu nedenle uygulama VarAtlas'ı otomatik crawl etmez, robots kısıtlı veri uç noktalarını çağırmaz ve CORS'u aşmaya çalışmaz. Kullanıcı, VarAtlas'taki ilgili program sayfasından kamuya açık ve kişisel olmayan toplulaştırılmış tabloyu kendi tarayıcısıyla indirip/CSV'ye dönüştürüp yükleyebilir. Kaynak ve erişim tarihini `kaynak` alanında görünür tutun; örneğin `VarAtlas, erişim 2026-10-07`. Bu akış, güvenli manuel indirme + yerel içe aktarma yaklaşımıdır.

## Notlar

- Başlangıç ekranındaki kayıtlar **sentetik demo veridir; gerçek Hacettepe dağılımını temsil etmez**.
- İl yoğunluğu, erişilebilir sıralama ve ilk 10 SVG/PNG grafiği tarayıcıda oluşturulur.
- Instagram önizlemesi 1080 × 1350 oranındadır.
- Gerçek veri kullanırken YÖK Atlas veya VarAtlas'tan ilgili toplulaştırılmış veriyi yetkili/kamuya açık sayfadan indirin; `il` ve `ogrenci_sayisi` sütunlarını düzenleyip `yil`/`kaynak` ve erişim tarihini ekleyin. Resmi kaynağın lisans ve kullanım koşullarını kontrol edin.
