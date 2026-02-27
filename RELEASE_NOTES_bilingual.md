# Release Notes / Note di rilascio

---

## v1.2.0-beta

&gt; ⚠️ **IT:** Versione di manutenzione — risolve bug critici di ricerca fixture e parsing canali.
&gt; ⚠️ **EN:** Maintenance release — fixes critical fixture search and channel parsing bugs.

---

### 🇮🇹 Correzioni principali / 🇬🇧 Main fixes

#### Ricerca fixture QXF migliorata / Improved QXF fixture search

**IT:** Risolto problema di ricerca file `.qxf` in librerie con struttura non standard. Ora lo script:
- Cerca ricorsivamente in tutte le sottocartelle
- Usa score-based matching per trovare il file più appropriato
- Accetta file anche con manufacturer diverso o vuoto se il match è forte (score ≥ 45)
- Priorizza file con nome manufacturer-modello esatto

**EN:** Fixed `.qxf` file search issues in non-standard library structures. The script now:
- Searches recursively in all subdirectories
- Uses score-based matching to find the most appropriate file
- Accepts files with different or empty manufacturer if match is strong (score ≥ 45)
- Prioritizes files with exact manufacturer-model name

#### Supporto preset canali QLC+ / QLC+ channel preset support

**IT:** Aggiunto riconoscimento automatico dei canali colore e funzione tramite attributo `Preset` nei file QXF:

| Preset | Gruppo assegnato |
|--------|------------------|
| `IntensityRed` / `IntensityGreen` / `IntensityBlue` | Red / Green / Blue |
| `IntensityWhite` | White |
| `IntensityAmber` | Amber |
| `IntensityUV` / `IntensityViolet` | UV |
| `IntensityCyan` / `IntensityMagenta` / `IntensityYellow` | Cyan / Magenta / Yellow |
| `BeamZoomSmallBig` / `BeamZoomBigSmall` | Zoom |
| `FocusNearFar` / `FocusFarNear` | Focus |
| `PrismRotation` / `PrismOnOff` | Prism |
| `SpeedPanTiltSlowFast` | Speed |

**EN:** Added automatic recognition of color and function channels via `Preset` attribute in QXF files:

| Preset | Assigned group |
|--------|----------------|
| `IntensityRed` / `IntensityGreen` / `IntensityBlue` | Red / Green / Blue |
| `IntensityWhite` | White |
| `IntensityAmber` | Amber |
| `IntensityUV` / `IntensityViolet` | UV |
| `IntensityCyan` / `IntensityMagenta` / `IntensityYellow` | Cyan / Magenta / Yellow |
| `BeamZoomSmallBig` / `BeamZoomBigSmall` | Zoom |
| `FocusNearFar` / `FocusFarNear` | Focus |
| `PrismRotation` / `PrismOnOff` | Prism |
| `SpeedPanTiltSlowFast` | Speed |

#### Fallback moving head robusto / Robust moving head fallback

**IT:** Quando non viene trovato il file `.qxf`, il fallback generico ora rileva correttamente i moving head anche da keyword nel nome (es. "Beam", "7R", "230W", "Wash Zoom") e crea automaticamente i canali Pan/Tilt necessari per gli EFX.

**EN:** When `.qxf` file is not found, the generic fallback now correctly detects moving heads from name keywords (e.g. "Beam", "7R", "230W", "Wash Zoom") and automatically creates Pan/Tilt channels needed for EFX.

#### Gestione errori valori None / None value error handling

**IT:** Aggiunta protezione contro valori `None` nelle capability dei canali. Lo script ora salta silenziosamente valori non validi invece di generare errore `TypeError`.

**EN:** Added protection against `None` values in channel capabilities. The script now silently skips invalid values instead of raising `TypeError`.

---

### 🇮🇹 Novità v1.1.0-alpha (mantenute) / 🇬🇧 v1.1.0-alpha features (retained)

&gt; IT: Tutte le funzionalità della v1.1.0-alpha sono mantenute e funzionanti:
&gt; EN: All v1.1.0-alpha features are retained and working:

- Sistema multilingua `--lang it|en` / Multilingual system `--lang it|en`
- Nuovi chaser di gruppo: Stomp Colore, Onda Colore, Alba, Tramonto, Split Colori / Color Stomp, Color Wave, Sunrise, Sundown, Split Colors
- Nuovi chaser globali: Arcobaleno Globale, Stomp Globale, Battito Globale, ecc. / Global Rainbow, Global Stomp, Global Heartbeat, etc.
- Scene GLOBAL colori / GLOBAL color scenes

---

### IT: File di esempio testati / EN: Tested fixture files

| Manufacturer | Model | Canali / Channels | Stato / Status |
|-------------|-------|-------------------|----------------|
| Shehds | Super Beam 230W 7R (new) | 16CH | ✅ Funzionante / Working |
| Shehds | Wash Zoom LED 36x18W RGBWA+UV | 12CH | ✅ Funzionante / Working |
| Generic | RGB / RGBW / Dimmer | vari | ✅ Funzionante / Working |

---

### IT: Debug migliorato / EN: Improved debugging

**IT:** Aggiunti messaggi di debug dettagliati per:
- Varianti del nome modello generate durante la ricerca
- Score di matching dei candidati trovati
- Manufacturer e Model letti dai file QXF
- Canali rilevati per ogni fixture (inclusi gruppi assegnati)

**EN:** Added detailed debug messages for:
- Generated model name variants during search
- Matching score of found candidates
- Manufacturer and Model read from QXF files
- Detected channels for each fixture (including assigned groups)

---

### IT: Compatibilità / EN: Compatibility

| Componente / Component | IT: Versione testata / EN: Tested version |
|-----------|---------------|
| Python | 3.10, 3.11, 3.12 |
| QLC+ | 4.12.x, 4.13.x, 4.14.x |
| Sistema / OS | Linux (Ubuntu 22.04+), macOS 13+, Windows 10/11 |

---

## v1.1.0-alpha *(precedente / previous)*

IT: Prima release con sistema multilingua, chaser globali, nuovi effetti di gruppo.

EN: First release with multilingual system, global chasers, new group effects.

---

## v1.0.0-alpha.1 *(precedente / previous)*

IT: Prima release pubblica con generazione scene statiche, EFX e chaser per singola fixture e gruppo, fallback Generic, raggruppamento per (modello, modo, canali).

EN: First public release with static scene generation, EFX and chasers for single fixture and group, Generic fallback, grouping by (model, mode, channels).
