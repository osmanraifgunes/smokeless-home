# Smokeless — Tanıtım Sayfası

Smokeless uygulamasının App Store ve Google Play linklerini içeren statik tanıtım sayfası. GitHub Pages üzerinden yayınlanır.

- App Store: https://apps.apple.com/app/id6798220798
- Google Play: https://play.google.com/store/apps/details?id=com.org.smokeless

## Yapı

- `index.html` — tek sayfa (TR/EN, CSS ve JS satır içi, harici bağımlılık yok)
- `assets/img/` — ikon ve ekran görüntüleri (`tr/`, `en/`)
- `.github/workflows/pages.yml` — `main`'e push edildiğinde GitHub Pages'e deploy

## Yerelde çalıştırma

```sh
python3 -m http.server 8080
```

## Ekran görüntülerini güncelleme

Kaynak: `../smokeless/stores/ios/iphone/1320x2868/<dil>/`. Örnek:

```sh
sips -s format jpeg -s formatOptions 78 -Z 1100 <kaynak>.png --out assets/img/tr/<ad>.jpg
```

## İlk kurulum

Repo ayarlarında **Settings → Pages → Source: GitHub Actions** seçilmelidir.
