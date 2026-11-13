# Smokeless — Tanıtım Sayfası

Smokeless uygulamasının tanıtım sayfası. GitHub Pages üzerinden yayınlanır:
https://osmanraifgunes.github.io/smokeless-home/

- App Store: https://apps.apple.com/app/id6798220798
- Google Play: https://play.google.com/store/apps/details?id=com.org.smokeless

## Yapı

| Yol | Ne |
|---|---|
| `index.html` | Tek sayfa. Varsayılan dil İngilizce; Türkçe `?lang=tr` ile ya da TR düğmesiyle açılır. CSS/JS satır içi, harici bağımlılık yok. |
| `media.html` | Medya kiti: tüm sosyal medya görselleri, indirilebilir. |
| `assets/img/` | İkon ve uygulama ekran görüntüleri (`en/`, `tr/`). |
| `assets/og/` | Sosyal medya görselleri: 6 konu × 2 dil × 3 format (1200×630, 1080×1080, 1080×1920). |
| `tools/og/` | Bu görselleri üreten şablon ve betik. |
| `robots.txt`, `sitemap.xml` | SEO. |
| `.github/workflows/pages.yml` | `main`'e push edildiğinde GitHub Pages'e deploy. |

## Dil

Metinler `index.html` içinde İngilizce durur (arama motorları ve sosyal medya botları bunu görür). Türkçe karşılıklar sayfanın sonundaki `I18N.tr` sözlüğündedir; yeni metin eklerken iki sözlüğe de aynı `data-i18n` anahtarıyla ekleyin.

## Sosyal medya görsellerini yeniden üretme

macOS + Google Chrome gerekir, yeni paket gerekmez.

```sh
tools/og/render.sh                  # tümü
tools/og/render.sh "main widget" en # belirli konular / dil
```

Metinler `tools/og/template.html` içindeki `T` sözlüğündedir.

## SEO

- `canonical`, `hreflang` (en, tr, x-default), Open Graph, Twitter kartı
- JSON-LD: `MobileApplication` ve `FAQPage`
- `robots.txt` ve `sitemap.xml`

Yayına aldıktan sonra Google Search Console'a siteyi ekleyip `sitemap.xml`'i gönderin. Özel alan adına geçilirse `index.html`, `media.html`, `robots.txt` ve `sitemap.xml` içindeki `osmanraifgunes.github.io/smokeless-home/` adresini değiştirin.

## Yerelde çalıştırma

```sh
python3 -m http.server 8080
```

## Ekran görüntülerini güncelleme

Kaynak: `../smokeless/stores/ios/iphone/1320x2868/<dil>/`.

```sh
sips -s format jpeg -s formatOptions 78 -Z 1100 <kaynak>.png --out assets/img/en/<ad>.jpg
```
