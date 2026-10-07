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

VarAtlas'ın kamuya açık açıklama sayfası, program detaylarında yerleşenlerin geldikleri iller ve coğrafi dağılım özetleri sunduğunu belirtiyor. İncelenen [Hacettepe Çağdaş Türk Lehçeleri ve Edebiyatları sayfası](https://varatlas.com/detay/hacettepe-universitesi-cagdas-turk-lehceleri-ve-edebiyatlari-4-yillik-104810838), veriyi “adayların mezun oldukları liselerin konumlarına göre” tanımlıyor. Bu, **üniversitenin tüm öğrencilerinin illeri** değil, tek bir programın yerleşen adayları için lise konumundan türetilmiş bir dağılımdır; mevcut dashboard'un `ilde ikamet eden öğrenci` tanımıyla doğrudan eşdeğer değildir.

7 Ekim 2026 tarihinde kontrol edilen `https://varatlas.com/robots.txt` dosyası genel sayfalara izin verirken `kontenjan_data.json`, `kontenjan_search.json` ve `.gz` veri dökümlerini `Disallow` ediyor. Ana sayfa ve üniversite sayfaları dinamik içerik yüklediği için doğrudan tarayıcıdan güvenilir, CORS uyumlu bir veri akışı da bulunamadı. Kullanım koşullarının otomatik scraping için açık bir izin verdiği doğrulanamadı.

İncelenen sayfanın HTML'inde program kimliğiyle çağrılan `https://data.varatlas.com/jsons_merged/104810838.json` adresi de görüldü ve tek bir düşük hızlı doğrulama isteğiyle erişilebildi. Bu payload program metriklerinin yanı sıra lise bazında okul adları içerebildiğinden toplu olarak çekilip dashboard'a aktarılmadı. Ayrıca bu endpoint için herkese açık bir API sözleşmesi, lisans veya kullanım izni bulunamadı; `robots.txt` bu yolu açıkça yasaklamasa da bu, otomatik kullanım izni anlamına gelmez.

VarAtlas'ın iddia ettiği upstream kaynaklar [ÖSYM YKS yerleştirme kılavuzları](https://www.osym.gov.tr/) ve [resmî YÖK Atlas](https://yokatlas.yok.gov.tr/). Ancak il dağılımının ÖSYM/YÖK tarafında herkese açık, belgelenmiş ve doğrudan indirilebilir bir endpoint'i doğrulanamadı. Bu nedenle uygulama VarAtlas'ı otomatik crawl etmez, robots kısıtlı veri dökümlerini çağırmaz, CORS'u aşmaya çalışmaz ve VarAtlas değerlerini gerçek üniversite toplamı gibi sunmaz.

Kullanıcı, VarAtlas'taki ilgili program sayfasından kamuya açık ve kişisel olmayan toplulaştırılmış tabloyu kendi tarayıcısıyla indirip/CSV'ye dönüştürüp yükleyebilir. Kaynak ve erişim tarihini `kaynak` alanında görünür tutun; örneğin `VarAtlas program sayfası, erişim 2026-10-07`. Bu akış, güvenli manuel indirme + yerel içe aktarma yaklaşımıdır. VarAtlas/ÖSYM/YÖK Atlas için bu proje içinde ayrıca bir lisans varsayılmaz; kullanımda ilgili sitelerin güncel koşulları kontrol edilmelidir.

## Notlar

- Başlangıç ekranındaki kayıtlar **sentetik demo veridir; gerçek Hacettepe dağılımını temsil etmez**.
- İl yoğunluğu, erişilebilir sıralama ve ilk 10 SVG/PNG grafiği tarayıcıda oluşturulur.
- Instagram önizlemesi 1080 × 1350 oranındadır.
- Gerçek veri kullanırken YÖK Atlas veya VarAtlas'tan ilgili toplulaştırılmış veriyi yetkili/kamuya açık sayfadan indirin; `il` ve `ogrenci_sayisi` sütunlarını düzenleyip `yil`/`kaynak` ve erişim tarihini ekleyin. Resmi kaynağın lisans ve kullanım koşullarını kontrol edin.
