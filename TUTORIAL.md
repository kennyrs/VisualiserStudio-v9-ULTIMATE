# 📚 VisualiserStudio - Kompletan Tutorial

Detaljno uputstvo za sve funkcionalnosti aplikacije.

---

## 📖 Sadržaj

1. [Instalacija](#instalacija)
2. [Prvi Projekat](#prvi-projekat)
3. [Rad sa Elementima](#rad-sa-elementima)
4. [Audio Visualizer](#audio-visualizer)
5. [Tekst i Stilizovanje](#tekst-i-stilizovanje)
6. [Export Video](#export-video)
7. [Napredne Tehnike](#napredne-tehnike)
8. [Troubleshooting](#troubleshooting)

---

## 1. Instalacija

### Windows

```batch
# 1. Preuzmi i instaliraj Python 3.8+
#    https://www.python.org/downloads/

# 2. Pokreni instalacioni script
install.bat

# 3. Pokreni aplikaciju
run.bat
```

### Linux/Mac

```bash
# 1. Instalacija (automatska)
chmod +x install.sh
./install.sh

# 2. Pokretanje
./run.sh
```

### Ručna Instalacija

```bash
# 1. Instaliraj dependencies
pip install -r requirements.txt

# 2. Kreiraj strukturu
python setup_and_run.py

# 3. Pokreni
python main.py
```

---

## 2. Prvi Projekat

### Korak 1: Učitaj Audio (30 sekundi)

1. **Otvori aplikaciju**
   ```bash
   python main.py
   ```

2. **Media Panel** (leva strana)
   - Klikni **"Browse"** pod "Audio File"
   - Izaberi MP3/WAV fajl
   - ✓ Audio se automatski učitava
   - Timeline prikazuje trajanje

**Podržani formati:**
- MP3 (najčešći)
- WAV (najbolji kvalitet)
- OGG
- FLAC (lossless)
- M4A

### Korak 2: Dodaj Visualizer (10 sekundi)

1. **Visualizer Panel** (desna strana)
2. Klikni **"➕ Add Visualizer"**
3. ✓ Visualizer se pojavljuje u centru

**Šta se dešava:**
- Element se kreira na poziciji (960, 540)
- Default veličina: 800x300px
- Default tip: BARS
- Default gradient: Ocean

### Korak 3: Preview (20 sekundi)

1. **Play Kontrole** (ispod canvas-a)
2. Klikni **"▶ Play"**
3. Posmatraj kako se visualizer kreće sa muzikom
4. Klikni **"⏸ Pause"** da pauziraš

**Kontrole:**
- **▶ Play** - Pokreni playback
- **⏸ Pause** - Pauziraj
- **⏹ Stop** - Vrati na početak
- **Timeline Slider** - Skroluj kroz audio

---

## 3. Rad sa Elementima

### Selektovanje Elementa

**Kako:**
- Klikni na element u preview-u
- Element dobija **cyan (plavi) border**
- Prikazuju se **8 resize handle-a**

**Signali da je element selektovan:**
```
✓ Plavi isprekidani border
✓ Beli kvadratići na uglovima
✓ Cursor se menja prilikom hover-a
```

### Pomeranje (Drag & Drop)

**Metoda 1: Drag & Drop**
1. Klikni na element (bilo gde osim handle-a)
2. Drži levi klik miša
3. Pomeri na željenu poziciju
4. Pusti klik
5. ✓ Pozicija automatski sačuvana

**Metoda 2: Numerički Unos** (future)
- X koordinata: 0 do 1920 (1080p)
- Y koordinata: 0 do 1080 (1080p)

**Tips:**
```
Centar (1080p): X=960, Y=540
Gornji levi ugao: X=0, Y=0
Donji desni ugao: X=1920, Y=1080
```

### Resize (Promeni Veličinu)

**8 Resize Handle-a:**

```
┌───────┬───────┬───────┐
│  TL   │   T   │  TR   │  TL = Top Left
├───────┼───────┼───────┤  T  = Top
│   L   │       │   R   │  TR = Top Right
├───────┼───────┼───────┤  L  = Left
│  BL   │   B   │  BR   │  R  = Right
└───────┴───────┴───────┘  B  = Bottom
                           BL = Bottom Left
                           BR = Bottom Right
```

**Kako:**
1. Selektuj element
2. Hover preko handle-a (cursor se menja)
3. Klikni i drži
4. Povuci da promeniš veličinu
5. Pusti

**Cursor Indikatori:**
- **↔** - Horizontalno (Left/Right)
- **↕** - Vertikalno (Top/Bottom)
- **↖↘** - Dijagonalno (TL/BR)
- **↗↙** - Dijagonalno (TR/BL)

**Constraint:**
- Minimalna veličina: 50x50px
- Maksimalna: Bez limita

### Lock/Unlock (Future Feature)

```python
# Kada implementirano:
element.state.locked = True  # Ne može se pomerati
element.state.locked = False # Može se pomerati
```

---

## 4. Audio Visualizer

### Tipovi Visualizera

#### 1. BARS - Klasični Equalizer

**Idealno za:** Pop, Rock, EDM

**Parametri:**
```
EQ Bands: 16-32 (preporučeno 20)
Smoothness: 0.6-0.7
Rounded Bars: ✓ (elegantnije)
```

**Izgled:**
```
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
```

#### 2. MIRROR_BARS - Simetrično Ogledalo

**Idealno za:** Hip-Hop, Trap, Bass-heavy

**Parametri:**
```
EQ Bands: 24-32
Smoothness: 0.5-0.6 (brža reakcija)
Mirror Gap: 10-30px
```

**Izgled:**
```
█ █ █ █ █ █ █ █
▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀
[   GAP   ]
▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄
█ █ █ █ █ █ █ █
```

#### 3. LINE - Glatka Linija

**Idealno za:** Ambient, Classical, Chill

**Parametri:**
```
EQ Bands: 16-24
Smoothness: 0.8-0.9 (vrlo glatko)
Line Thickness: 2-4px
```

**Izgled:**
```
    ╱╲    ╱╲
   ╱  ╲  ╱  ╲
  ╱    ╲╱    ╲
```

#### 4. CIRCULAR - 360° Radijalni

**Idealno za:** Sve žanrove, Logo prezentacije

**Parametri:**
```
EQ Bands: 32-48 (više = glađe)
Smoothness: 0.7-0.8
```

**Izgled:**
```
      |
   ╱  |  ╲
  ─   ●   ─
   ╲  |  ╱
      |
```

#### 5. RING - Kružni Prsten

**Idealno za:** Techno, House, Trance

**Parametri:**
```
EQ Bands: 32-64
Smoothness: 0.6-0.7
```

**Izgled:**
```
    ╱▓▓▓╲
   │ ▒▒▒ │
   │▒▒●▒▒│
   │ ▒▒▒ │
    ╲▄▄▄╱
```

### Gradients (Boje)

#### Ocean 🌊
```
Colors: (0,119,190) → (0,180,216) → (72,202,228)
Mood: Profesionalno, Smirujuće
Best for: Corporate, Podcasts, Ambient
```

#### Sunset 🌅
```
Colors: (255,94,77) → (251,206,177) → (255,158,128)
Mood: Toplo, Romantično
Best for: Love songs, Indie, Folk
```

#### Fire 🔥
```
Colors: (255,0,0) → (255,165,0) → (255,255,0)
Mood: Energično, Intenzivno
Best for: Rock, Metal, Intense EDM
```

#### Purple 💜
```
Colors: (138,43,226) → (186,85,211) → (221,160,221)
Mood: Elegantno, Luksuzno
Best for: R&B, Soul, Premium content
```

#### Neon ⚡
```
Colors: (0,255,255) → (255,0,255) → (255,255,0)
Mood: Party, Klub
Best for: EDM, House, Dance
```

#### Mint 🍃
```
Colors: (0,255,127) → (127,255,212) → (175,238,238)
Mood: Sveže, Moderno
Best for: Chill, Lo-fi, Study music
```

### Smoothness (Glatkoća)

**Šta radi:**
- Interpolira između frame-ova
- Eliminiše "jumpy" kretanje
- 0.0 = Trenutna reakcija (jumpy)
- 1.0 = Veoma glatko (sporo)

**Preporuke po žanru:**
```
EDM/Dubstep:    0.3 - 0.5  (brza reakcija)
Pop/Rock:       0.6 - 0.7  (balansirano)
Ambient/Chill:  0.8 - 0.9  (vrlo glatko)
Classical:      0.85- 0.95 (najglatakije)
```

**Formula:**
```python
level = prev_level * (1 - smoothness) + current_level * smoothness
```

### EQ Bands (Frekvencijski Opsezi)

**Šta su:**
- Broj frekvencijskih traka
- Više = detaljnije, ali sporije

**Preporuke:**
```
8-12:  Minimalistički, retro look
16-20: Balans (preporučeno)
24-32: Detaljno, profesionalno
40-64: Ekstremno detaljno (sporo)
```

**Performance:**
```
16 bands = ~30 FPS preview
32 bands = ~20 FPS preview
64 bands = ~10 FPS preview
```

---

## 5. Tekst i Stilizovanje

### Dodavanje Teksta

**Korak 1: Dodaj Element**
1. **Text Panel** (desna strana)
2. Klikni **"➕ Add Text"**
3. Tekst se pojavljuje na (100, 100)

**Korak 2: Unesi Sadržaj**
1. **Content** text box
2. Ukucaj željeni tekst
3. Može više linija (Enter)

**Korak 3: Stilizuj**
- **Font:** Arial, Impact, Courier, itd.
- **Size:** 12-200px
- **Bold:** ✓ ili ✗
- **Color:** RGB picker

**Korak 4: Pozicioniraj**
- Drag & drop na mesto
- Resize handle-i za veličinu

### Quick Templates

**Song - Artist**
```
"Song Title - Artist Name"
```

**Artist Name**
```
"Artist Name"
```

**Song Title**
```
"Song Title"
```

### Font Preporuke

**Za YouTube Lyric Videos:**
```
Font: Arial Black ili Impact
Size: 72-96px
Bold: ✓
Color: Bela (255, 255, 255)
```

**Za Subtitle:**
```
Font: Arial
Size: 36-48px
Bold: ✓
Color: Svetlo siva (200, 200, 200)
```

**Za Logo/Branding:**
```
Font: Trebuchet MS ili Georgia
Size: 48-72px
Bold: ✗ ili ✓
Color: Brand color
```

### Pozicioniranje Teksta

**Standard Pozicije (1080p):**
```
Gornji centar:    X=960,  Y=50
Gornji levi:      X=50,   Y=50
Donji centar:     X=960,  Y=1000
Donji levi:       X=50,   Y=1000
Centar ekrana:    X=960,  Y=540
```

---

## 6. Export Video

### Priprema za Export

**Pre exporta proveri:**
- ✓ Audio je učitan
- ✓ Svi elementi su pozicionirani
- ✓ Preview izgleda dobro
- ✓ FFmpeg je instaliran

### Export Proces

**Korak 1: Otvori Export Dialog**
1. **File** → **Export Video** (Ctrl+E)
2. Izaberi output lokaciju
3. Unesi ime fajla (.mp4)

**Korak 2: Podesi Settings**

**Resolution:**
```
1920x1080 (1080p)  - Standard, YouTube
1280x720  (720p)   - Manji fajl
3840x2160 (4K)     - Premium quality
1080x1920 (Vertical) - Instagram/TikTok
```

**Frame Rate (FPS):**
```
24 fps - Filmski look
30 fps - Standard (preporučeno)
60 fps - Super smooth (veliki fajl)
```

**Quality (CRF):**
```
15-17: Visok kvalitet (ogroman fajl)
18-20: Dobar kvalitet (preporučeno)
21-23: Srednji kvalitet
24-28: Niži kvalitet (mali fajl)
```

**Encoding Preset:**
```
ultrafast: Najbrže, najveći fajl
fast:      Brzo, srednji fajl
medium:    Balansirano (preporučeno)
slow:      Sporo, mali fajl
slower:    Najsporije, najmanji fajl
```

**Korak 3: Start Export**
1. Klikni **"Start Export"**
2. Progress bar pokazuje napredak
3. Status log prikazuje detalje
4. Čekaj završetak (može trajati)

### Vreme Renderovanja

**Pesma od 3 minuta (Intel i5-10400):**
```
1080p / 30fps / medium:  ~4-6 min
1080p / 60fps / medium:  ~8-12 min
4K / 30fps / medium:     ~15-20 min
4K / 60fps / slow:       ~30-40 min
```

**Faktori koji utiču:**
- Broj elemenata
- EQ Bands (više = sporije)
- Glow effects (kada implementiran)
- CPU brzina
- Encoding preset

---

## 7. Napredne Tehnike

### Multiple Visualizers

**Zašto:**
- Layered efekat
- Različiti frekvencijski rangovi
- Vizuelna kompleksnost

**Kako:**
```
1. Dodaj 2-3 visualizera
2. Postavi različite tipove
3. Različite boje/gradients
4. Overlap ili odvojeno
```

**Primer Setup:**
```
Background Visualizer:
  Type: BARS
  Position: X=960, Y=700
  Size: 1900x400
  Gradient: Ocean
  Opacity: 50%

Foreground Visualizer:
  Type: CIRCULAR
  Position: X=960, Y=540
  Size: 600x600
  Gradient: Fire
  Opacity: 100%
```

### Z-Index Layering

**Šta je:**
- Redosled prikaza elemenata
- Veći Z = ispred

**Kako:**
```python
element.state.z_index = 0  # Background
element.state.z_index = 1  # Middle
element.state.z_index = 2  # Foreground
```

### Background Images

**Best Practices:**
```
Resolution: Ista kao export (1920x1080)
Format: PNG ili JPG
Size: <5MB (za performance)
```

**Stilovi:**
```
Solid Color: Photoshop, 1920x1080, solid fill
Gradient: Vertical ili radial gradient
Photo: Blur + darken za text visibility
Abstract: Geometric patterns, subtle
```

---

## 8. Troubleshooting

### Audio Problemi

**Problem: Audio se ne učitava**
```
Rešenje:
1. Proveri format (MP3, WAV)
2. Konvertuj u WAV
3. Proveri da fajl nije corrupted
```

**Problem: No sound u preview**
```
Rešenje:
1. Proveri system volume
2. Restartuj aplikaciju
3. Reinstaliraj pygame
```

### Preview Problemi

**Problem: Lag/Stuttering**
```
Rešenje:
1. Smanji EQ Bands (16-20)
2. Disable glow
3. Zatvori druge aplikacije
4. Lower preview FPS
```

**Problem: Black screen**
```
Rešenje:
1. Klikni Play
2. Proveri da su elementi visible
3. Check Z-index order
```

### Export Problemi

**Problem: FFmpeg not found**
```
Rešenje:
Windows: winget install ffmpeg
Linux:   sudo apt install ffmpeg
Mac:     brew install ffmpeg
```

**Problem: Export fails/crashes**
```
Rešenje:
1. Check disk space
2. Try lower resolution
3. Use faster preset
4. Check FFmpeg version
```

**Problem: Video/Audio desync**
```
Rešenje:
1. Use constant FPS
2. Check audio file integrity
3. Try different encoding preset
```

---

## 📞 Dodatna Pomoć

**Dokumentacija:**
- README.md - Opšti vodič
- QUICKSTART.md - Brzi početak
- Ovaj fajl - Detaljan tutorial

**Support:**
- GitHub Issues
- Email support
- Discord (coming soon)

---

**Srećno kreiranje! 🎨🎵**
