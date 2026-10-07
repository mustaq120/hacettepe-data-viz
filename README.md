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

## Notlar

- Başlangıç ekranındaki kayıtlar **sentetik demo veridir; gerçek Hacettepe dağılımını temsil etmez**.
- İl yoğunluğu, erişilebilir sıralama ve ilk 10 SVG/PNG grafiği tarayıcıda oluşturulur.
- Instagram önizlemesi 1080 × 1350 oranındadır.
- Gerçek veri kullanırken YÖK Atlas’tan ilgili veriyi resmi kanallardan indirin; `il` ve `ogrenci_sayisi` sütunlarını düzenleyip gerekirse `yil`/`kaynak` ekleyin. Resmi kaynağın lisans ve kullanım koşullarını kontrol edin.
