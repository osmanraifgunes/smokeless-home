# Smokeless — Tanıtım Sayfası

Smokeless uygulamasının tanıtım sayfası. GitHub Pages üzerinden yayınlanır:
https://osmanraifgunes.github.io/smokeless-home/

- App Store: https://apps.apple.com/app/id6798220798
- Google Play: https://play.google.com/store/apps/details?id=com.org.smokeless

## Yapı

Site, uygulamanın desteklediği 15 dilde yayınlanır: en (kök), tr, es, fr, de, pt, ru, ar, ur, hi, bn, zh, ja, id, vi. Her dilin kendi sayfası (`/tr/`, `/de/`…) ve kendi sosyal medya önizleme görseli vardır.

| Yol | Ne |
|---|---|
| `i18n/<dil>.json` | **Tüm metinlerin kaynağı.** `page` sayfa metinleri, `og` sosyal medya görsel metinleri. |
| `tools/site/page.html` | Sayfa şablonu (`{{anahtar}}` yer tutucuları). |
| `tools/build.py` | Şablon + çevirilerden `index.html`, `<dil>/index.html`, `media.html`, `sitemap.xml` ve `tools/og/strings.js` üretir. |
| `tools/og/` | Sosyal medya görsel şablonu ve render betiği. |
| `assets/img/<dil>/` | Uygulama ekran görüntüleri (en, tr, es, fr, ar, hi, zh; diğer diller `en` kullanır). |
| `assets/og/<dil>/` | Sosyal medya görselleri: 6 konu × 3 format (1200×630, 1080×1080, 1080×1920). |
| `index.html`, `<dil>/index.html`, `media.html`, `sitemap.xml` | **Üretilen dosyalar — elle düzenlemeyin.** |
| `robots.txt` | SEO. |

Yayın: GitHub Pages, "Deploy from branch" (`main` / kök). Her push otomatik yayınlanır.

## Metin değiştirme

1. `i18n/<dil>.json` dosyalarını düzenleyin (yeni anahtar eklerken 15 dosyanın hepsine ekleyin; build eksik anahtarda durur).
2. `python3 tools/build.py`
3. Sosyal medya görsel metni değiştiyse: `tools/og/render.sh` (tümü) veya `tools/og/render.sh main "tr de"`.
4. Görseller değiştiyse `tools/build.py` içindeki `OG_VERSION`'ı artırıp tekrar build alın; sosyal medya önbelleği kırılır.

Gereken: Python 3, macOS + Google Chrome (görseller için). Yeni paket gerekmez.

## Paylaşım linkleri

Her dil kendi linkiyle paylaşılmalı ki önizleme görseli o dilde çıksın: `https://osmanraifgunes.github.io/smokeless-home/tr/` gibi. Eski `?lang=tr` linkleri `/tr/`'ye yönlenir.

## SEO

- Her dilde `canonical`, 15 dil için `hreflang` + `x-default`, Open Graph, Twitter kartı
- JSON-LD: `MobileApplication` ve `FAQPage` (her dilde)
- `robots.txt`, çok dilli `sitemap.xml`

Yayına aldıktan sonra Google Search Console'a siteyi ekleyip `sitemap.xml`'i gönderin. Özel alan adına geçilirse `tools/build.py` içindeki `BASE` ve `robots.txt`'yi değiştirip build alın.

## Yerelde çalıştırma

```sh
python3 -m http.server 8080
```

## Ekran görüntülerini güncelleme

Kaynak: `../smokeless/stores/ios/iphone/1320x2868/<dil>/`.

```sh
sips -s format jpeg -s formatOptions 78 -Z 1100 <kaynak>.png --out assets/img/<dil>/<ad>.jpg
```
