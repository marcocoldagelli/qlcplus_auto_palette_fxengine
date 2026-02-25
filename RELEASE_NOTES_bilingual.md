# Release Notes / Note di rilascio

---

## v1.1.0-alpha.4

> ⚠️ **IT:** Versione alpha — funzionante e testata, ma l'API interna (nomi costanti, struttura funzioni) potrebbe cambiare in versioni future.
> ⚠️ **EN:** Alpha release — working and tested, but the internal API (constant names, function structure) may change in future versions.

---

### 🇮🇹 Novità / 🇬🇧 What's new

#### Sistema multilingua / Multilingual system

**IT:** Aggiunto supporto completo per lingua dei nomi delle scene generati. Usare `--lang it` (default) o `--lang en` da riga di comando.

**EN:** Full language support added for generated scene names. Use `--lang it` (default) or `--lang en` on the command line.

```bash
# Italiano (default)
python3 qlcplus_auto_palette_fxengine.py show.qxw

# English
python3 qlcplus_auto_palette_fxengine.py show.qxw --lang en
```

IT: Cosa viene tradotto con `--lang en`:
EN: What gets translated with `--lang en`:
- Colori RGB e CMY / RGB and CMY color names
- Scene dimmer, shutter, zoom, iris, combo
- Nomi EFX: taglie, velocità, modificatori / EFX names: sizes, speeds, modifiers
- Tutti i nomi di Chaser / All chaser names
- Bicolori e tricolori / Bicolor and tricolor sequences

#### Nuovi chaser di gruppo RGB / New RGB group chasers

IT: Aggiunti 5 nuovi tipi di chaser nella sezione di gruppo, tutti disponibili in IT e EN:

EN: Added 5 new chaser types in the group section, all available in IT and EN:

| IT | EN | Descrizione / Description |
|----|----|--------------------------|
| **Stomp Colore** | **Color Stomp** | IT: Ogni fixture lampeggia su un colore diverso in sequenza. EN: Each fixture flashes on a different sequential color. |
| **Onda Colore** | **Color Wave** | IT: Onda cromatica — ogni fixture prende il colore successivo del ciclo. EN: Chromatic wave — each fixture takes the next color in the cycle. |
| **Alba** | **Sunrise** | IT: Progressione Rosso → Arancio → Giallo → Bianco Caldo → Bianco con crossfade. EN: Ramp Red → Orange → Yellow → Warm White → White with crossfade. |
| **Tramonto** | **Sundown** | IT: Inverso dell'Alba — da Bianco verso il rosso scuro. EN: Reverse of Sunrise — from White towards deep red. |
| **Split Colori** | **Split Colors** | IT: Fixture dispari = colori caldi, pari = colori freddi, alternati nel tempo. EN: Odd fixtures = warm colors, even fixtures = cool colors, alternating over time. |

#### Nuovi chaser globali / New global chasers

IT: Aggiunta una nuova categoria `CHASER/GLOBAL` con chaser che coinvolgono **tutte le fixture** del progetto simultaneamente, usando le scene `GLOBAL »` pregenerate.

EN: Added a new `CHASER/GLOBAL` category with chasers involving **all project fixtures** simultaneously, using the pre-generated `GLOBAL »` scenes.

| IT | EN | Descrizione / Description |
|----|----|----|
| **Arcobaleno Globale** | **Global Rainbow** | IT: Tutte le fixture ciclano sull'arcobaleno (+ Smooth). EN: All fixtures cycle through the rainbow (+ Smooth). |
| **Stomp Globale** | **Global Stomp** | IT: Tutte le fixture insieme full/zero. EN: All fixtures together full/zero. |
| **Battito Globale** | **Global Heartbeat** | IT: Pulsazione dimmer su tutte le fixture. EN: Dimmer pulse on all fixtures. |
| **Impulso Globale** | **Global Pulse** | IT: Singolo flash ciclico globale. EN: Single cyclic global flash. |
| **Polizia Globale** | **Global Police** | IT: Rosso/Blu strobo su tutte le fixture RGB. EN: Red/Blue strobe on all RGB fixtures. |
| **Alba Globale** | **Global Sunrise** | IT: Progressione cromatica dall'alba su tutte le fixture. EN: Chromatic sunrise progression on all fixtures. |
| **Strobo Globale** | **Global Strobe** | IT: Shutter open/closed su tutte le fixture con Shutter. EN: Shutter open/closed on all fixtures with a Shutter channel. |
| **Colori Caldi/Freddi Globale** | **Global Warm/Cool Colors** | IT: Palette caldi/freddi su tutte le fixture RGB. EN: Warm/cool palettes on all RGB fixtures. |
| **Club/Discoteca Globale** | **Global Club/Disco** | IT: Club e discoteca su tutte le fixture. EN: Club and disco on all fixtures. |

#### Scene GLOBAL colori / GLOBAL color scenes

IT: Aggiunte scene `GLOBAL » <Colore>` (es. `GLOBAL » Rosso`, `GLOBAL » White`) che impostano contemporaneamente tutti i canali RGB di tutte le fixture allo stesso colore. Queste scene sono anche la base dei nuovi chaser globali.

EN: Added `GLOBAL » <Color>` scenes (e.g. `GLOBAL » Red`, `GLOBAL » White`) that simultaneously set all RGB channels of all fixtures to the same color. These scenes are also the foundation of the new global chasers.

#### Commenti interni bilingue / Bilingual internal comments

IT: Tutti i commenti principali nello script sono ora disponibili sia in italiano che in inglese.

EN: All main comments in the script are now available in both Italian and English.

---

### IT: Opzioni da riga di comando / EN: Command-line options

| Opzione / Option | Valore / Value | Default | IT | EN |
|---|---|---|---|---|
| `--output` | `FILE.qxw` | `input_palette.qxw` | File di output | Output file |
| `--fixture-dir` | `PATH` | — | Dir aggiuntiva `.qxf` | Additional `.qxf` dir |
| `--fade-in` | `MS` | `0` | FadeIn scene (ms) | Scene fade in (ms) |
| `--fade-out` | `MS` | `2000` | FadeOut scene (ms) | Scene fade out (ms) |
| `--lang` | `it`\|`en` | `it` | **NUOVO** — lingua nomi | **NEW** — name language |
| `--overwrite` | flag | off | Sovrascrive esistenti | Overwrite existing |
| `--skip-groups` | flag | off | Salta gruppi | Skip groups |
| `--skip-combos` | flag | off | Salta combo | Skip combos |
| `--skip-efx` | flag | off | Salta EFX | Skip EFX |
| `--skip-chasers` | flag | off | Salta chaser | Skip chasers |
| `--min-cap-scenes` | `N` | `2` | Min capability | Min capabilities |

---

### IT: Limitazioni note / EN: Known limitations

- IT: I canali Pan/Tilt devono essere correttamente definiti nel file `.qxf` con `Group=Pan`/`Tilt` o con il preset `PositionPan`/`PositionTilt`; fixture con definizioni `.qxf` incomplete potrebbero non generare EFX.
  EN: Pan/Tilt channels must be correctly defined in the `.qxf` file with `Group=Pan`/`Tilt` or with the `PositionPan`/`PositionTilt` preset; fixtures with incomplete `.qxf` definitions may not generate EFX.
- IT: Le fixture Generic ricevono capabilities semplificate: scene strobe e color wheel non vengono generate per queste fixture.
  EN: Generic fixtures receive simplified capabilities: strobe and color wheel scenes are not generated for these fixtures.
- IT: `--fade-in` / `--fade-out` si applicano uniformemente a tutte le scene.
  EN: `--fade-in` / `--fade-out` apply uniformly to all scenes.
- IT: I chaser di gruppo `Onda Colore` / `Split Colori` richiedono che le scene per-fixture dei singoli colori esistano nel `scene_map`; se una fixture non ha canali RGB, quella fixture viene saltata silenziosamente nel chaser.
  EN: The `Color Wave` / `Split Colors` group chasers require that per-fixture color scenes exist in `scene_map`; if a fixture has no RGB channels, it is silently skipped in the chaser.

---

### IT: Compatibilità / EN: Compatibility

| Componente / Component | IT: Versione testata / EN: Tested version |
|-----------|---------------|
| Python | 3.10, 3.11, 3.12 |
| QLC+ | 4.12.x, 4.13.x |
| Sistema / OS | Linux (Ubuntu 22.04+), macOS 13+, Windows 10/11 |

---

## v1.0.0-alpha.1 *(precedente / previous)*

IT: Prima release pubblica con generazione scene statiche, EFX e chaser per singola fixture e gruppo, fallback Generic, raggruppamento per (modello, modo, canali).

EN: First public release with static scene generation, EFX and chasers for single fixture and group, Generic fallback, grouping by (model, mode, channels).
