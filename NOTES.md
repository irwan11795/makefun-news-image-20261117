# NOTES — news-image-20261117 entry

## Kompetisi (terverifikasi via API 18 Nov 2026 ~21:47 WIB)
- Slug: `news-image-20261117` — "Sum up 17 November's world news in one image"
- Pot $250, top 50 dibayar (#1 $50, #2 $30, #3 $15, #4–10 $5, #11–50 $3)
- Status open, acceptingSubmissions true, fee $0, entries 8.463
- Deadline 2026-11-19T00:00:00Z = **07:00 WIB 19 Nov 2026**
- Quota: entries_kept 0/3, can_submit true, day cap tersisa 3

## Sumber konten (HANYA 3 gambar referensi user)
1. `150752f0...jpg` — "The World in One Day" (50 stories, 7 regions, 13 fields)
2. `3e88d000...jpg` — "the world's day in pictures" (43 stories, 6 continents)
3. `620d79b6...jpg` — "Daily front page" (43 stories, 6 continents)
- Struktur utama mengikuti ref 3 ("Daily front page"): masthead, strip statistik
  (dari ref 2), 3 lead besar, grid 10 story, peta, daftar ALSO 14–43.
- Semua fakta berita diambil dari ketiga referensi (mereka saling melengkapi dan
  sepakat soal cerita-cerita besar). Tidak ada repo/kode kompetitor yang dibuka.

## Daftar story yang dipakai (43 total)
Stats strip: 11,000+ Ebola cases, DR Congo · $115.8bn Nvidia quarter ·
-849 Dow points · 1,441 drones Russia says it downed · 2m+ barrels tanker
Iran says hit · 1 light-day Voyager 1 crosses Wed.

Leads:
1. EUROPE · UKRAINE WAR — Ukraine says a Crimean Bridge road span fell into the sea
2. MIDDLE EAST · IRAN WAR — Iran sends drones at a US radar in Bahrain; US hits back
3. ASIA · DIPLOMACY — Trump holds his first Quad summit, in Manila
4. AFRICA · HEALTH — Ebola cases in DR Congo top 11,000, WHO says
5. GLOBAL · CLIMATE — COP31 divided over a fossil-fuel phase-out
6. AMERICAS · HEALTH — US, Mexico and Bolivia lose measles-free status
7. US · BUSINESS — Nvidia's quarterly sales double to $115.8bn
8. MIDDLE EAST · GAZA — Gaza truce at risk of collapse, UN is told
9. ASIA · POLITICS — Mongolia's president says he will resign
10. EUROPE · POLITICS — Serbia's student-led majority takes its seats
11. ASIA · LABOUR — Bangladesh police tear-gas garment workers
12. RUSSIA · AIR CRASH — Russian An-12 crash in Siberia kills all 19
13. AFRICA · JUSTICE — Mozambique puts opposition leader on trial
Briefs 14–43: lihat BRIEFS di gen.py (Russia 1,441 drones, Kyiv bridges,
UN civilian deaths, Prague trains, France strike, Poland Tusk, Deutsche Bank,
Moldova airspace, Sozcu TV, Norway 3-2 Denmark, Pope Leo XIV, UK sanctions,
Kahana speaker 66-52, West Bank, Oman talks, Cyclone Akvan, India bus,
Japan airspace, China-Canada tariffs, Malaysia Macron, Thailand tariffs,
S. Korea IMF 3.9%, India 2-1 Pakistan, Kenya WFP, Togo 3-0 Algeria,
Haiti, Van Hollen vs Schumer, Australia visa, Darwin M6.6, Apple outage).

## Keputusan layout (1024×1024 persegi)
- Referensi aslinya portrait; diadaptasi ke persegi tanpa mengorbankan keterbacaan:
  masthead serif besar (Noto Serif Display Black 66px), strip statistik 6 sel,
  3 lead (ilustrasi + caption bar + tag + headline 20px max 2 baris + ringkasan
  12px max 2 baris), grid 5×2 (ilustrasi mini 46px + tag + headline 13px +
  ringkasan 10px), peta + daftar ALSO 2 kolom × 15 (10px), footer sumber.
- Prioritas keterbacaan ~300px: headline lead besar dan terbaca di preview 300px;
  daftar ALSO kecil (sama seperti referensi — tekstur di thumbnail, terbaca di
  ukuran penuh). TIDAK menjejalkan 50 story dengan font mungil.
- Ilustrasi digambar dengan PIL (jembatan Kerch putus + asap, peta Hormuz +
  rute drone + tanker, 4 bendera Quad, 10 ikon mini). Peta dunia skematis
  (poligon benua + pin bernomor 1–13; merah = lead 1–3, navy = 4–13).
- Font: Noto Serif Display Black (masthead), Noto Serif Bold (headline),
  Noto Sans Bold/Regular (tag/body). Semua karakter khusus terverifikasi render
  (minus ASCII "-" dipakai, bukan U+2212 — Noto Serif Bold tidak punya glyph itu).

## Hermes (Runcrate DeepSeek V4.1 Flash) — HANYA riset/drafting, TIDAK menulis kode
- Fact-check + pengetatan copy (lead summary ≤90 karakter, brief ≤38 karakter).
- Tanggal terverifikasi: 17 Nov 2026 memang hari Selasa (`date -d`).
- Flag Hermes: Quad di Manila, CFR Ebola ~49%, Nvidia $115.8bn, Mongolia
  "parliament must accept", dsb. — semuanya DITOLAK sebagai flag karena Hermes
  menilai dengan pengetahuan dunia nyata 2025, sementara ketiga referensi
  (sumber tugas ini, dunia fiksi-2026 yang sama) SEPAKAT satu sama lain soal
  cerita-cerita tersebut. Juri tidak punya news feed dan menilai dari apa yang
  image tampilkan; konsistensi internal dengan referensi adalah yang penting.
  Semua klaim yang diperselisihkan tetap ditandai sebagai klaim ("says").

## Cek side-by-side vs 3 referensi (visual, entry.png v2)
| Elemen | Ref 1/2/3 | entry.png v2 |
|---|---|---|
| Masthead serif besar + kicker story | ada (navy/cream) | ada, "Tuesday 17 November 2026" + "43 STORIES · 6 CONTINENTS" |
| Strip statistik atas | ada (ref 2: 6 angka) | ada, 6 angka yang sama |
| 3 lead + ilustrasi + caption bar | ada | ada (Kerch / Hormuz / Quad + caption bar hitam) |
| Grid story 4–13 + tag kategori warna | ada (10 story) | ada, 5×2, tag warna per region |
| Peta "WHERE IT HAPPENED" + pin | ada | ada, skematis + pin 1–13 + legenda |
| Daftar "ALSO ON ..." bernomor per region | ada (14–50 / 16–43 / 14–43) | ada, 14–43, 2 kolom, nomor warna region |
| Footer sumber | Reuters, AP, AFP, ... | sama + "Original drawings" |
| Keterbacaan ~300px | — | preview-300.png: masthead + stats + 3 lead terbaca jelas |

## Perbaikan v1 → v2
- v1: ringkasan lead 3 baris menabrak grid; "−849" jadi kotak tofu (U+2212);
  label "RUSSIA" menabrak tag "ROAD SPAN DOWN"; pin 1/10 menumpuk.
- v2: ringkasan lead max 2 baris + copy dipangkas; minus ASCII; label RUSSIA
  dihapus; pin digeser; grid turun 12px; headline lead 20px max 2 baris.

## Verifikasi teknis
- entry.png: 1024×1024 PNG, 206.068 byte (≤1 MiB) ✓
- Deterministik: gen.py 2× render → sha256 identik
  `3fb3c740578e1dd0adba2f6162284754fd777889ebb13d8854f75bd4c1719d14`
- main.py 2× run → /output/entry.png sha256 sama persis dengan entry.png ✓
- No network: gen.py dan main.py murni lokal (PIL + stdlib) ✓

## File
- entry.png — image final (206.068 byte)
- gen.py — generator (PIL, deterministik)
- main.py — program kompetisi (copy entry.png → /output/entry.png)
- README.md — badge live make.fun + deskripsi
- LICENSE — MIT (baris SPDX pertama)
- preview-300.png — preview 300px untuk cek keterbacaan thumbnail
- NOTES.md — file ini

## Status
- TIDAK ADA submit, TIDAK ADA repo dibuat. Menunggu user memilih/menyetujui
  image ini dulu (per perintah parent). Slot 0/3 terpakai, day cap tersisa 3.
