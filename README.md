# QLC+ Auto Palette FX Engine

> **IT:** Genera automaticamente centinaia di scene, effetti EFX e chaser da un progetto QLC+ esistente.
> **EN:** Automatically generate hundreds of scenes, EFX effects and chasers from an existing QLC+ project.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![QLC+](https://img.shields.io/badge/QLC%2B-4.x-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.1alpha-yellow)

---

## 🇮🇹 Italiano

### Cos'è

`qlcplus_auto_palette_fxengine.py` è uno script Python che legge un file di progetto **QLC+** (`.qxw`) con fixture già definite e patchate, carica automaticamente le definizioni fixture (`.qxf`) dalla libreria di QLC+, e genera una **palette completa** di funzioni organizzate in cartelle:

| Tipo | Quantità tipica | Descrizione |
|------|----------------|-------------|
| **Scene statiche** | 100–500+ | Dimmer, colori RGB/CMY/RGBW, color wheel, gobo, posizioni Pan/Tilt, combo |
| **EFX** | 50–300+ | Effetti di movimento per moving head (cerchio, 8, lissajous, ecc.) |
| **Chaser** | 150–500+ | Sequenze: arcobaleno, stomp, police, chase, knight rider, chaser globali… |

Il file `.qxw` originale non viene mai modificato: lo script produce sempre un nuovo file `_palette.qxw`.

### Requisiti

- **Python 3.8+** (nessuna dipendenza esterna, solo stdlib)
- **QLC+ 4.x** installato (per aprire il file generato e per la libreria fixture)
- Un file `.qxw` con fixture già aggiunte e patchate

### Installazione

```bash
git clone https://github.com/marcocoldagelli/qlcplus_auto_palette_fxengine.git
cd qlcplus_auto_palette_fxengine
python3 qlcplus_auto_palette_fxengine.py --help
```

### Avvio rapido

```bash
# Genera la palette in italiano (default)
python3 qlcplus_auto_palette_fxengine.py mio_show.qxw

# Genera la palette in inglese
python3 qlcplus_auto_palette_fxengine.py mio_show.qxw --lang en
```

---

## 🇬🇧 English

### What is it

`qlcplus_auto_palette_fxengine.py` is a Python script that reads a **QLC+** project file (`.qxw`) with fixtures already defined and patched, automatically loads the fixture definitions (`.qxf`) from the QLC+ library, and generates a **complete palette** of functions organized in folders:

| Type | Typical count | Description |
|------|--------------|-------------|
| **Static scenes** | 100–500+ | Dimmer, RGB/CMY/RGBW colors, color wheel, gobos, Pan/Tilt positions, combos |
| **EFX** | 50–300+ | Movement effects for moving heads (circle, figure-8, lissajous, etc.) |
| **Chasers** | 150–500+ | Effect sequences: rainbow, stomp, police, chase, knight rider, global chasers… |

The original `.qxw` file is never modified: the script always produces a new `_palette.qxw` file.

### Requirements

- **Python 3.8+** (no external dependencies, pure stdlib)
- **QLC+ 4.x** installed (to open the generated file and for the fixture library)
- A `.qxw` file with fixtures already added and patched

### Installation

```bash
git clone https://github.com/marcocoldagelli/qlcplus_auto_palette_fxengine.git
cd qlcplus_auto_palette_fxengine
python3 qlcplus_auto_palette_fxengine.py --help
```

### Quick start

```bash
# Generate palette in Italian (default)
python3 qlcplus_auto_palette_fxengine.py my_show.qxw

# Generate palette in English
python3 qlcplus_auto_palette_fxengine.py my_show.qxw --lang en
```

---

## Opzioni / Options

```
python3 qlcplus_auto_palette_fxengine.py <file.qxw> [OPZIONI / OPTIONS]
```

| Opzione / Option | Valore / Value | Default | IT | EN |
|---|---|---|---|---|
| `--output` | `FILE.qxw` | `input_palette.qxw` | File di output | Output file path |
| `--fixture-dir` | `PATH` | — | Dir aggiuntiva `.qxf` | Additional `.qxf` directory |
| `--fade-in` | `MS` | `0` | FadeIn scene (ms) | Scene fade in (ms) |
| `--fade-out` | `MS` | `2000` | FadeOut scene (ms) | Scene fade out (ms) |
| `--lang` | `it` \| `en` | `it` | Lingua dei nomi generati | Language of generated names |
| `--overwrite` | flag | off | Sovrascrive funzioni esistenti | Overwrite existing functions |
| `--skip-groups` | flag | off | Salta gruppi | Skip group scenes/EFX/chasers |
| `--skip-combos` | flag | off | Salta combo | Skip combo scenes |
| `--skip-efx` | flag | off | Salta EFX | Skip movement EFX |
| `--skip-chasers` | flag | off | Salta chaser | Skip chasers |
| `--min-cap-scenes` | `N` | `2` | Min capability per scene | Min capabilities for scenes |

---

## Palette generate / Generated palette

### IT: Scene GLOBAL / EN: GLOBAL scenes

| IT | EN |
|---|---|
| `GLOBAL » Dimmer Zero/10%/25%/50%/75%/Full` | Same — sets all dimmers |
| `GLOBAL » Shutter Aperto / Chiuso` | `GLOBAL » Shutter Open / Closed` |
| `GLOBAL » All Strobe Slow / Med / Fast` | Same |
| `GLOBAL » All Moving Center` | Same |
| `GLOBAL » Rosso / Bianco / Blu / …` (35 colori) | `GLOBAL » Red / White / Blue / …` (35 colors) |

### IT: Scene per fixture / EN: Per-fixture scenes

- **Dimmer:** 6 livelli + shutter + strobe / 6 levels + shutter + strobe
- **RGB:** 35 colori + varianti RGBW/RGBA/RGBAW / 35 colors + RGBW/RGBA/RGBAW variants
- **CMY:** 21 colori / 21 colors
- **Color Wheel, Gobo, Prism, Zoom, Iris, Focus, Frost**
- **Pan/Tilt:** 29 posizioni predefinite / 29 predefined positions
- **Combo:** Stage Ready, Blackout Totale/Full Blackout, Full Show

### EFX di movimento / Movement EFX

19 forme × 3 taglie × 5 velocità + varianti = 50–100 EFX per moving head.
19 shapes × 3 sizes × 5 speeds + variants = 50–100 EFX per moving head.

EFX di gruppo con 6 modalità di fase: **Sync, Fan, Mirror, Opposite/Opposto, Wave, Pairs/Coppie**.
Group EFX with 6 phase offset modes: **Sync, Fan, Mirror, Opposite, Wave, Pairs**.

### IT: Chaser / EN: Chasers

**Singola fixture / Single fixture:**
- Dimmer: Stomp, Heartbeat, Breathing, Double/Triple/Quad Flash, Lightning, Flicker, Ramp Up Down
- RGB: Arcobaleno/Rainbow, Pastelli/Pastels, Colori Caldi/Warm Colors, Colori Freddi/Cool Colors, Police, Ambulanza/Ambulance, Tecno/Techno, Warm-Cool, 12 Bicolori, 6 Tricolori
- CMY: Arcobaleno/Rainbow, Caldi/Warm, Freddi/Cool
- Moving: Stage Sweep, Audience Scan, Position Chase, Pan/Tilt Oscillazione/Oscillation

**Gruppo / Group:**
- Sequenziale/Sequential Chase, PingPong, Knight Rider, Pairs, ODD/EVEN Flash
- Stomp Gruppo/Group Stomp, Lightning, Double/Triple Flash
- Arcobaleno/Rainbow, Pastelli/Pastels, Bicolori/Bicolors, Tricolori/Tricolors, Police, Techno, Color Ripple
- **NOVITÀ v1.1 / NEW v1.1:** Stomp Colore/Color Stomp, Onda Colore/Color Wave, Alba/Sunrise, Tramonto/Sundown, Split Colori/Split Colors
- Stage PT Chase, Corner Chase, Waterfall

**GLOBAL (tutte le fixture / all fixtures) — NOVITÀ v1.1 / NEW v1.1:**
- Arcobaleno Globale/Global Rainbow (+ Smooth), Stomp Globale/Global Stomp
- Polizia Globale/Global Police, Alba Globale/Global Sunrise
- Battito Globale/Global Heartbeat, Impulso Globale/Global Pulse
- Strobo Globale/Global Strobe, Club Colors/Discoteca Globale

---

## IT: Struttura cartelle / EN: Folder structure

```
Auto Palette/
├── GLOBAL/                          ← scene globali / global scenes
├── <Nome Fixture / Fixture Name>/   ← scene per fixture
├── GRUPPI/ o GROUPS/
│   └── <Modello (Modo)>/            ← scene di gruppo / group scenes
├── EFX/
│   ├── <Nome Fixture>/              ← EFX per fixture
│   └── GRUPPI/GROUPS/
│       └── <Modello (Modo)>/        ← EFX di gruppo / group EFX
└── CHASER/
    ├── GLOBAL/                      ← chaser globali / global chasers  ← NUOVO v1.1
    ├── <Nome Fixture>/              ← chaser per fixture
    └── GRUPPI/GROUPS/
        └── <Modello (Modo)>/        ← chaser di gruppo / group chasers
```

---

## IT: Raggruppamento fixture / EN: Fixture grouping

IT: Fixture raggruppate per `(Modello, Modo, Canali)`: fixture con stesso modello ma configurazione diversa (es. RGB 3ch puro vs Dimmer+RGB 4ch) rimangono in gruppi separati.

EN: Fixtures grouped by `(Model, Mode, Channels)`: fixtures with the same model name but different configurations (e.g. pure RGB 3ch vs Dimmer+RGB 4ch / IRGB) are kept in separate groups.

---

## IT: Percorsi libreria fixture / EN: Fixture library paths

| Sistema / System | Percorso / Path |
|---------|------|
| Linux | `/usr/share/qlcplus/fixtures` |
| macOS | `/Applications/QLC+.app/Contents/Resources/fixtures` |
| Windows | `C:\QLC+\fixtures` · `C:\Program Files\QLC+\fixtures` |
| Utente / User | `~/QLC+/fixtures` · `~/.qlcplus/fixtures` |

---

## IT: Fixture Generic (fallback) / EN: Generic fixtures (fallback)

| Modello / Model | IT: Canali inferiti / EN: Inferred channels |
|-------|------------------|
| Generic RGB (3ch) | R, G, B |
| Generic RGB (4ch / IRGB) | Dimmer, R, G, B |
| Generic RGBW | R, G, B, W |
| Generic RGBA | R, G, B, A |
| Generic RGBAW | R, G, B, A, W |
| Generic CMY | C, M, Y |
| Smoke / Haze / Fog | Effect |

---

## IT: Personalizzazione / EN: Customization

```python
# Aggiungere un colore RGB / Add an RGB color
RGB_PALETTE = [
    ...
    ("My Color", 100, 200, 150),  # name, R, G, B
]

# Aggiungere una posizione Pan/Tilt / Add a Pan/Tilt position
MOVING_POSITIONS = [
    ...
    ("My Position", 90, 110),  # name, pan (0-255), tilt (0-255)
]
```

---

## Autore / Author

**Marco Coldagelli** — v1.1alpha

---

## Licenza / License

MIT License — libero uso, modifica e distribuzione con attribuzione.
MIT License — free to use, modify and distribute with attribution.
