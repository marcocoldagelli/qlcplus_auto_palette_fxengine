# qlcplus_auto_palette_fxengine
Stop building QLC+ scenes by hand. One command generates your entire palette — colors, positions, movement effects and chase sequences — for every fixture in your show.

# QLC+ Auto Palette FX Engine

> **Genera automaticamente centinaia di scene, effetti EFX e Chaser a partire da un progetto QLC+ esistente.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![QLC+](https://img.shields.io/badge/QLC%2B-4.x-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.0alpha-yellow)

---

## Cos'è

`qlcplus_auto_palette_fxengine.py` è uno script Python che legge un file di progetto **QLC+** (`.qxw`) con le fixture già definite e patchate, carica automaticamente le definizioni fixture (`.qxf`) dalla libreria di QLC+, e genera una **palette completa** di funzioni organizzate in cartelle:

| Tipo | Quantità tipica | Descrizione |
|------|----------------|-------------|
| **Scene statiche** | 100–500+ | Dimmer, colori RGB/CMY/RGBW, color wheel, gobo, posizioni Pan/Tilt, combo |
| **EFX** | 50–300+ | Effetti di movimento per moving head (cerchio, figura 8, lissajous, ecc.) |
| **Chaser** | 100–400+ | Sequenze di effetti: arcobaleno, stomp, police, chase, knight rider, ecc. |

Il file originale `.qxw` non viene mai modificato: lo script produce sempre un nuovo file `_palette.qxw`.

---

## Requisiti

- **Python 3.8+** (nessuna dipendenza esterna, solo stdlib)
- **QLC+ 4.x** installato (per aprire il file generato e per la libreria fixture)
- Un file `.qxw` con le fixture già aggiunte e patchate

---

## Installazione

```bash
# Clona il repository
git clone https://github.com/tuo-utente/qlcplus-auto-palette.git
cd qlcplus-auto-palette

# Nessuna dipendenza da installare — Python puro
python3 qlcplus_auto_palette_fxengine.py --help
```

---

## Uso rapido

```bash
# Genera la palette con le opzioni di default
python3 qlcplus_auto_palette_fxengine.py mio_show.qxw
```

Produce `mio_show_palette.qxw` nella stessa directory. Aprirlo con QLC+ e la cartella **Auto Palette/** sarà disponibile nel pannello Funzioni.

---

## Opzioni

```
python3 qlcplus_auto_palette_fxengine.py <file.qxw> [OPZIONI]

Opzioni:
  --output FILE         File .qxw di output (default: input_palette.qxw)
  --fixture-dir DIR     Directory aggiuntiva con file .qxf personalizzati
  --fade-in MS          FadeIn in ms per tutte le scene (default: 0)
  --fade-out MS         FadeOut in ms per tutte le scene (default: 2000)
  --overwrite           Sovrascrive funzioni già presenti con lo stesso nome
  --skip-groups         Salta scene/EFX/Chaser di gruppo
  --skip-combos         Salta le scene combo (Stage Ready, Full Show, ecc.)
  --skip-efx            Salta la generazione degli EFX di movimento
  --skip-chasers        Salta la generazione dei Chaser
  --min-cap-scenes N    Min capability per generare scene da color wheel/gobo (default: 2)
```

### Esempi

```bash
# Fixture in percorso non standard + output personalizzato
python3 qlcplus_auto_palette_fxengine.py show.qxw \
        --fixture-dir /home/user/fixture_custom \
        --output show_completo.qxw \
        --fade-out 1500

# Solo scene statiche, niente EFX né Chaser (più veloce)
python3 qlcplus_auto_palette_fxengine.py show.qxw --skip-efx --skip-chasers

# Aggiornamento dopo aver modificato il progetto
python3 qlcplus_auto_palette_fxengine.py show_palette.qxw --overwrite
```

---

## Palette generate

### Scene GLOBAL
Scene che agiscono su tutte le fixture contemporaneamente:
- `GLOBAL » Dimmer Zero/10%/25%/50%/75%/Full`
- `GLOBAL » All Shutter Aperto / Chiuso`
- `GLOBAL » All Strobe Slow / Med / Fast`
- `GLOBAL » All Moving Center`

### Per ogni fixture
Le scene per singola fixture coprono:

- **Dimmer/Intensity** — 6 livelli + shutter open/close + strobe slow/med/fast
- **RGB** — 35 colori (primari, secondari, terziari, saturi, teatrali, pastelli) con varianti RGBW/RGBA/RGBAW
- **CMY** — 21 colori
- **Color Wheel** — una scena per ogni posizione dal file `.qxf`
- **Gobo** — una scena per ogni gobo + rotation CW/CCW/Stop
- **Prism** — On/Off/Rot + tutte le capability
- **Zoom / Iris / Focus / Frost** — presets Stretto/Medio/Largo e Near/Mid/Far
- **Pan/Tilt** — 29 posizioni predefinite (DS/US/Side/Audience/Balcony/Floor…)
- **Speed / Effect / Macro** — una scena per ogni capability del canale
- **Combo** — Stage Ready, Blackout Totale, Full Show, Rosso/Bianco/Blu Puro

### EFX di movimento
Per ogni fixture con Pan e Tilt, in tutte le combinazioni di forma × taglia × velocità:

| Forme disponibili | Taglie | Velocità |
|---|---|---|
| Circle, Eight, Diamond, Square, SquareChoppy, Leaf, Line (Pan Sweep / Tilt Swing), Lissajous (2:1, 3:2, 1:3, 3:1, 4:3, 5:4) | Piccolo (60), Medio (127), Grande (200) | Molto Lento (20s) → Velocissimo (1.5s) |

### EFX di gruppo
Per gruppi di 2+ fixture, con modalità di sfasamento: **Sync, Fan, Mirror, Opposto, Wave, Coppie**.

### Chaser
Oltre 50 tipologie di sequenze per singola fixture e per gruppo: stomp, breathing, heartbeat, lightning, flicker, arcobaleno, police, ambulanza, tecno, chase sequenziale, knight rider, ODD/EVEN, ripple, sweep palco, audience scan e molti altri.

---

## Struttura cartelle in QLC+

```
Auto Palette/
├── GLOBAL/                          ← scene su tutte le fixture
├── <Nome Fixture>/                  ← scene per singola fixture
├── GRUPPI/
│   └── <Modello (Mode)>/            ← scene di gruppo
├── EFX/
│   ├── <Nome Fixture>/              ← EFX per singola fixture
│   └── GRUPPI/
│       └── <Modello (Mode)>/        ← EFX di gruppo
└── CHASER/
    ├── <Nome Fixture>/              ← Chaser per singola fixture
    └── GRUPPI/
        └── <Modello (Mode)>/        ← Chaser di gruppo
```

---

## Raggruppamento fixture

Le fixture vengono raggruppate per `(Model, Mode, Channels)`. Questo garantisce che fixture con lo stesso nome di modello ma configurazioni diverse non vengano mai mescolate — ad esempio un **Generic RGB a 3 canali** (RGB puro) e uno a **4 canali** (Dimmer + RGB / IRGB) finiscono in gruppi separati con scene e Chaser corretti.

---

## Percorsi fixture cercati automaticamente

Lo script trova la libreria `.qxf` nei percorsi standard di QLC+:

| Sistema | Percorso |
|---------|---------|
| Linux | `/usr/share/qlcplus/fixtures` |
| macOS | `/Applications/QLC+.app/Contents/Resources/fixtures` |
| Windows | `C:\QLC+\fixtures` · `C:\Program Files\QLC+\fixtures` |
| Utente | `~/QLC+/fixtures` · `~/.qlcplus/fixtures` |

Per percorsi non standard usare `--fixture-dir`.

---

## Fixture Generic (fallback automatico)

Se il file `.qxf` non viene trovato, lo script inferisce i canali dal nome del modello:

| Modello | Canali inferiti |
|---------|----------------|
| Generic RGB (3ch) | R, G, B |
| Generic RGB (4ch / IRGB) | Dimmer, R, G, B |
| Generic RGBW | R, G, B, W |
| Generic RGBA | R, G, B, A |
| Generic RGBAW | R, G, B, A, W |
| Generic CMY | C, M, Y |
| Smoke / Haze / Fog | Effect |

---

## Personalizzazione

Le palette sono definite come costanti Python facilmente modificabili:

```python
# Aggiungere un colore RGB
RGB_PALETTE = [
    ...
    ("Mio Colore", 100, 200, 150),  # nome, R, G, B
]

# Aggiungere una posizione Pan/Tilt
MOVING_POSITIONS = [
    ...
    ("Mia Posizione", 90, 110),  # nome, pan_byte (0-255), tilt_byte (0-255)
]

# Aggiungere una forma EFX
EFX_SHAPES = [
    ...
    ("Mia Forma", "Circle", 30, {}),  # nome, algoritmo, rotazione_gradi, extra_kwargs
]
```

---

## Log di esecuzione

```
════════════════════════════════════════════════════════════════
  QLC+ Auto Palette FX Engine v1.0alpha by Marco Coldagelli
════════════════════════════════════════════════════════════════
  Input : mio_show.qxw
  Output: mio_show_palette.qxw

  Fixture patchate: 6
    [  0] Par LED 1         Generic RGB (3ch Mode)  U1@1
    [  1] Par LED 2         Generic RGB (3ch Mode)  U1@4
    [  2] Moving Head 1     Shehds Beam 200RGO      U1@10
    ...

  ── Passata 1: Scene statiche ──
    + [   1] GLOBAL » Dimmer Zero
    + [   2] GLOBAL » Dimmer Full
    + [  42] Par LED 1 » Rosso
    ...

  ── Passata 2: EFX di movimento ──
    ~ [  87] Moving Head 1 » EFX Circle Medio Lento
    ...

  ── Passata 3: Chaser ──
    ≫ [ 312] Par LED 1 » CHR Arcobaleno Medio
    ...

────────────────────────────────────────────────────────────────
  Scene    aggiunte :  420  (saltate: 0)
  EFX      aggiunti :   96  (saltati: 0)
  Chaser   aggiunti :  188  (saltati: 0)
  Output            : mio_show_palette.qxw
════════════════════════════════════════════════════════════════
```

---

## Autore

**Marco Coldagelli** — v1.0alpha

---

## Licenza

MIT License — libero di usare, modificare e distribuire con attribuzione.
