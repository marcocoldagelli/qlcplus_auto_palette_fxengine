# QLC+ Auto Palette FX Engine — Release Notes

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
