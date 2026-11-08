# QLC+ Auto Palette FX Engine

> **IT:** Genera automaticamente centinaia di scene, effetti EFX e chaser da un progetto QLC+ esistente.
> **EN:** Automatically generate hundreds of scenes, EFX effects and chasers from an existing QLC+ project.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![QLC+](https://img.shields.io/badge/QLC%2B-4.x-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.4-brightgreen)

---

## 🇮🇹 Italiano

### Cos'è

`qlcplus_auto_palette_fxengine.py` è uno script Python che legge un file di progetto **QLC+** (`.qxw`) con fixture già definite e patchate, carica automaticamente le definizioni fixture (`.qxf`) dalla libreria di QLC+, e genera una **palette completa** di funzioni organizzate in cartelle:

| Tipo | Quantità tipica | Descrizione |
|------|----------------|-------------|
| **Scene statiche** | 100–1500+ | Dimmer, shutter/strobo, colori RGB/CMY/RGBW, color wheel, gobo, posizioni Pan/Tilt, combo |
| **EFX** | 100–5000+ | Effetti di movimento per moving head (cerchio, 8, lissajous, ecc.) |
| **Chaser** | 200–2500+ | Sequenze: arcobaleno, stomp, police, chase, knight rider, chaser globali… |

Le quantità dipendono dal numero di fixture e dal profilo scelto (`compatto` o `completo`, vedi sotto).

Il file `.qxw` originale non viene mai modificato: lo script produce sempre un nuovo file `_palette.qxw`.

### Novità della v1.4

- **Riconoscimento dei canali** basato sulla tabella ufficiale dei preset di QLC+ 4.14: Master Dimmer, canali fine, colori, zoom, focus e iris vengono riconosciuti anche sulle fixture moderne definite solo con i preset.
- **Shutter, strobo e prisma** letti dai preset delle capability (`ShutterOpen`, `ShutterClose`, `Strobe…`, `PrismEffectOn/Off`); i nomi vengono cercati solo come parole intere.
- **Dimmer generici** (`Generic / Generic`) trattati come dimmer su tutti i canali, non più scambiati per Generic RGBW.
- **Chaser** con dissolvenze per passo: i chaser veloci non si impastano più con il fade-out delle scene.
- **EFX** con ampiezze entro il limite di QLC+ (127): niente più movimenti schiacciati ai fine corsa.
- **Profilo `compatto`** (predefinito) e **`completo`**: il compatto evita i doppioni tra funzioni per singola fixture e funzioni di gruppo.
- **Ricerca dei `.qxf`** anche nella cartella del progetto e nella cartella utente di QLC+ su macOS.

Dettagli in [RELEASE_NOTES_bilingual.md](RELEASE_NOTES_bilingual.md).

### Requisiti

- **Python 3.8+** (nessuna dipendenza esterna, solo stdlib)
- **QLC+ 4.x** installato (per aprire il file generato e per la libreria fixture) — verificato con **QLC+ 4.14.4**
- Un file `.qxw` con fixture già aggiunte e patchate

### Installazione

```bash
git clone https://github.com/marcocoldagelli/qlcplus_auto_palette_fxengine.git
cd qlcplus_auto_palette_fxengine
python3 qlcplus_auto_palette_fxengine.py --help
```

### Avvio rapido

```bash
# Genera la palette in italiano (default, profilo compatto)
python3 qlcplus_auto_palette_fxengine.py mio_show.qxw

# Tutte le varianti, come nella v1.3
python3 qlcplus_auto_palette_fxengine.py mio_show.qxw --profilo completo

# Genera la palette in inglese
python3 qlcplus_auto_palette_fxengine.py mio_show.qxw --lang en
```

---

## 🇬🇧 English

### What is it

`qlcplus_auto_palette_fxengine.py` is a Python script that reads a **QLC+** project file (`.qxw`) with fixtures already defined and patched, automatically loads the fixture definitions (`.qxf`) from the QLC+ library, and generates a **complete palette** of functions organized in folders:

| Type | Typical count | Description |
|------|--------------|-------------|
| **Static scenes** | 100–1500+ | Dimmer, shutter/strobe, RGB/CMY/RGBW colors, color wheel, gobos, Pan/Tilt positions, combos |
| **EFX** | 100–5000+ | Movement effects for moving heads (circle, figure-8, lissajous, etc.) |
| **Chasers** | 200–2500+ | Effect sequences: rainbow, stomp, police, chase, knight rider, global chasers… |

Counts depend on the number of fixtures and on the selected profile (`compact` or `full`, see below).

The original `.qxw` file is never modified: the script always produces a new `_palette.qxw` file.

### What's new in v1.4

- **Channel detection** based on the official QLC+ 4.14 preset table: Master Dimmer, fine channels, colours, zoom, focus and iris are recognised even on modern preset-only fixtures.
- **Shutter, strobe and prism** read from capability presets (`ShutterOpen`, `ShutterClose`, `Strobe…`, `PrismEffectOn/Off`); names are matched as whole words only.
- **Generic dimmers** (`Generic / Generic`) handled as dimmers on every channel, no longer mistaken for Generic RGBW.
- **Chasers** use per-step fades: fast chasers no longer smear with the scenes' fade-out.
- **EFX** amplitudes kept within the QLC+ limit (127): no more movements clipped at the end stops.
- **`compact` profile** (default) and **`full`**: compact avoids duplicates between single-fixture and group functions.
- **`.qxf` search** also in the project folder and in the QLC+ user folder on macOS.

Details in [RELEASE_NOTES_bilingual.md](RELEASE_NOTES_bilingual.md).

### Requirements

- **Python 3.8+** (no external dependencies, pure stdlib)
- **QLC+ 4.x** installed (to open the generated file and for the fixture library) — verified with **QLC+ 4.14.4**
- A `.qxw` file with fixtures already added and patched

### Installation

```bash
git clone https://github.com/marcocoldagelli/qlcplus_auto_palette_fxengine.git
cd qlcplus_auto_palette_fxengine
python3 qlcplus_auto_palette_fxengine.py --help
```

### Quick start

```bash
# Generate palette in Italian (default, compact profile)
python3 qlcplus_auto_palette_fxengine.py my_show.qxw

# Every variant, as in v1.3
python3 qlcplus_auto_palette_fxengine.py my_show.qxw --profile full

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
| `--fade-out` | `MS` | `2000` | FadeOut scene (ms) — non influisce più sui chaser | Scene fade out (ms) — no longer affects chasers |
| `--profilo` / `--profile` | `compatto`\|`completo` (`compact`\|`full`) | `compatto` | Compatto: niente doppioni con i gruppi. Completo: tutte le varianti | Compact: no duplicates with groups. Full: every variant |
| `--lang` | `it` \| `en` | `it` | Lingua dei nomi generati | Language of generated names |
| `--overwrite` | flag | off | Sovrascrive funzioni esistenti | Overwrite existing functions |
| `--skip-groups` | flag | off | Salta gruppi | Skip group scenes/EFX/chasers |
| `--skip-combos` | flag | off | Salta combo | Skip combo scenes |
| `--skip-efx` | flag | off | Salta EFX | Skip movement EFX |
| `--skip-chasers` | flag | off | Salta chaser | Skip chasers |
| `--min-cap-scenes` | `N` | `2` | Min capability per scene | Min capabilities for scenes |

### Profili / Profiles

| | `compatto` / `compact` (default) | `completo` / `full` |
|---|---|---|
| **IT** | Scene per tutte le fixture. EFX e chaser per singola fixture solo per le fixture che non fanno parte di un gruppo (per modello o FixtureGroup). Gruppo per modello saltato se identico a un FixtureGroup. EFX di gruppo solo in taglia Media. | Tutto, come nella v1.3 (con le correzioni della v1.4). |
| **EN** | Scenes for every fixture. Single-fixture EFX and chasers only for fixtures not in a group (per model or FixtureGroup). Per-model group skipped when identical to a FixtureGroup. Group EFX in Medium size only. | Everything, as in v1.3 (with the v1.4 fixes). |

---

## Palette generate / Generated palette

### IT: Scene GLOBAL / EN: GLOBAL scenes

| IT | EN |
|---|---|
| `GLOBAL » Dimmer Zero/10%/25%/50%/75%/Full` | Same — sets all dimmers |
| `GLOBAL » All Shutter Aperto / Chiuso` | `GLOBAL » All Shutter Open / Closed` |
| `GLOBAL » All Strobe Slow / Med / Fast` | Same |
| `GLOBAL » All Moving Center` | Same |
| `GLOBAL » Rosso / Bianco / Blu / …` (35 colori) | `GLOBAL » Red / White / Blue / …` (35 colors) |

### IT: Scene per fixture / EN: Per-fixture scenes

- **Dimmer:** 6 livelli / 6 levels
- **Shutter/Strobo / Shutter/Strobe:** Aperto/Chiuso + Strobe Slow/Med/Fast (anche su fixture senza dimmer / also on fixtures without dimmer)
- **RGB:** 35 colori + varianti RGBW/RGBA/RGBAW / 35 colors + RGBW/RGBA/RGBAW variants
- **CMY:** 21 colori / 21 colors
- **Color Wheel, Gobo, Prism, Zoom, Iris, Focus, Frost**
- **Pan/Tilt:** 29 posizioni predefinite (canali fine a 0) / 29 predefined positions (fine channels at 0)
- **Combo:** Stage Ready, Blackout Totale/Full Blackout, Full Show

### EFX di movimento / Movement EFX

19 forme × 3 taglie (Piccolo 30 / Medio 70 / Grande 127) × velocità variabili + varianti.
19 shapes × 3 sizes (Small 30 / Medium 70 / Large 127) × variable speeds + variants.

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
- Stomp Colore/Color Stomp, Onda Colore/Color Wave, Alba/Sunrise, Tramonto/Sundown, Split Colori/Split Colors
- Stage PT Chase, Corner Chase, Waterfall

**GLOBAL (tutte le fixture / all fixtures):**
- Arcobaleno Globale/Global Rainbow (+ Smooth), Stomp Globale/Global Stomp
- Polizia Globale/Global Police, Alba Globale/Global Sunrise
- Battito Globale/Global Heartbeat, Impulso Globale/Global Pulse
- Strobo Globale/Global Strobe, Club Colors/Discoteca Globale

**QLC-GRUPPI:**

IT: Per ogni `FixtureGroup` definito manualmente nel progetto QLC+, vengono generati scene, EFX e chaser dedicati. Solo le capabilities comuni a **tutte** le fixture del gruppo vengono utilizzate (intersezione).

EN: For each `FixtureGroup` manually defined in the QLC+ project, dedicated scenes, EFX and chasers are generated. Only capabilities shared by **all** fixtures in the group are used (intersection).

IT: Dalla v1.4 tutti i chaser usano dissolvenze per passo (`PerStep`): il ritmo resta quello dei passi anche con `--fade-out` alto.
EN: Since v1.4 every chaser uses per-step fades (`PerStep`): the rhythm follows the steps even with a high `--fade-out`.

---

## IT: Struttura cartelle / EN: Folder structure

```
Auto Palette/
├── GLOBAL/                          ← scene globali / global scenes
├── <Nome Fixture / Fixture Name>/   ← scene per fixture
├── GRUPPI/                          ← scene per-modello / per-model scenes
│   └── <Modello (Modo)>/
├── QLC-GRUPPI/                      ← scene gruppi QLC+
│   └── <ID - Nome Gruppo QLC+>/
├── EFX/
│   ├── <Nome Fixture>/              ← EFX per fixture (compatto: solo fixture fuori dai gruppi)
│   ├── GRUPPI/
│   │   └── <Modello (Modo)>/        ← EFX di gruppo per-modello
│   └── QLC-GRUPPI/                  ← EFX gruppi QLC+
│       └── <ID - Nome Gruppo QLC+>/
└── CHASER/
    ├── GLOBAL/                      ← chaser globali / global chasers
    ├── <Nome Fixture>/              ← chaser per fixture (compatto: solo fixture fuori dai gruppi)
    ├── GRUPPI/
    │   └── <Modello (Modo)>/        ← chaser per-modello / per-model chasers
    └── QLC-GRUPPI/                  ← chaser gruppi QLC+
        └── <ID - Nome Gruppo QLC+>/
```

---

## IT: Raggruppamento fixture / EN: Fixture grouping

IT: Fixture raggruppate per `(Modello, Modo, Canali)`: fixture con stesso modello ma configurazione diversa (es. RGB 3ch puro vs Dimmer+RGB 4ch) rimangono in gruppi separati. Lo script legge anche i `FixtureGroup` definiti nel progetto (cartelle `QLC-GRUPPI/`). Con il profilo compatto, un gruppo per modello che contiene esattamente le stesse fixture di un `FixtureGroup` non viene duplicato.

EN: Fixtures grouped by `(Model, Mode, Channels)`: fixtures with the same model name but different configurations (e.g. pure RGB 3ch vs Dimmer+RGB 4ch / IRGB) are kept in separate groups. The script also reads `FixtureGroup` entries defined in the project (`QLC-GRUPPI/` folders). With the compact profile, a per-model group containing exactly the same fixtures as a `FixtureGroup` is not duplicated.

---

## IT: Percorsi libreria fixture / EN: Fixture library paths

| Sistema / System | Percorso / Path |
|---------|------|
| Progetto / Project | cartella del file `.qxw` / folder of the `.qxw` file (v1.4) |
| Linux | `/usr/share/qlcplus/fixtures` · `/usr/local/share/qlcplus/fixtures` |
| macOS | `/Applications/QLC+.app/Contents/Resources/fixtures` |
| Windows | `C:\QLC+\fixtures` · `C:\Program Files\QLC+\fixtures` |
| Utente / User | `~/QLC+/fixtures` · `~/QLC+/Fixtures` · `~/.qlcplus/fixtures` · `~/Library/Application Support/QLC+/fixtures` (macOS, v1.4) |

---

## IT: Fixture Generic (fallback) / EN: Generic fixtures (fallback)

| Modello / Model | IT: Canali inferiti / EN: Inferred channels |
|-------|------------------|
| Generic (dimmer QLC+, 1…N canali) / Generic (QLC+ dimmer, 1…N channels) | Dimmer su ogni canale / Dimmer on every channel (v1.4) |
| Generic RGB (3ch) | R, G, B |
| Generic RGB (4ch / IRGB) | Dimmer, R, G, B |
| Generic RGBW | R, G, B, W |
| Generic RGBA | R, G, B, A |
| Generic RGBAW | R, G, B, A, W |
| Generic CMY | C, M, Y |
| Smoke / Haze / Fog | Effect |

---

## IT: Risoluzione problemi / EN: Troubleshooting

| IT: Problema / EN: Issue | IT: Causa / EN: Cause | IT: Soluzione / EN: Solution |
|---|---|---|
| Nessuna fixture trovata / No fixtures found | File .qxw non valido o privo di fixture patchate / Invalid .qxw or no patched fixtures | Verificare le fixture nel tab Fixture / Check fixtures in the Fixture tab |
| Definizione non trovata / Definition not found | File .qxf mancante nella libreria / Missing .qxf in library | Copiare il `.qxf` nella cartella del progetto o usare `--fixture-dir` / Copy the `.qxf` next to the project or use `--fixture-dir` |
| Nessun EFX generato / No EFX generated | Canali Pan/Tilt non rilevati nel .qxf / Pan/Tilt not detected in .qxf | Verificare `Group=Pan/Tilt` o i preset `PositionPan/PositionTilt` nel .qxf / Check `Group=Pan/Tilt` or `PositionPan/PositionTilt` presets in the .qxf |
| Pochi EFX/chaser per singola fixture / Few single-fixture EFX/chasers | Profilo compatto: la fixture fa parte di un gruppo / Compact profile: the fixture belongs to a group | Usare le funzioni di gruppo oppure `--profilo completo` / Use group functions or `--profile full` |
| ID duplicati nel file .qxw / Duplicate IDs | File già processato / Already-processed file | Usare `--overwrite` |
| Chaser vuoti / Empty chasers | Canali RGB assenti per quella fixture / Missing RGB channels | Verificare i canali RGB della fixture / Check fixture RGB channels |
| Gruppo QLC+ ignorato / QLC+ group ignored | Fixture IDs non patchate nel progetto / Fixture IDs not patched | Verificare che tutte le fixture del gruppo siano patchate / Check all group fixtures are patched |
| **Errori grossolani nelle scene: colori sbagliati, canali invertiti, capabilities fuori posto / Gross errors in scenes: wrong colors, inverted channels, misplaced capabilities** | **File .qxf non rilevato in libreria — lo script ha usato il fallback Generic inferendo i canali dal nome del modello / .qxf not found in library — script fell back to Generic mode, inferring channels from model name** | **Verificare che il .qxf sia presente nella libreria o nella cartella del progetto e che il nome modello nel .qxw corrisponda esattamente al campo `<Model>` nel .qxf. Usare `--fixture-dir` se necessario. Il log segnala `[WARN] definizione non trovata` quando scatta il fallback / Check that the .qxf is in the library or next to the project and the model name in the .qxw matches exactly the `<Model>` field in the .qxf. Use `--fixture-dir` if needed. The log shows `[WARN] definition not found` when fallback is triggered** |

> **IT:** Se le scene presentano errori grossolani di mappatura, la causa più probabile è il fallback Generic. Controllare sempre il log: `[WARN] definizione non trovata per …` indica esattamente quali fixture sono state processate senza definizione .qxf.
>
> **EN:** If scenes show gross mapping errors, the most likely cause is the Generic fallback. Always check the log: `[WARN] definition not found for …` identifies exactly which fixtures were processed without a .qxf definition.

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

**Marco Coldagelli** — v1.4

---

## Licenza / License

MIT License — libero uso, modifica e distribuzione con attribuzione.
MIT License — free to use, modify and distribute with attribution.
