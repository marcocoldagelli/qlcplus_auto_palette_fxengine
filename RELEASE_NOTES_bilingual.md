# QLC+ Auto Palette FX Engine — Release Notes

## v1.4

> **IT:** Release di correzione e affidabilità. Verificata aprendo i file generati in **QLC+ 4.14.4** e controllando i valori DMX in uscita.
> **EN:** Fix and reliability release. Verified by opening the generated files in **QLC+ 4.14.4** and checking the DMX output values.

### ⚠️ Cambio di comportamento / Behaviour change

Il nuovo profilo predefinito è **`compatto`**: genera meno funzioni per singola fixture quando la fixture fa parte di un gruppo. Per ottenere tutte le varianti come nella v1.3 usare `--profilo completo`.

The new default profile is **`compact`**: it generates fewer single-fixture functions when the fixture belongs to a group. To get every variant as in v1.3, use `--profile full`.

### 🐛 Fix / Bug fixes

#### 🎚️ Master Dimmer e canali da preset / Master Dimmer and preset channels

Lo script riconosceva solo pochi preset di canale (es. `IntensityDimmer`, ma non `IntensityMasterDimmer`). Sulle fixture moderne definite solo con i preset non venivano generate scene dimmer, e le combo "Stage Ready" / "Full Show" lasciavano il dimmer a 0.

The script recognised only a few channel presets (e.g. `IntensityDimmer`, but not `IntensityMasterDimmer`). On modern preset-only fixtures no dimmer scenes were generated, and the "Stage Ready" / "Full Show" combos left the dimmer at 0.

**Fix:** il riconoscimento usa ora la tabella completa dei preset di canale di QLC+ 4.14 (71 preset: gruppo, colore, byte). Vengono riconosciuti correttamente dimmer e master dimmer, canali **fine** (byte LSB), colori, zoom, focus e iris. I canali `Intensity` con elemento `<Colour>` sono trattati come colore e non più come dimmer.

**Fix:** detection now uses the full QLC+ 4.14 channel preset table (71 presets: group, colour, byte). Dimmer and master dimmer, **fine** channels (LSB byte), colours, zoom, focus and iris are correctly recognised. `Intensity` channels with a `<Colour>` element are handled as colour, no longer as dimmer.

---

#### 🔦 Shutter, strobo e prisma / Shutter, strobe and prism

Lo shutter "aperto" veniva cercato nei nomi delle capability anche con la parola chiave `on`, che compare dentro altre parole (es. "Shutter Closed (Not Functi**on**)"): su alcune fixture "Shutter Aperto" e "Stage Ready" chiudevano lo shutter.

The "open" shutter was searched in capability names also with the keyword `on`, which appears inside other words (e.g. "Shutter Closed (Not Functi**on**)"): on some fixtures "Shutter Open" and "Stage Ready" closed the shutter.

**Fix:**

1. Shutter aperto/chiuso, strobo e prisma vengono letti prima dai **preset delle capability** (`ShutterOpen`, `ShutterClose`, `Strobe…SlowToFast/FastToSlow`, `PrismEffectOn/Off`).
2. Solo se i preset mancano si cercano i nomi, e sempre come **parola intera**.
3. Le fasce strobo "Fast-Slow" vengono invertite correttamente (lento = estremo alto della fascia).
4. Le scene shutter/strobo vengono generate anche su fixture senza canale dimmer.
5. Corretto un errore nelle scene strobo di gruppo: le tre velocità condividevano la stessa lista.

**Fix:**

1. Open/closed shutter, strobe and prism are read first from **capability presets** (`ShutterOpen`, `ShutterClose`, `Strobe…SlowToFast/FastToSlow`, `PrismEffectOn/Off`).
2. Names are searched only if presets are missing, and always as **whole words**.
3. "Fast-Slow" strobe ranges are correctly inverted (slow = high end of the range).
4. Shutter/strobe scenes are generated also on fixtures without a dimmer channel.
5. Fixed a bug in group strobe scenes: the three speeds shared the same list.

---

#### 💡 Dimmer generici / Generic dimmers

Le fixture `Generic / Generic` (dimmer interno di QLC+) venivano abbinate per somiglianza di nome a `Generic-Generic-RGBW.qxf` e ricevevano scene colore inesistenti.

`Generic / Generic` fixtures (QLC+ built-in dimmer) were matched by name similarity to `Generic-Generic-RGBW.qxf` and received meaningless colour scenes.

**Fix:** `Generic / Generic` viene riconosciuto come dimmer generico, con un dimmer su **ogni** canale (dimmer pack da 1…N canali). Il match per somiglianza non accetta più un file di produttore diverso quando uno dei due è "Generic".

**Fix:** `Generic / Generic` is recognised as a generic dimmer, with a dimmer on **every** channel (1…N channel dimmer packs). Similarity matching no longer accepts a file from a different manufacturer when either one is "Generic".

---

#### 🎞️ Chaser veloci / Fast chasers

I chaser usavano le dissolvenze delle scene (`Default`), con fade-out predefinito di 2000 ms: con passi brevi i colori si sovrapponevano in HTP (es. "Bicolore Bianco-Viola" restava bianco).

Chasers used the scenes' fades (`Default`), with a default fade-out of 2000 ms: with short steps the colours overlapped in HTP (e.g. "Bicolor White-Violet" stayed white).

**Fix:** tutti i chaser usano dissolvenze **per passo** (`PerStep`), con i valori di ogni passo.

**Fix:** every chaser uses **per-step** fades (`PerStep`), with each step's values.

---

#### 🔄 Ampiezza EFX / EFX amplitude

Le taglie e le ampiezze arrivavano a 200–255, oltre il massimo di QLC+ (127): i movimenti venivano schiacciati ai fine corsa, e "Medio" era già a escursione piena.

Sizes and amplitudes reached 200–255, above the QLC+ maximum (127): movements were clipped at the end stops, and "Medium" was already at full travel.

**Fix:** taglie Piccolo 30 / Medio 70 / Grande 127; sweep Stretto 25 / Medio 60 / Largo 100 / Full 127; varianti larga/stretta 127/30.

**Fix:** sizes Small 30 / Medium 70 / Large 127; sweeps Narrow 25 / Medium 60 / Wide 100 / Full 127; wide/narrow variants 127/30.

---

#### 🎯 Canali fine / Fine channels

I canali `PositionPanFine` / `PositionTiltFine` venivano trattati come canali principali e ricevevano lo stesso valore (es. 127 invece di 0).

`PositionPanFine` / `PositionTiltFine` channels were handled as coarse channels and received the same value (e.g. 127 instead of 0).

**Fix:** i canali fine vengono riconosciuti dalla tabella dei preset e impostati a 0 nelle posizioni.

**Fix:** fine channels are recognised from the preset table and set to 0 in positions.

---

### ✨ Novità / What's new

#### 📦 Profili compatto / completo — Compact / full profiles

Nuova opzione `--profilo compatto|completo` (alias `--profile compact|full`), predefinito `compatto`:

- scene per tutte le fixture (invariato);
- EFX e chaser per singola fixture **solo** per le fixture che non fanno parte di un gruppo (per modello o `FixtureGroup`);
- gruppo per modello saltato se contiene esattamente le stesse fixture di un `FixtureGroup`;
- EFX di gruppo solo in taglia Media.

New option `--profile compact|full` (alias `--profilo compatto|completo`), default `compact`:

- scenes for every fixture (unchanged);
- single-fixture EFX and chasers **only** for fixtures not in a group (per model or `FixtureGroup`);
- per-model group skipped when it contains exactly the same fixtures as a `FixtureGroup`;
- group EFX in Medium size only.

Esempio su un impianto di prova di 18 fixture: 2467 funzioni con `compatto`, 8894 con `completo`.
Example on an 18-fixture test rig: 2467 functions with `compact`, 8894 with `full`.

---

#### 📁 Ricerca definizioni / Definition search

I `.qxf` vengono cercati anche:

- nella **cartella del progetto** (dove QLC+ cerca le definizioni "di progetto");
- nella cartella utente di QLC+ su **macOS** (`~/Library/Application Support/QLC+/fixtures`) e in `~/QLC+/Fixtures`.

`.qxf` files are also searched:

- in the **project folder** (where QLC+ looks for project-local definitions);
- in the QLC+ user folder on **macOS** (`~/Library/Application Support/QLC+/fixtures`) and in `~/QLC+/Fixtures`.

---

### 🧪 Verifica / Verification

Test su tre progetti (impianto di prova con ADJ Focus Spot 4Z, ADJ Inno Pocket Z4, Eurolite LED PAR-64 RGBW+UV, Stairville MH-X25 e dimmer generici; uno spettacolo teatrale; un template busking), in entrambi i profili:

- tutti i file generati si aprono in QLC+ 4.14.4 caricando esattamente il numero di funzioni generate;
- valori DMX verificati in uscita: Stage Ready, shutter, strobo, prisma, colori, chaser di gruppo, EFX di gruppo, dimmer generici.

Tests on three projects (test rig with ADJ Focus Spot 4Z, ADJ Inno Pocket Z4, Eurolite LED PAR-64 RGBW+UV, Stairville MH-X25 and generic dimmers; a theatre show; a busking template), in both profiles:

- every generated file opens in QLC+ 4.14.4 loading exactly the number of generated functions;
- DMX output values verified: Stage Ready, shutter, strobe, prism, colours, group chasers, group EFX, generic dimmers.

Non ancora verificati: fixture CMY, ruote colori/gobo di molti costruttori diversi, fixture multi-head, `--lang en`, `--overwrite`.
Not yet verified: CMY fixtures, colour/gobo wheels from many different manufacturers, multi-head fixtures, `--lang en`, `--overwrite`.

---

## v1.3.1beta

### 🐛 Fix / Bug fixes

#### 🏷️ Lettura nome FixtureGroup robusta / Robust FixtureGroup name reading

Il rilevamento del nome dei `FixtureGroup` QLC+ era fragile: lo script cercava esclusivamente il tag `<n>`, che non è presente in tutte le versioni di QLC+. In caso di mancato rilevamento, il nome del gruppo veniva sostituito dal solo ID numerico (es. `Gruppo 0`, `Gruppo 1`).

The `FixtureGroup` name detection was fragile: the script only looked for the `<n>` tag, which is not present in all QLC+ versions. If not found, the group name was replaced by a plain numeric ID (e.g. `Gruppo 0`, `Gruppo 1`).

**Fix:** la lettura ora prova in sequenza più varianti:

1. Tag `<n>` (formato standard QLC+ 4.x)
2. Tag `<Name>` o `<name>` (varianti di versione)
3. Attributo XML `name` / `Name`
4. Fallback a `Gruppo {ID}` solo se nessuna variante restituisce testo

**Fix:** name reading now tries multiple variants in sequence:

1. Tag `<n>` (standard QLC+ 4.x format)
2. Tag `<Name>` or `<name>` (version variants)
3. XML attribute `name` / `Name`
4. Fallback to `Gruppo {ID}` only if no variant returns text

---

#### 🔢 Formato label QLC-GRUPPI / QLC-GRUPPI label format

I gruppi QLC+ vengono ora nominati con formato `{ID} - {Nome}` (es. `0 - Matrice fondale`) invece del solo nome. Questo rende il label leggibile anche in presenza di nomi simili o ambigui, e mantiene sempre visibile il riferimento all'ID QLC+.

QLC+ groups are now labelled as `{ID} - {Name}` (e.g. `0 - Backdrop Matrix`) instead of the bare name. This keeps the label readable even with similar or ambiguous names, and always shows the QLC+ ID as a reference.

> Questo fix riguarda **esclusivamente** i gruppi `QLC-GRUPPI/` introdotti in v1.3beta.  
> I gruppi per-modello (`GRUPPI/`) non sono stati modificati.  
> This fix affects **only** the `QLC-GRUPPI/` groups introduced in v1.3beta.  
> Per-model groups (`GRUPPI/`) are unchanged.

---

## v1.3beta

### Novità / What's new

#### 🗂️ Supporto FixtureGroup QLC+ / QLC+ FixtureGroup support

Lo script legge ora i gruppi di fixture definiti manualmente dal light designer direttamente nel progetto QLC+ (`<FixtureGroup>`). Per ciascun gruppo vengono generate automaticamente scene, EFX e chaser dedicati, organizzati sotto i path:

- `Auto Palette/QLC-GRUPPI/<Nome Gruppo>`
- `Auto Palette/EFX/QLC-GRUPPI/<Nome Gruppo>`
- `Auto Palette/CHASER/QLC-GRUPPI/<Nome Gruppo>`

The script now reads fixture groups manually defined by the lighting designer directly in the QLC+ project (`<FixtureGroup>`). For each group, dedicated scenes, EFX and chasers are automatically generated, organised under:

- `Auto Palette/QLC-GRUPPI/<Group Name>`
- `Auto Palette/EFX/QLC-GRUPPI/<Group Name>`
- `Auto Palette/CHASER/QLC-GRUPPI/<Group Name>`

> I gruppi per-modello generati automaticamente restano invariati — le due famiglie coesistono nel progetto.  
> Auto-generated per-model groups are unchanged — both families coexist in the project.

---

#### ⚡ Intersezione capabilities per gruppi eterogenei / Capability intersection for heterogeneous groups

Per i gruppi QLC+, che tipicamente contengono fixture di modelli diversi, vengono generati **solo gli effetti supportati da tutte le fixture del gruppo**. Se ad esempio un gruppo misto non ha il canale gobo comune a tutti i membri, le scene gobo non vengono create per quel gruppo.

For QLC+ groups, which typically contain fixtures of different models, **only effects supported by all fixtures in the group** are generated. If for example a mixed group does not share a common gobo channel across all members, gobo scenes will not be created for that group.

---

#### 🌐 Prefisso GRUPPO localizzato / Localised GROUP prefix

Il prefisso dei nomi delle funzioni di gruppo è ora correttamente localizzato:

- `--lang it` → `GRUPPO <nome>`
- `--lang en` → `GROUP <name>`

Questo fix riguardava anche i gruppi per-modello della versione precedente, dove il prefisso era sempre in italiano indipendentemente dalla lingua scelta.

The group function name prefix is now correctly localised. This fix also applied to per-model groups from the previous version, where the prefix was always in Italian regardless of the selected language.

---

#### 💬 Output terminale localizzato / Localised terminal output

Tutti i messaggi dell'output terminale (intestazioni di passata, riepilogo finale, messaggi di errore) sono ora tradotti in inglese quando si usa `--lang en`.

All terminal output messages (pass headers, final summary, error messages) are now translated to English when using `--lang en`.

Implementato tramite dizionario `UI_STRINGS` e funzione `U()`, separati da `STRINGS`/`T()` che gestiscono i nomi delle funzioni QLC+ nel file `.qxw`.

Implemented via a dedicated `UI_STRINGS` dictionary and `U()` function, kept separate from `STRINGS`/`T()` which handle QLC+ function names written to the `.qxw` file.

---

### Versioni precedenti / Previous versions

#### v1.2beta — Fix

- Ricerca ricorsiva in tutte le sottocartelle della libreria fixture / Recursive search in all fixture library subfolders
- Pattern di ricerca flessibili per nomi file diversi / Flexible search patterns for variant file names
- Fallback intelligente per moving head: rileva Pan/Tilt anche senza definizione QXF / Smart fallback for moving heads: detects Pan/Tilt even without QXF definition

#### v1.1alpha — Novità / What's new

- Sistema multilingua IT/EN (`--lang it|en`) / IT/EN multilingual system
- Nuovi chaser di gruppo RGB: Color Stomp, Color Wave, Sunrise, Sundown, Split Colors / New RGB group chasers
- Nuovi chaser globali (tutte le fixture): Rainbow, Stomp, Police, Sunrise, Heartbeat, Strobe / New global chasers (all fixtures)
- Commenti interni bilingue IT+EN / Bilingual internal comments

---

*Marco Coldagelli — [github.com/marcocoldagelli](https://github.com/marcocoldagelli)*
