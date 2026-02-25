#!/usr/bin/env python3
"""
qlcplus_auto_palette_fxengine.py  v1.1alpha  Marco Coldagelli
==============================
IT: Legge un file .qxw di QLC+ (con fixture già definite e patchate),
    carica le definizioni fixture (.qxf) dalla libreria di QLC+,
    e genera automaticamente una palette completa di scene organizzate
    per tipo di fixture e funzionalità.
EN: Reads a QLC+ project file (.qxw) with fixtures already defined and patched,
    loads fixture definitions (.qxf) from the QLC+ library,
    and automatically generates a complete palette of scenes organised
    by fixture type and functionality.

Novità v1.1alpha / What's new in v1.1alpha:
  - Sistema multilingua IT/EN (--lang it|en) / IT/EN multilingual system (--lang it|en)
  - Nuovi chaser di gruppo RGB: Color Stomp, Color Wave, Sunrise, Sundown, Split Colors
    New RGB group chasers: Color Stomp, Color Wave, Sunrise, Sundown, Split Colors
  - Nuovi chaser globali (tutte le fixture): Rainbow, Stomp, Police, Sunrise, Heartbeat, Strobe
    New global chasers (all fixtures): Rainbow, Stomp, Police, Sunrise, Heartbeat, Strobe
  - Commenti interni bilingue IT+EN / Bilingual internal comments IT+EN

PALETTE GENERATE (per tipologia):
──────────────────────────────────
 GLOBAL
   • Blackout / Full / 25% / 50% / 75%
   • All Shutter Open / All Shutter Closed
   • All Moving → Center
   • All Strobe Slow / Med / Fast

 PER OGNI FIXTURE
   DIMMER/INTENSITY
   • Zero / 10% / 25% / 50% / 75% / Full
   • Strobe Slow / Medium / Fast / Stop (da capability)
   • Shutter Open / Closed

   COLORI RGB
   • Bianco / Bianco Caldo / Bianco Freddo
   • Rosso / Verde / Blu
   • Giallo / Ciano / Magenta
   • Arancio / Rosa / Corallo / Lavanda / Lime / Teal / Indaco
   • Ambra / Viola / Gold / Acquamarina
   • Rosso Scuro / Blu Notte / Verde Bosco
   • Pastello: Rosa / Azzurro / Menta / Lilla / Pesca

   RGBW (aggiunte varianti con canale White)
   • Bianco puro (solo W) / Bianco misto (RGB+W)

   RGBA / RGBAW
   • varianti con Amber combinato

   UV
   • UV Full / UV Half / UV + Blu

   CANALE WHITE STANDALONE
   • Zero / 25% / 50% / 75% / Full

   CANALE AMBER STANDALONE
   • Zero / 25% / 50% / 75% / Full

   CMY
   • Bianco / Rosso / Verde / Blu / Giallo / Ciano / Magenta
   • Arancio / Rosa / Lavanda / Gold

   COLOR WHEEL
   • ogni colore/posizione dalle capability del canale

   GOBO
   • ogni gobo dalle capability (tutti i canali gobo)
   • Gobo Rotation On/Off (se presente canale gobo rotation)

   PRISM
   • Prism Open / Prism In / Prism Off (da capability)

   FOCUS / ZOOM / IRIS / FROST
   • Zoom Stretto / Medio / Largo
   • Iris Aperto / Metà / Chiuso
   • Focus Near / Mid / Far
   • Frost On / Off

   MOVING HEAD — POSIZIONI
   • Pan: Far Left / Left / Center / Right / Far Right
   • Tilt: Down / Low / Center / High / Up
   • Combinazioni: DS-C / DS-SL / DS-SR / US-C / US-SL / US-SR
   • Stage positions: Front Wash / Back Wash / Side Left / Side Right
   • PT Home (0,0) / PT Center / PT Audience
   • Pan+Tilt con fine canali allineati

   SPEED / MACRO / EFFECT
   • Speed Stop / Slow / Medium / Fast
   • ogni capability del canale Effect o Macro

 MOVING HEAD — EFFETTI DI MOVIMENTO (funzioni EFX di QLC+)
   FORME (per ogni fixture moving, 3 taglie × 4 velocità):
   • Circle             → cerchio standard
   • Circle 45°         → cerchio ruotato (diverso per Diamond/Square)
   • Eight Orizzontale  → figura 8 su asse X
   • Eight Verticale    → figura 8 su asse Y
   • Eight Diagonale    → figura 8 a 45°
   • Pan Sweep          → oscillazione orizzontale pura (Line 0°)
   • Tilt Swing         → oscillazione verticale pura (Line 90°)
   • Pan Sweep Largo    → ampiezza massima
   • Diamond            → rombo
   • Square             → quadrato
   • SquareChoppy       → quadrato scattoso (robot)
   • Leaf               → foglia (loop asimmetrico)
   • Lissajous 2:1      → figura armonica freq 2:1
   • Lissajous 3:2      → figura armonica freq 3:2
   • Lissajous 1:3      → figura armonica freq 1:3
   • Lissajous 3:1      → figura armonica freq 3:1
   VELOCITÀ: Molto Lento (20s) / Lento (12s) / Medio (6s) / Veloce (3s) / Velocissimo (1.5s)
   TAGLIE: Piccolo (w=60) / Medio (w=127) / Grande (w=200)

   EFFETTI DI GRUPPO (per ≥2 fixture dello stesso tipo):
   • Sync              → tutte in fase (stessa traiettoria)
   • Fan               → sfasamento progressivo 0..360°
   • Mirror            → metà avanti / metà indietro
   • Opposto           → coppie a 180° di fase
   • Wave              → fase a onda progressiva
   • Chase Seq         → sequenza a catena (offset 360/n × i)
   Per forme: Circle, Eight Oriz/Vert, Pan Sweep, Tilt Swing, Diamond, Square, Lissajous 2:1

 PER GRUPPO (≥2 fixture stesso modello) — SCENE
   • Full / Blackout / 50%
   • tutti i colori RGB
   • tutti i colori CMY
   • tutte le posizioni Moving
   • Strobe + Speed
   • colori alternati (ODD/EVEN split)

 COMBO UTILI (per fixture complesse)
   • Stage Ready = dimmer full + shutter open + bianco + PT center
   • Blackout Totale = dimmer 0 + shutter chiuso
   • Full Show = dimmer full + shutter open + bianco/open gobo

Uso:
  python3 qlcplus_auto_palette.py <file.qxw> \\
          [--fixture-dir /path/to/fixtures] \\
          [--output out.qxw] \\
          [--fade-in MS] [--fade-out MS] \\
          [--overwrite] [--skip-groups] [--skip-combos] \\
          [--min-cap-scenes N]
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

# ─── Lingua / Language ────────────────────────────────────────────────────────
# IT: Imposta la lingua con --lang it (default) o --lang en da riga di comando.
# EN: Set the language with --lang it (default) or --lang en on the command line.
LANG = "it"

# Dizionario traduzioni: chiave → stringa localizzata
STRINGS = {
    "it": {
        # Shutter
        "Shutter Aperto":        "Shutter Aperto",
        "Shutter Chiuso":        "Shutter Chiuso",
        "All Shutter Aperto":    "All Shutter Aperto",
        "All Shutter Chiuso":    "All Shutter Chiuso",
        # Zoom
        "Zoom Stretto":          "Zoom Stretto",
        "Zoom Medio":            "Zoom Medio",
        "Zoom Largo":            "Zoom Largo",
        # Iris
        "Iris Aperto":           "Iris Aperto",
        "Iris Metà":             "Iris Metà",
        "Iris Chiuso":           "Iris Chiuso",
        # Combo
        "Blackout Totale":       "Blackout Totale",
        "Rosso Puro":            "Rosso Puro",
        "Bianco Puro":           "Bianco Puro",
        "Blu Puro":              "Blu Puro",
        # White variants
        "White Puro (W)":        "White Puro (W)",
        "White Misto (RGB+W)":   "White Misto (RGB+W)",
        # Group
        "Alternato":             "Alternato",
        # EFX sizes
        "Piccolo":               "Piccolo",
        "Grande":                "Grande",
        # EFX/chaser speeds
        "Molto Lento":           "Molto Lento",
        "Lento":                 "Lento",
        "Medio":                 "Medio",
        "Veloce":                "Veloce",
        "Velocissimo":           "Velocissimo",
        "Lentissimo":            "Lentissimo",
        "Strobo":                "Strobo",
        "Mega Strobo":           "Mega Strobo",
        # EFX amplitude
        "Stretto":               "Stretto",
        "Largo":                 "Largo",
        "Full":                  "Full",
        # EFX misc
        "Inverso":               "Inverso",
        "Opposto":               "Opposto",
        "Coppie":                "Coppie",
        # Chaser — dimmer
        "Flicker Fiamma":        "Flicker Fiamma",
        "Ramp Up Down":          "Ramp Up Down",
        "Posizioni Casuali":     "Posizioni Casuali",
        # Chaser — RGB
        "Arcobaleno":            "Arcobaleno",
        "Rainbow Completo":      "Rainbow Completo",
        "Rainbow Casuale":       "Rainbow Casuale",
        "Pastelli":              "Pastelli",
        "Pastelli Smooth":       "Pastelli Smooth",
        "Colori Caldi":          "Colori Caldi",
        "Colori Freddi":         "Colori Freddi",
        "Colori Teatrali":       "Colori Teatrali",
        "Colori Teatrali Smooth":"Colori Teatrali Smooth",
        "Discoteca":             "Discoteca",
        "Discoteca Casuale":     "Discoteca Casuale",
        "Primari":               "Primari",
        "Secondari":             "Secondari",
        "Bicolore":              "Bicolore",
        "Tricolore":             "Tricolore",
        "Strobe Arcobaleno":     "Strobe Arcobaleno",
        "Lampo Bianco":          "Lampo Bianco",
        "Ambulanza":             "Ambulanza",
        "Tecno":                 "Tecno",
        "Tecno Casuale":         "Tecno Casuale",
        "Warm-Cool":             "Warm-Cool",
        "Club Colors":           "Club Colors",
        # Chaser — CMY
        "CMY Arcobaleno":        "CMY Arcobaleno",
        "CMY Rainbow Casuale":   "CMY Rainbow Casuale",
        "CMY Caldi":             "CMY Caldi",
        "CMY Freddi":            "CMY Freddi",
        # Chaser — moving
        "Pan Oscillazione":      "Pan Oscillazione",
        "Tilt Oscillazione":     "Tilt Oscillazione",
        "Stage Sweep":           "Stage Sweep",
        "Audience Scan":         "Audience Scan",
        "Position Chase DS-US":  "Position Chase DS-US",
        "Position Chase Corner": "Position Chase Corner",
        "Position + Color Chase Medio": "Position + Color Chase Medio",
        # Chaser — group
        "Chase Sequenziale":     "Chase Sequenziale",
        "Chase PingPong":        "Chase PingPong",
        "Chase Casuale":         "Chase Casuale",
        "Knight Rider":          "Knight Rider",
        "Chase A Coppie":        "Chase A Coppie",
        "ODD/EVEN Flash":        "ODD/EVEN Flash",
        "ODD/EVEN + Full":       "ODD/EVEN + Full",
        "Stomp Gruppo":          "Stomp Gruppo",
        "Lightning Gruppo":      "Lightning Gruppo",
        "Double Flash Gruppo":   "Double Flash Gruppo",
        "Triple Flash Gruppo":   "Triple Flash Gruppo",
        "Ripple Colori":         "Ripple Colori",
        "PT Chase Palco":        "PT Chase Palco",
        "PT Corner Chase":       "PT Corner Chase",
        "PT Corner PingPong":    "PT Corner PingPong",
        "PT Posizioni Casuali":  "PT Posizioni Casuali",
        "Waterfall":             "Waterfall",
        # Nuovi chaser di gruppo colore / New group color chasers
        "Stomp Colore":          "Stomp Colore",
        "Onda Colore":           "Onda Colore",
        "Alba":                  "Alba",
        "Tramonto":              "Tramonto",
        "Split Colori":          "Split Colori",
        # Chaser globali / Global chasers
        "Arcobaleno Globale":    "Arcobaleno Globale",
        "Stomp Globale":         "Stomp Globale",
        "Polizia Globale":       "Polizia Globale",
        "Alba Globale":          "Alba Globale",
        "Battito Globale":       "Battito Globale",
        "Strobo Globale":        "Strobo Globale",
        "Impulso Globale":       "Impulso Globale",
        # Colori (usati nei lookup chaser)
        "Rosso":                 "Rosso",
        "Blu":                   "Blu",
        "Verde":                 "Verde",
        "Bianco":                "Bianco",
        "Giallo":                "Giallo",
        "Ciano":                 "Ciano",
        "Magenta":               "Magenta",
        "Ambra":                 "Ambra",
        "Arancio":               "Arancio",
        "Bianco Caldo":          "Bianco Caldo",
        "Ghiaccio":              "Ghiaccio",
        "Bianco Freddo":         "Bianco Freddo",
        "Viola":                 "Viola",
        "Indaco":                "Indaco",
    },
    "en": {
        # Shutter
        "Shutter Aperto":        "Shutter Open",
        "Shutter Chiuso":        "Shutter Closed",
        "All Shutter Aperto":    "All Shutter Open",
        "All Shutter Chiuso":    "All Shutter Closed",
        # Zoom
        "Zoom Stretto":          "Zoom Narrow",
        "Zoom Medio":            "Zoom Medium",
        "Zoom Largo":            "Zoom Wide",
        # Iris
        "Iris Aperto":           "Iris Open",
        "Iris Metà":             "Iris Half",
        "Iris Chiuso":           "Iris Closed",
        # Combo
        "Blackout Totale":       "Full Blackout",
        "Rosso Puro":            "Pure Red",
        "Bianco Puro":           "Pure White",
        "Blu Puro":              "Pure Blue",
        # White variants
        "White Puro (W)":        "Pure White (W)",
        "White Misto (RGB+W)":   "Mixed White (RGB+W)",
        # Group
        "Alternato":             "Alternating",
        # EFX sizes
        "Piccolo":               "Small",
        "Grande":                "Large",
        # EFX/chaser speeds
        "Molto Lento":           "Very Slow",
        "Lento":                 "Slow",
        "Medio":                 "Medium",
        "Veloce":                "Fast",
        "Velocissimo":           "Very Fast",
        "Lentissimo":            "Very Slow",
        "Strobo":                "Strobe",
        "Mega Strobo":           "Mega Strobe",
        # EFX amplitude
        "Stretto":               "Narrow",
        "Largo":                 "Wide",
        "Full":                  "Full",
        # EFX misc
        "Inverso":               "Reverse",
        "Opposto":               "Opposite",
        "Coppie":                "Pairs",
        # Chaser — dimmer
        "Flicker Fiamma":        "Flame Flicker",
        "Ramp Up Down":          "Ramp Up Down",
        "Posizioni Casuali":     "Random Positions",
        # Chaser — RGB
        "Arcobaleno":            "Rainbow",
        "Rainbow Completo":      "Full Rainbow",
        "Rainbow Casuale":       "Random Rainbow",
        "Pastelli":              "Pastels",
        "Pastelli Smooth":       "Pastels Smooth",
        "Colori Caldi":          "Warm Colors",
        "Colori Freddi":         "Cool Colors",
        "Colori Teatrali":       "Theatrical",
        "Colori Teatrali Smooth":"Theatrical Smooth",
        "Discoteca":             "Disco",
        "Discoteca Casuale":     "Random Disco",
        "Primari":               "Primary",
        "Secondari":             "Secondary",
        "Bicolore":              "Bicolor",
        "Tricolore":             "Tricolor",
        "Strobe Arcobaleno":     "Strobe Rainbow",
        "Lampo Bianco":          "White Flash",
        "Ambulanza":             "Ambulance",
        "Tecno":                 "Techno",
        "Tecno Casuale":         "Random Techno",
        "Warm-Cool":             "Warm-Cool",
        "Club Colors":           "Club Colors",
        # Chaser — CMY
        "CMY Arcobaleno":        "CMY Rainbow",
        "CMY Rainbow Casuale":   "CMY Random Rainbow",
        "CMY Caldi":             "CMY Warm",
        "CMY Freddi":            "CMY Cool",
        # Chaser — moving
        "Pan Oscillazione":      "Pan Oscillation",
        "Tilt Oscillazione":     "Tilt Oscillation",
        "Stage Sweep":           "Stage Sweep",
        "Audience Scan":         "Audience Scan",
        "Position Chase DS-US":  "Position Chase DS-US",
        "Position Chase Corner": "Position Chase Corner",
        "Position + Color Chase Medio": "Position + Color Chase Medium",
        # Chaser — group
        "Chase Sequenziale":     "Sequential Chase",
        "Chase PingPong":        "Chase PingPong",
        "Chase Casuale":         "Random Chase",
        "Knight Rider":          "Knight Rider",
        "Chase A Coppie":        "Pairs Chase",
        "ODD/EVEN Flash":        "ODD/EVEN Flash",
        "ODD/EVEN + Full":       "ODD/EVEN + Full",
        "Stomp Gruppo":          "Group Stomp",
        "Lightning Gruppo":      "Lightning Group",
        "Double Flash Gruppo":   "Double Flash Group",
        "Triple Flash Gruppo":   "Triple Flash Group",
        "Ripple Colori":         "Color Ripple",
        "PT Chase Palco":        "PT Stage Chase",
        "PT Corner Chase":       "PT Corner Chase",
        "PT Corner PingPong":    "PT Corner PingPong",
        "PT Posizioni Casuali":  "PT Random Positions",
        "Waterfall":             "Waterfall",
        # Nuovi chaser di gruppo colore / New group color chasers
        "Stomp Colore":          "Color Stomp",
        "Onda Colore":           "Color Wave",
        "Alba":                  "Sunrise",
        "Tramonto":              "Sundown",
        "Split Colori":          "Split Colors",
        # Chaser globali / Global chasers
        "Arcobaleno Globale":    "Global Rainbow",
        "Stomp Globale":         "Global Stomp",
        "Polizia Globale":       "Global Police",
        "Alba Globale":          "Global Sunrise",
        "Battito Globale":       "Global Heartbeat",
        "Strobo Globale":        "Global Strobe",
        "Impulso Globale":       "Global Pulse",
        # Colori (usati nei lookup chaser)
        "Rosso":                 "Red",
        "Blu":                   "Blue",
        "Verde":                 "Green",
        "Bianco":                "White",
        "Giallo":                "Yellow",
        "Ciano":                 "Cyan",
        "Magenta":               "Magenta",
        "Ambra":                 "Amber",
        "Arancio":               "Orange",
        "Bianco Caldo":          "Warm White",
        "Ghiaccio":              "Ice",
        "Bianco Freddo":         "Cool White",
        "Viola":                 "Violet",
        "Indaco":                "Indigo",
    },
}


def T(key):
    """Restituisce la stringa localizzata per la lingua corrente (LANG)."""
    return STRINGS.get(LANG, STRINGS["it"]).get(key, key)


# ─── Percorsi default libreria QLC+ / Default QLC+ fixture library search paths ─────
FIXTURE_SEARCH_PATHS = [
    "/usr/share/qlcplus/fixtures",
    "/usr/local/share/qlcplus/fixtures",
    "/Applications/QLC+.app/Contents/Resources/fixtures",
    r"C:\QLC+\fixtures",
    r"C:\Program Files\QLC+\fixtures",
    str(Path.home() / "QLC+" / "fixtures"),
    str(Path.home() / ".qlcplus" / "fixtures"),
]

# ─── Gruppi canale QLC+ / QLC+ channel group constants ──────────────────────────
G_INTENSITY = "Intensity"
G_RED       = "Red"
G_GREEN     = "Green"
G_BLUE      = "Blue"
G_WHITE     = "White"
G_AMBER     = "Amber"
G_UV        = "UV"
G_CYAN      = "Cyan"
G_MAGENTA   = "Magenta"
G_YELLOW    = "Yellow"
G_COLOUR    = "Colour"
G_GOBO      = "Gobo"
G_PAN       = "Pan"
G_TILT      = "Tilt"
G_SHUTTER   = "Shutter"
G_PRISM     = "Prism"
G_SPEED     = "Speed"
G_EFFECT    = "Effect"
G_FOCUS     = "Focus"
G_ZOOM      = "Zoom"
G_IRIS      = "Iris"
G_FROST     = "Beam"      # QLC+ usa "Beam" per frost/diffusion
G_MACRO     = "Macro"
G_NOTHING   = "Nothing"

# ─── Palette colori RGB estesa / Extended RGB color palette ─────────────────────
# (nome/name, R, G, B)
RGB_PALETTE = [
    # Bianchi / Whites
    ("Bianco",            255, 255, 255),
    ("Bianco Caldo",      255, 200, 100),
    ("Bianco Freddo",     200, 220, 255),
    # Primari / Primary
    ("Rosso",             255,   0,   0),
    ("Verde",               0, 255,   0),
    ("Blu",                 0,   0, 255),
    # Secondari / Secondary
    ("Giallo",            255, 255,   0),
    ("Ciano",               0, 255, 255),
    ("Magenta",           255,   0, 255),
    # Terziari / Tertiary
    ("Arancio",           255, 128,   0),
    ("Rosa",              255,  20, 147),
    ("Corallo",           255,  80,  60),
    ("Lime",              128, 255,   0),
    ("Teal",                0, 200, 180),
    ("Lavanda",           180, 100, 255),
    ("Indaco",             75,   0, 130),
    # Saturi / Saturated
    ("Ambra",             255, 160,   0),
    ("Viola",             148,   0, 211),
    ("Gold",              255, 200,   0),
    ("Acquamarina",        50, 255, 200),
    # Scuri / Teatrali / Dark / Theatrical
    ("Rosso Scuro",       180,   0,   0),
    ("Blu Notte",           0,   0, 160),
    ("Verde Bosco",         0, 100,   0),
    ("Cremisi",           180,   0,  50),
    ("Azzurro Reale",       0,  80, 255),
    # Pastelli / Pastels (soft atmospheres)
    ("Pastello Rosa",     255, 182, 193),
    ("Pastello Azzurro",  173, 216, 230),
    ("Pastello Menta",    152, 255, 152),
    ("Pastello Lilla",    221, 160, 221),
    ("Pastello Pesca",    255, 218, 185),
    ("Pastello Giallo",   255, 255, 153),
    # Fuoco/Ghiaccio / Fire/Ice
    ("Fuoco",             255,  60,   0),
    ("Ghiaccio",          150, 220, 255),
    ("Brace",             255,  30,   0),
    # Party / UV Simulation
    ("UV Sim",             80,   0, 200),
    ("Strobe Bianco",     255, 255, 255),  # alias per strobe preset
]

# ─── Palette colori CMY / CMY color palette (0 = open, 255 = saturated) ───────
# (nome/name, C, M, Y)
CMY_PALETTE = [
    ("Bianco",      0,   0,   0),
    ("Rosso",       0, 255, 255),
    ("Verde",     255,   0, 255),
    ("Blu",       255, 255,   0),
    ("Giallo",      0,   0, 255),
    ("Ciano",     255,   0,   0),
    ("Magenta",     0, 255,   0),
    ("Arancio",     0, 130, 255),
    ("Rosa",        0, 200,  50),
    ("Lavanda",   100, 200,   0),
    ("Gold",        0,  50, 255),
    ("Acquamarina",200,   0, 100),
    ("Viola",     150, 255,   0),
    ("Ambra",       0,  80, 255),
    ("Corallo",     0, 180, 180),
    ("Teal",      200,   0, 100),
    ("Indaco",    200, 200,   0),
    ("Rosso Scuro",  0, 255, 200),
    ("Blu Notte", 200, 200,  50),
    ("Bianco Caldo",  0,  40, 100),
    ("Bianco Freddo", 80,  20,   0),
]


# ─── Palette colori RGB — versione inglese ────────────────────────────────────
RGB_PALETTE_EN = [
    # Whites
    ("White",            255, 255, 255),
    ("Warm White",       255, 200, 100),
    ("Cool White",       200, 220, 255),
    # Primary
    ("Red",              255,   0,   0),
    ("Green",              0, 255,   0),
    ("Blue",               0,   0, 255),
    # Secondary
    ("Yellow",           255, 255,   0),
    ("Cyan",               0, 255, 255),
    ("Magenta",          255,   0, 255),
    # Tertiary
    ("Orange",           255, 128,   0),
    ("Pink",             255,  20, 147),
    ("Coral",            255,  80,  60),
    ("Lime",             128, 255,   0),
    ("Teal",               0, 200, 180),
    ("Lavender",         180, 100, 255),
    ("Indigo",            75,   0, 130),
    # Saturated
    ("Amber",            255, 160,   0),
    ("Violet",           148,   0, 211),
    ("Gold",             255, 200,   0),
    ("Aquamarine",        50, 255, 200),
    # Dark / theatrical
    ("Dark Red",         180,   0,   0),
    ("Midnight Blue",      0,   0, 160),
    ("Forest Green",       0, 100,   0),
    ("Crimson",          180,   0,  50),
    ("Royal Blue",         0,  80, 255),
    # Pastels
    ("Pastel Pink",      255, 182, 193),
    ("Baby Blue",        173, 216, 230),
    ("Mint",             152, 255, 152),
    ("Pastel Lilac",     221, 160, 221),
    ("Peach",            255, 218, 185),
    ("Pastel Yellow",    255, 255, 153),
    # Fire / ice
    ("Fire",             255,  60,   0),
    ("Ice",              150, 220, 255),
    ("Ember",            255,  30,   0),
    # Party / UV Simulation
    ("UV Sim",            80,   0, 200),
    ("Strobe White",     255, 255, 255),
]

# ─── Palette colori CMY — versione inglese ────────────────────────────────────
CMY_PALETTE_EN = [
    ("White",       0,   0,   0),
    ("Red",         0, 255, 255),
    ("Green",     255,   0, 255),
    ("Blue",      255, 255,   0),
    ("Yellow",      0,   0, 255),
    ("Cyan",      255,   0,   0),
    ("Magenta",     0, 255,   0),
    ("Orange",      0, 130, 255),
    ("Pink",        0, 200,  50),
    ("Lavender",  100, 200,   0),
    ("Gold",        0,  50, 255),
    ("Aquamarine",200,   0, 100),
    ("Violet",    150, 255,   0),
    ("Amber",       0,  80, 255),
    ("Coral",       0, 180, 180),
    ("Teal",      200,   0, 100),
    ("Indigo",    200, 200,   0),
    ("Dark Red",    0, 255, 200),
    ("Midnight Blue", 200, 200, 50),
    ("Warm White",  0,  40, 100),
    ("Cool White", 80,  20,   0),
]

# ─── Seleziona la palette corrente in base alla lingua ────────────────────────
RGB_PALETTE_IT = RGB_PALETTE  # salva riferimento all'originale IT
CMY_PALETTE_IT = CMY_PALETTE  # salva riferimento all'originale IT

# ─── Posizioni Moving Head / Moving Head positions ──────────────────────────────
# (nome/name, pan_byte, tilt_byte) — 0-255, 127=center/centro
MOVING_POSITIONS = [
    # Solo Pan / Pan only
    ("Pan Far Left",     0,   None),
    ("Pan Left",        64,   None),
    ("Pan Center",     127,   None),
    ("Pan Right",      192,   None),
    ("Pan Far Right",  255,   None),
    # Solo Tilt / Tilt only
    ("Tilt Down",      None,    0),
    ("Tilt Low",       None,   64),
    ("Tilt Center",    None,  127),
    ("Tilt High",      None,  192),
    ("Tilt Up",        None,  255),
    # Posizioni palco combinate / Combined stage positions
    ("PT Home",          0,    0),
    ("PT Center",      127,  127),
    # Downstage (verso il pubblico / towards audience)
    ("DS Center",      127,   64),
    ("DS Stage Left",   64,   64),
    ("DS Stage Right", 192,   64),
    # Upstage (verso il fondo / towards backdrop)
    ("US Center",      127,  192),
    ("US Stage Left",   64,  192),
    ("US Stage Right", 192,  192),
    # Orientamenti wash / Wash orientations
    ("Front Wash",     127,   48),
    ("Back Wash",      127,  210),
    ("Side Left",       32,  127),
    ("Side Right",     224,  127),
    # Angoli e speciali / Angles and specials
    ("PT Upstage SX",   48,  200),
    ("PT Upstage DX",  210,  200),
    ("PT Audience",    127,   20),
    ("PT Balcony",     127,   10),
    ("PT Floor",       127,  245),
    ("PT Hard Left",     8,  127),
    ("PT Hard Right",  248,  127),
]

# ─── Livelli dimmer / Dimmer levels ─────────────────────────────────────────────
DIMMER_LEVELS = [
    ("Zero",   0),
    ("10%",   25),
    ("25%",   63),
    ("50%",  127),
    ("75%",  191),
    ("Full", 255),
]

# ─── Zoom presets / Zoom position presets ───────────────────────────────────────
ZOOM_PRESETS_IT = [
    ("Zoom Stretto",    5),
    ("Zoom Medio",    127),
    ("Zoom Largo",    250),
]
# Liste mutabili (aggiornate da _init_lang())
ZOOM_PRESETS = list(ZOOM_PRESETS_IT)

IRIS_PRESETS_IT = [
    ("Iris Aperto",    0),
    ("Iris Metà",    127),
    ("Iris Chiuso",  255),
]
IRIS_PRESETS = list(IRIS_PRESETS_IT)

FOCUS_PRESETS = [
    ("Focus Near",    0),
    ("Focus Mid",   127),
    ("Focus Far",   255),
]


# ══════════════════════════════════════════════════════════════════════════════
# Utilità XML / XML utilities
# ══════════════════════════════════════════════════════════════════════════════

def safe_xml_parse(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    clean = [l for l in lines if not l.strip().startswith("<!DOCTYPE")]
    xml_str = "".join(clean)
    try:
        return ET.fromstring(xml_str)
    except ET.ParseError:
        return ET.parse(path).getroot()


def strip_ns(elem):
    root = elem.getroot() if hasattr(elem, "getroot") else elem
    for el in root.iter():
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
        keys_to_fix = [k for k in el.attrib if "}" in k]
        for k in keys_to_fix:
            el.attrib[k.split("}", 1)[1]] = el.attrib.pop(k)
    return root


def indent_xml(elem, level=0):
    pad = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = pad + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = pad
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = pad
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = pad
    if not level:
        elem.tail = "\n"


# ══════════════════════════════════════════════════════════════════════════════
# Caricamento / Parsing fixture .qxf
# Loading and parsing QLC+ fixture definition files
# ══════════════════════════════════════════════════════════════════════════════

def find_fixture_dirs(extra=None):
    dirs = list(FIXTURE_SEARCH_PATHS)
    if extra:
        dirs.insert(0, extra)
    return [d for d in dirs if os.path.isdir(d)]


def load_fixture_definition(manufacturer, model, fixture_dirs):
    candidates = []
    for base in fixture_dirs:
        mfr_dir = os.path.join(base, manufacturer)
        candidates += [
            os.path.join(mfr_dir, f"{manufacturer}-{model}.qxf"),
            os.path.join(base,    f"{manufacturer}-{model}.qxf"),
            os.path.join(mfr_dir, f"{model}.qxf"),
        ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                return strip_ns(safe_xml_parse(path))
            except ET.ParseError as e:
                print(f"  [WARN] Parsing error {path}: {e}")
    return None


def parse_qxf_mode(qxf_root, mode_name):
    channels_by_name = {}
    for ch in qxf_root.findall("Channel"):
        ch_name = ch.get("Name", "")
        group_el = ch.find("Group")
        group = (group_el.text or "Nothing").strip() if group_el is not None else "Nothing"
        byte_val = int(group_el.get("Byte", "0")) if group_el is not None else 0

        preset = ch.get("Preset", "")
        if preset == "PositionPan" or preset == "PositionPanFine":
            group = G_PAN
        elif preset == "PositionTilt" or preset == "PositionTiltFine":
            group = G_TILT
        elif preset == "IntensityDimmer":
            group = G_INTENSITY
        elif preset == "ColorMacro" or preset == "ColorDoubleMacro":
            group = G_COLOUR
        elif preset == "GoboMacro" or preset == "GoboShakeMacro":
            group = G_GOBO
        elif preset == "ShutterClose" or preset == "ShutterOpen" or preset == "StrobeSlowToFast":
            group = G_SHUTTER

        caps = []
        for cap in ch.findall("Capability"):
            try:
                caps.append((
                    int(cap.get("Min", 0)),
                    int(cap.get("Max", 255)),
                    (cap.text or "").strip()
                ))
            except ValueError:
                pass
        channels_by_name[ch_name] = {
            "name": ch_name, "group": group,
            "byte": byte_val, "capabilities": caps
        }

    mode_el = None
    for m in qxf_root.findall("Mode"):
        if m.get("Name", "") == mode_name:
            mode_el = m
            break
    if mode_el is None:
        mode_el = qxf_root.find("Mode")
    if mode_el is None:
        return {}

    result = {}
    for ch_ref in mode_el.findall("Channel"):
        num = int(ch_ref.get("Number", -1))
        name = (ch_ref.text or "").strip()
        if num >= 0 and name in channels_by_name:
            result[num] = channels_by_name[name]
    return result


# ══════════════════════════════════════════════════════════════════════════════
# Parsing .qxw — lettura progetto QLC+ / Reading the QLC+ project file
# ══════════════════════════════════════════════════════════════════════════════

def parse_qxw_fixtures(qxw_root):
    fixtures = []
    _eng = qxw_root.find("Engine"); engine = _eng if _eng is not None else qxw_root
    for fix in engine.findall("Fixture"):
        try:
            def get_value(elem, name, default=None):
                val = elem.get(name)
                if val is not None:
                    return val
                child = elem.find(name)
                if child is not None and child.text:
                    return child.text
                for child in elem:
                    if child.tag.lower() == name.lower():
                        return child.text
                return default

            fix_id = get_value(fix, "ID")
            if fix_id is None:
                continue

            fix_id = int(fix_id)
            name = get_value(fix, "n") or get_value(fix, "Name") or "Unknown"

            fixtures.append({
                "id":           fix_id,
                "name":         name,
                "manufacturer": get_value(fix, "Manufacturer", ""),
                "model":        get_value(fix, "Model", ""),
                "mode":         get_value(fix, "Mode", ""),
                "universe":     int(get_value(fix, "Universe", "0")),
                "address":      int(get_value(fix, "Address", "0")),
                "channels":     int(get_value(fix, "Channels", "1")),
            })
        except (ValueError, TypeError) as e:
            print(f"  [WARN] Fixture ignorata: {e}")
    return fixtures


def get_next_function_id(qxw_root):
    _eng = qxw_root.find("Engine"); engine = _eng if _eng is not None else qxw_root
    max_id = -1
    for fn in engine.findall("Function"):
        try:
            fid = int(fn.get("ID", -1))
            if fid > max_id:
                max_id = fid
        except ValueError:
            pass
    return max_id + 1


# ══════════════════════════════════════════════════════════════════════════════
# Costruzione elemento XML <Function> Scene / Building XML <Function> Scene element
# ══════════════════════════════════════════════════════════════════════════════


def _init_lang():
    """Reinizializza tutte le costanti dipendenti dalla lingua.
    Va chiamata DOPO aver impostato LANG e PRIMA di generate_palettes().
    """
    global RGB_PALETTE, CMY_PALETTE, ZOOM_PRESETS, IRIS_PRESETS
    global EFX_SIZES, EFX_SPEEDS, EFX_SPEEDS_SHORT, EFX_GROUP_SPEEDS
    global CHASER_SPEEDS, CHASER_FLASH_SPEEDS, CHASER_COLOR_SPEEDS
    global RGB_NAMES_FULL, RGB_NAMES_PASTELLI, RGB_NAMES_CALDI, RGB_NAMES_FREDDI
    global RGB_NAMES_CLUB, RGB_NAMES_DISCOTECA, RGB_NAMES_TEATRALI
    global RGB_NAMES_PRIMARI, RGB_NAMES_SECONDARI, RGB_NAMES_ARCOBALENO
    global BICOLORI, TRICOLORI

    # Palette colori
    if LANG == "en":
        RGB_PALETTE[:] = RGB_PALETTE_EN
        CMY_PALETTE[:] = CMY_PALETTE_EN
    else:
        RGB_PALETTE[:] = RGB_PALETTE_IT
        CMY_PALETTE[:] = CMY_PALETTE_IT

    # Presets Zoom / Iris (usano T())
    ZOOM_PRESETS[:] = [(T("Zoom Stretto"), 5), (T("Zoom Medio"), 127), (T("Zoom Largo"), 250)]
    IRIS_PRESETS[:] = [(T("Iris Aperto"), 0), (T("Iris Metà"), 127), (T("Iris Chiuso"), 255)]

    # EFX sizes / speeds
    EFX_SIZES[:]       = _EFX_SIZES()
    EFX_SPEEDS[:]      = _EFX_SPEEDS()
    EFX_SPEEDS_SHORT[:]= _EFX_SPEEDS_SHORT()
    EFX_GROUP_SPEEDS[:]= _EFX_GROUP_SPEEDS()

    # Chaser speeds
    CHASER_SPEEDS[:]      = _CHASER_SPEEDS()
    CHASER_FLASH_SPEEDS[:]= _CHASER_FLASH_SPEEDS()
    CHASER_COLOR_SPEEDS[:]= CHASER_SPEEDS[:5]

    # Ricava i nomi dalla palette selezionata
    _names = {r: r for (r, *_) in RGB_PALETTE}
    def _c(it_name):
        """Restituisce il nome tradotto del colore dato il nome italiano."""
        return T(it_name)

    RGB_NAMES_FULL[:]       = [n for (n, r, g, b) in RGB_PALETTE]
    RGB_NAMES_PASTELLI[:]   = [n for (n, r, g, b) in RGB_PALETTE
                                if any(x in n for x in ("Pastel", "Pastello"))]
    RGB_NAMES_CALDI[:]      = [_c(n) for n in ["Rosso","Arancio","Ambra","Gold","Giallo",
                                "Corallo","Fuoco","Brace","Bianco Caldo","Rosso Scuro","Cremisi"]
                               if _c(n) in _names]
    RGB_NAMES_FREDDI[:]     = [_c(n) for n in ["Blu","Ciano","Teal","Acquamarina","Lavanda",
                                "Indaco","Blu Notte","Azzurro Reale","Ghiaccio","Bianco Freddo",
                                "Pastello Azzurro","Pastello Menta"]
                               if _c(n) in _names]
    RGB_NAMES_CLUB[:]       = [_c(n) for n in ["Rosso","Verde","Blu","Bianco"] if _c(n) in _names]
    RGB_NAMES_DISCOTECA[:]  = [_c(n) for n in ["Rosso","Verde","Blu","Giallo","Ciano","Magenta",
                                "Arancio","Rosa","Viola","Ambra"]
                               if _c(n) in _names]
    RGB_NAMES_TEATRALI[:]   = [_c(n) for n in ["Rosso Scuro","Blu Notte","Verde Bosco","Ambra",
                                "Viola","Cremisi","Gold","Bianco Caldo"]
                               if _c(n) in _names]
    RGB_NAMES_PRIMARI[:]    = [_c(n) for n in ["Rosso","Verde","Blu"] if _c(n) in _names]
    RGB_NAMES_SECONDARI[:]  = [_c(n) for n in ["Giallo","Ciano","Magenta"] if _c(n) in _names]
    RGB_NAMES_ARCOBALENO[:] = [_c(n) for n in ["Rosso","Arancio","Giallo","Verde","Ciano",
                                "Blu","Indaco","Viola","Magenta"]
                               if _c(n) in _names]

    BICOLORI[:] = [
        (_c("Rosso") + "-" + _c("Blu"),     _c("Rosso"), _c("Blu")),
        (_c("Rosso") + "-" + _c("Bianco"),  _c("Rosso"), _c("Bianco")),
        (_c("Blu")   + "-" + _c("Bianco"),  _c("Blu"),   _c("Bianco")),
        (_c("Giallo")+ "-" + _c("Blu"),     _c("Giallo"),_c("Blu")),
        ("Verde-Magenta" if LANG=="it" else "Green-Magenta", _c("Verde"), _c("Magenta")),
        (_c("Arancio")+ "-" + _c("Blu"),    _c("Arancio"),_c("Blu")),
        (_c("Rosso")  + "-" + _c("Verde"),  _c("Rosso"), _c("Verde")),
        (_c("Ciano")  + "-" + _c("Rosso"),  _c("Ciano"), _c("Rosso")),
        (_c("Giallo") + "-" + _c("Viola"),  _c("Giallo"),_c("Viola")),
        (_c("Ambra")  + "-" + _c("Blu"),    _c("Ambra"), _c("Blu")),
        (_c("Bianco") + "-" + _c("Viola"),  _c("Bianco"),_c("Viola")),
        ("Fuoco-Ghiaccio" if LANG=="it" else "Fire-Ice",     _c("Fuoco") if LANG=="it" else _c("Fuoco"), _c("Ghiaccio") if LANG=="it" else _c("Ghiaccio")),
    ]
    # Fix Fire/Ice names in EN
    if LANG == "en":
        BICOLORI[-1] = ("Fire-Ice", _c("Fuoco"), _c("Ghiaccio"))
        BICOLORI[4]  = ("Green-Magenta", _c("Verde"), _c("Magenta"))

    TRICOLORI[:] = [
        ("IT" if LANG=="it" else "IT",      _c("Bianco"), _c("Rosso"),   _c("Verde")),
        ("RGB",                              _c("Rosso"),  _c("Verde"),   _c("Blu")),
        ("CMY",                              _c("Ciano"),  _c("Magenta"), _c("Giallo")),
        ("Fuoco" if LANG=="it" else "Fire",  _c("Rosso"),  _c("Arancio"), _c("Giallo")),
        ("Party",                            _c("Rosso"),  _c("Blu"),     _c("Giallo")),
        ("Alpin",                            _c("Rosso"),  _c("Bianco"),  _c("Blu")),
    ]


def make_scene(fn_id, name, channel_values, path="Auto Palette",
               fade_in=0, fade_out=2000):
    fn = ET.Element("Function")
    fn.set("ID", str(fn_id))
    fn.set("Type", "Scene")
    fn.set("Name", name)
    fn.set("Path", path)

    speed = ET.SubElement(fn, "Speed")
    speed.set("FadeIn",   str(fade_in))
    speed.set("FadeOut",  str(fade_out))
    speed.set("Duration", "0")

    for (fix_id, ch_num, val) in channel_values:
        fixture_val = ET.SubElement(fn, "FixtureVal")
        fixture_val.set("ID", str(fix_id))
        fixture_val.text = f"{ch_num},{int(max(0, min(255, val)))}"

    return fn


# ══════════════════════════════════════════════════════════════════════════════
# Utilità capability / Capability helper functions
# ══════════════════════════════════════════════════════════════════════════════

def cap_find(caps, *keywords, strategy="first"):
    kws = [k.lower() for k in keywords]
    for (cmin, cmax, cname) in caps:
        cname_l = cname.lower()
        if any(k in cname_l for k in kws):
            val = cmin if strategy == "first" else (cmin + cmax) // 2
            return val, cname
    return None, None


def cap_first(caps):
    return caps[0][0] if caps else 0


def cap_all_positions(caps, skip_keywords=None):
    skip = [k.lower() for k in (skip_keywords or [])]
    result = []
    for (cmin, cmax, cname) in caps:
        if any(s in cname.lower() for s in skip):
            continue
        mid = (cmin + cmax) // 2
        result.append((mid, cname))
    return result


def strobe_values(caps):
    strobe_ranges = [
        (cmin, cmax, cname) for (cmin, cmax, cname) in caps
        if any(k in cname.lower() for k in ["strobe", "stroboscop", "flash"])
        and (cmax - cmin) > 5
    ]
    result = {}
    if strobe_ranges:
        cmin, cmax, _ = strobe_ranges[0]
        span = cmax - cmin
        result["slow"]  = cmin + span // 6
        result["med"]   = cmin + span // 2
        result["fast"]  = cmin + span * 5 // 6
    return result


# ══════════════════════════════════════════════════════════════════════════════
# Categorizzazione canali / Fixture channel categorisation
# ══════════════════════════════════════════════════════════════════════════════

class FixtureChannels:
    def __init__(self, ch_map):
        self.raw = ch_map
        self.by_group = defaultdict(dict)
        for ch_num, info in ch_map.items():
            self.by_group[info["group"]][ch_num] = info

    def get(self, *groups):
        result = {}
        for g in groups:
            for ch_num, info in self.by_group.get(g, {}).items():
                if info["byte"] == 0:
                    result[ch_num] = info
        return result

    def get_fine(self, *groups):
        result = {}
        for g in groups:
            for ch_num, info in self.by_group.get(g, {}).items():
                if info["byte"] == 1:
                    result[ch_num] = info
        return result

    def has(self, *groups):
        return any(bool(self.by_group.get(g)) for g in groups)

    @property
    def has_rgb(self):
        return (self.has(G_RED) and self.has(G_GREEN) and self.has(G_BLUE))

    @property
    def has_cmy(self):
        return (self.has(G_CYAN) and self.has(G_MAGENTA) and self.has(G_YELLOW))

    @property
    def has_moving(self):
        if self.has(G_PAN) and self.has(G_TILT):
            return True
        return False

    def has_enough_channels_for_moving(self, min_channels=4):
        return len(self.raw) >= min_channels

    @property
    def has_dimmer(self):
        return self.has(G_INTENSITY)

    @property
    def has_white(self):
        return self.has(G_WHITE)

    @property
    def has_amber(self):
        return self.has(G_AMBER)

    @property
    def has_uv(self):
        return self.has(G_UV)


# ══════════════════════════════════════════════════════════════════════════════
# Generatori di scene per categoria / Scene generators by category
# ══════════════════════════════════════════════════════════════════════════════

def scenes_dimmer(fid, prefix, fc, path):
    scenes = []
    dimmers = fc.get(G_INTENSITY)
    if not dimmers:
        return scenes

    for lname, lval in DIMMER_LEVELS:
        scenes.append((
            f"{prefix} » Dimmer {lname}", path,
            [(fid, ch, lval) for ch in dimmers]
        ))

    shutters = fc.get(G_SHUTTER)
    if shutters:
        for ch_num, info in shutters.items():
            caps = info["capabilities"]
            open_v,  _ = cap_find(caps, "open", "lamp on", "aperto", "on")
            close_v, _ = cap_find(caps, "closed", "closed", "chiuso", "blackout", "off")
            strobe     = strobe_values(caps)

            if open_v is not None:
                scenes.append((
                    f"{prefix} » {T('Shutter Aperto')}", path,
                    [(fid, ch_num, open_v)]
                ))
            if close_v is not None:
                scenes.append((
                    f"{prefix} » {T('Shutter Chiuso')}", path,
                    [(fid, ch_num, close_v)]
                ))
            for label, key in [("Strobe Slow", "slow"), ("Strobe Med", "med"), ("Strobe Fast", "fast")]:
                if key in strobe:
                    scenes.append((
                        f"{prefix} » {label}", path,
                        [(fid, ch_num, strobe[key])]
                    ))
            break

    return scenes


def scenes_rgb(fid, prefix, fc, path):
    scenes = []
    reds   = fc.get(G_RED)
    greens = fc.get(G_GREEN)
    blues  = fc.get(G_BLUE)
    whites = fc.get(G_WHITE)
    ambers = fc.get(G_AMBER)
    uvs    = fc.get(G_UV)

    if not (reds and greens and blues):
        return scenes

    for color_name, r, g, b in RGB_PALETTE:
        vals = (
            [(fid, ch, r) for ch in reds]
          + [(fid, ch, g) for ch in greens]
          + [(fid, ch, b) for ch in blues]
        )
        if whites:
            w = 255 if (r == g == b == 255) else (
                80 if color_name in (T("Bianco Caldo"), T("Bianco Freddo")) else 0
            )
            vals += [(fid, ch, w) for ch in whites]
        if ambers:
            a = 200 if T("Ambra") in color_name or "Caldo" in color_name else (
                100 if color_name == "Gold" else 0  # Gold is invariant
            )
            vals += [(fid, ch, a) for ch in ambers]
        if uvs:
            uv = 255 if "UV" in color_name else 0
            vals += [(fid, ch, uv) for ch in uvs]

        scenes.append((f"{prefix} » {color_name}", path, vals))

    if whites:
        scenes.append((
            f"{prefix} » {T('White Puro (W)')}", path,
            [(fid, ch, 0)   for ch in reds]
          + [(fid, ch, 0)   for ch in greens]
          + [(fid, ch, 0)   for ch in blues]
          + [(fid, ch, 255) for ch in whites]
        ))
        scenes.append((
            f"{prefix} » {T('White Misto (RGB+W)')}", path,
            [(fid, ch, 200) for ch in reds]
          + [(fid, ch, 200) for ch in greens]
          + [(fid, ch, 200) for ch in blues]
          + [(fid, ch, 255) for ch in whites]
        ))
        for lname, lval in [("W 25%", 63), ("W 50%", 127), ("W 75%", 191), ("W Full", 255)]:
            scenes.append((
                f"{prefix} » White Ch {lname}", path,
                [(fid, ch, 0)    for ch in reds]
              + [(fid, ch, 0)    for ch in greens]
              + [(fid, ch, 0)    for ch in blues]
              + [(fid, ch, lval) for ch in whites]
            ))

    return scenes


def scenes_cmy(fid, prefix, fc, path):
    scenes = []
    cyans    = fc.get(G_CYAN)
    magentas = fc.get(G_MAGENTA)
    yellows  = fc.get(G_YELLOW)
    if not (cyans and magentas and yellows):
        return scenes

    for color_name, c, m, y in CMY_PALETTE:
        vals = (
            [(fid, ch, c) for ch in cyans]
          + [(fid, ch, m) for ch in magentas]
          + [(fid, ch, y) for ch in yellows]
        )
        scenes.append((f"{prefix} » CMY {color_name}", path, vals))

    scenes.append((f"{prefix} » CMY Cyan Full",    path, [(fid, ch, 255) for ch in cyans]))
    scenes.append((f"{prefix} » CMY Magenta Full", path, [(fid, ch, 255) for ch in magentas]))
    scenes.append((f"{prefix} » CMY Yellow Full",  path, [(fid, ch, 255) for ch in yellows]))

    return scenes


def scenes_white_standalone(fid, prefix, fc, path):
    scenes = []
    whites = fc.get(G_WHITE)
    if not whites or fc.has_rgb:
        return scenes
    for lname, lval in DIMMER_LEVELS:
        scenes.append((
            f"{prefix} » White {lname}", path,
            [(fid, ch, lval) for ch in whites]
        ))
    return scenes


def scenes_amber_standalone(fid, prefix, fc, path):
    scenes = []
    ambers = fc.get(G_AMBER)
    if not ambers:
        return scenes
    for lname, lval in DIMMER_LEVELS:
        scenes.append((
            f"{prefix} » Amber {lname}", path,
            [(fid, ch, lval) for ch in ambers]
        ))
    return scenes


def scenes_uv(fid, prefix, fc, path):
    scenes = []
    uvs = fc.get(G_UV)
    if not uvs:
        return scenes
    for lname, lval in [("Zero", 0), ("25%", 63), ("50%", 127), ("75%", 191), ("Full", 255)]:
        scenes.append((
            f"{prefix} » UV {lname}", path,
            [(fid, ch, lval) for ch in uvs]
        ))
    blues = fc.get(G_BLUE)
    if blues:
        scenes.append((
            f"{prefix} » UV + Blu", path,
            [(fid, ch, 255) for ch in uvs]
          + [(fid, ch, 100) for ch in blues]
        ))
    return scenes


def scenes_color_wheel(fid, prefix, fc, path, min_cap_scenes=2):
    scenes = []
    colours = fc.get(G_COLOUR)
    if not colours:
        return scenes

    for ch_num, info in colours.items():
        caps = info["capabilities"]
        if len(caps) < min_cap_scenes:
            continue
        skip = ["rotation", "rotate", "scroll", "speed", "rotaz"]
        for mid_val, cname in cap_all_positions(caps, skip_keywords=skip):
            label = cname if cname else f"Pos {mid_val}"
            scenes.append((
                f"{prefix} » Color {label}", path,
                [(fid, ch_num, mid_val)]
            ))
    return scenes


def scenes_gobo(fid, prefix, fc, path, min_cap_scenes=2):
    scenes = []
    gobos = fc.get(G_GOBO)
    if not gobos:
        return scenes

    gobo_idx = 1
    for ch_num, info in sorted(gobos.items()):
        caps = info["capabilities"]
        if len(caps) < min_cap_scenes:
            continue
        ch_label = f"Gobo{gobo_idx}"
        gobo_idx += 1

        skip_rot = ["rotation", "rotate", "spin", "cw", "ccw", "rotaz"]
        fixed_caps = [(cmin, cmax, cname) for (cmin, cmax, cname) in caps
                      if not any(k in cname.lower() for k in skip_rot)]

        for mid_val, cname in cap_all_positions(fixed_caps):
            label = cname if cname else f"Pos {mid_val}"
            scenes.append((
                f"{prefix} » {ch_label} {label}", path,
                [(fid, ch_num, mid_val)]
            ))

    for ch_num, info in gobos.items():
        caps = info["capabilities"]
        rot_v, rot_n = cap_find(caps, "rotation", "rotate", "spin")
        stop_v, _ = cap_find(caps, "no rotation", "stop", "fermo", "indexed")
        cw_v,  _ = cap_find(caps, "cw", "clockwise")
        ccw_v, _ = cap_find(caps, "ccw", "counter")
        if rot_v is not None:
            if stop_v is not None:
                scenes.append((f"{prefix} » Gobo Rot Stop",  path, [(fid, ch_num, stop_v)]))
            if cw_v is not None:
                scenes.append((f"{prefix} » Gobo Rot CW",   path, [(fid, ch_num, cw_v)]))
            if ccw_v is not None:
                scenes.append((f"{prefix} » Gobo Rot CCW",  path, [(fid, ch_num, ccw_v)]))
            rot_ranges = [(cmin, cmax, cname) for (cmin, cmax, cname) in caps
                          if any(k in cname.lower() for k in ["cw", "clockwise"])
                          and (cmax - cmin) > 5]
            if rot_ranges:
                cmin, cmax, _ = rot_ranges[0]
                scenes.append((f"{prefix} » Gobo Rot CW Slow",  path, [(fid, ch_num, cmin + 10)]))
                scenes.append((f"{prefix} » Gobo Rot CW Fast",  path, [(fid, ch_num, cmax - 10)]))

    return scenes


def scenes_prism(fid, prefix, fc, path):
    scenes = []
    prisms = fc.get(G_PRISM)
    if not prisms:
        return scenes
    for ch_num, info in prisms.items():
        caps = info["capabilities"]
        on_v,  _ = cap_find(caps, "prism", "on", "attivato", "in")
        off_v, _ = cap_find(caps, "open", "off", "no prism", "spento")
        rot_v, _ = cap_find(caps, "rotation", "rotate")
        if off_v is not None:
            scenes.append((f"{prefix} » Prism Off",  path, [(fid, ch_num, off_v)]))
        if on_v is not None:
            scenes.append((f"{prefix} » Prism On",   path, [(fid, ch_num, on_v)]))
        if rot_v is not None:
            scenes.append((f"{prefix} » Prism Rot",  path, [(fid, ch_num, rot_v)]))
        for mid_val, cname in cap_all_positions(caps):
            label = cname if cname else f"Pos {mid_val}"
            scenes.append((f"{prefix} » Prism {label}", path, [(fid, ch_num, mid_val)]))
        break
    return scenes


def scenes_zoom(fid, prefix, fc, path):
    scenes = []
    zooms = fc.get(G_ZOOM)
    if not zooms:
        return scenes
    for ch_num, info in zooms.items():
        caps = info["capabilities"]
        narrow_kw = ["narrow", "small", "stretto", "spot"]
        wide_kw   = ["wide", "largo", "beam", "wash"]
        narrow_v, _ = cap_find(caps, *narrow_kw)
        wide_v,   _ = cap_find(caps, *wide_kw)

        if caps:
            first_name = caps[0][2].lower()
            if any(k in first_name for k in wide_kw):
                narrow_v = 255 if narrow_v is None else narrow_v
                wide_v   = 0   if wide_v   is None else wide_v
            else:
                narrow_v = 0   if narrow_v is None else narrow_v
                wide_v   = 255 if wide_v   is None else wide_v

        scenes.append((f"{prefix} » {T('Zoom Stretto')}", path, [(fid, ch_num, narrow_v)]))
        scenes.append((f"{prefix} » {T('Zoom Medio')}",   path, [(fid, ch_num, 127)]))
        scenes.append((f"{prefix} » {T('Zoom Largo')}",   path, [(fid, ch_num, wide_v)]))
        break
    return scenes


def scenes_iris(fid, prefix, fc, path):
    scenes = []
    irises = fc.get(G_IRIS)
    if not irises:
        return scenes
    for ch_num, info in irises.items():
        caps = info["capabilities"]
        open_v,  _ = cap_find(caps, "open", "aperto", "max")
        close_v, _ = cap_find(caps, "closed", "close", "chiuso", "min", "small")
        scenes.append((f"{prefix} » {T('Iris Aperto')}", path, [(fid, ch_num, open_v  or 0)]))
        scenes.append((f"{prefix} » {T('Iris Metà')}",   path, [(fid, ch_num, 127)]))
        scenes.append((f"{prefix} » {T('Iris Chiuso')}", path, [(fid, ch_num, close_v or 255)]))
        break
    return scenes


def scenes_focus(fid, prefix, fc, path):
    scenes = []
    focuses = fc.get(G_FOCUS)
    if not focuses:
        return scenes
    for ch_num, info in focuses.items():
        scenes.append((f"{prefix} » Focus Near", path, [(fid, ch_num, 0)]))
        scenes.append((f"{prefix} » Focus Mid",  path, [(fid, ch_num, 127)]))
        scenes.append((f"{prefix} » Focus Far",  path, [(fid, ch_num, 255)]))
        break
    return scenes


def scenes_frost(fid, prefix, fc, path):
    scenes = []
    beams = fc.get(G_FROST)
    if not beams:
        return scenes
    for ch_num, info in beams.items():
        caps = info["capabilities"]
        on_v,  _ = cap_find(caps, "frost", "diffusion", "soft")
        off_v, _ = cap_find(caps, "open", "clear", "off", "no frost")
        if off_v is not None:
            scenes.append((f"{prefix} » Frost Off", path, [(fid, ch_num, off_v)]))
        if on_v is not None:
            scenes.append((f"{prefix} » Frost On",  path, [(fid, ch_num, on_v)]))
        scenes.append((f"{prefix} » Frost 50%",     path, [(fid, ch_num, 127)]))
        break
    return scenes


def scenes_speed(fid, prefix, fc, path):
    scenes = []
    speeds = fc.get(G_SPEED)
    if not speeds:
        return scenes
    for ch_num, info in speeds.items():
        caps = info["capabilities"]
        stop_v, _ = cap_find(caps, "stop", "fermo", "no", "0")
        slow_v, _ = cap_find(caps, "slow", "lento")
        fast_v, _ = cap_find(caps, "fast", "veloce")
        if stop_v is not None:
            scenes.append((f"{prefix} » Speed Stop",   path, [(fid, ch_num, stop_v)]))
        scenes.append((f"{prefix} » Speed Slow",       path, [(fid, ch_num, slow_v or 64)]))
        scenes.append((f"{prefix} » Speed Medium",     path, [(fid, ch_num, 127)]))
        scenes.append((f"{prefix} » Speed Fast",       path, [(fid, ch_num, fast_v or 220)]))
        break
    return scenes


def scenes_effect(fid, prefix, fc, path, min_cap_scenes=2):
    scenes = []
    for g in [G_EFFECT, G_MACRO]:
        for ch_num, info in fc.get(g).items():
            caps = info["capabilities"]
            if len(caps) < min_cap_scenes:
                continue
            gname = info["group"]
            for mid_val, cname in cap_all_positions(caps):
                label = cname if cname else f"Pos {mid_val}"
                scenes.append((
                    f"{prefix} » {gname} {label}", path,
                    [(fid, ch_num, mid_val)]
                ))
    return scenes


def scenes_moving(fid, prefix, fc, path):
    scenes = []
    pans      = fc.get(G_PAN)
    pan_fines = fc.get_fine(G_PAN)
    tilts     = fc.get(G_TILT)
    tilt_fines= fc.get_fine(G_TILT)
    if not (pans and tilts):
        return scenes

    def pt_vals(pan_v, tilt_v):
        vals = []
        if pan_v is not None:
            vals += [(fid, ch, pan_v) for ch in pans]
            vals += [(fid, ch, 0)     for ch in pan_fines]
        if tilt_v is not None:
            vals += [(fid, ch, tilt_v) for ch in tilts]
            vals += [(fid, ch, 0)      for ch in tilt_fines]
        return vals

    for pos_name, pan_v, tilt_v in MOVING_POSITIONS:
        v = pt_vals(pan_v, tilt_v)
        if v:
            scenes.append((f"{prefix} » {pos_name}", path, v))

    return scenes


def scenes_combo(fid, prefix, fc, path):
    scenes = []
    dimmers  = fc.get(G_INTENSITY)
    shutters = fc.get(G_SHUTTER)
    reds     = fc.get(G_RED)
    greens   = fc.get(G_GREEN)
    blues    = fc.get(G_BLUE)
    whites   = fc.get(G_WHITE)
    pans     = fc.get(G_PAN)
    pan_fine = fc.get_fine(G_PAN)
    tilts    = fc.get(G_TILT)
    tilt_fine= fc.get_fine(G_TILT)
    gobos    = fc.get(G_GOBO)

    shutter_open = None
    for ch_num, info in shutters.items():
        v, _ = cap_find(info["capabilities"], "open", "on", "lamp on")
        if v is not None:
            shutter_open = (ch_num, v)
        break

    shutter_close = None
    for ch_num, info in shutters.items():
        v, _ = cap_find(info["capabilities"], "closed", "blackout", "off")
        if v is not None:
            shutter_close = (ch_num, v)
        break

    stage_vals = []
    if dimmers:
        stage_vals += [(fid, ch, 255) for ch in dimmers]
    if shutter_open:
        stage_vals.append((fid, shutter_open[0], shutter_open[1]))
    if reds and greens and blues:
        stage_vals += [(fid, ch, 255) for ch in reds]
        stage_vals += [(fid, ch, 255) for ch in greens]
        stage_vals += [(fid, ch, 255) for ch in blues]
    elif whites:
        stage_vals += [(fid, ch, 255) for ch in whites]
    if pans and tilts:
        stage_vals += [(fid, ch, 127) for ch in pans]
        stage_vals += [(fid, ch, 0)   for ch in pan_fine]
        stage_vals += [(fid, ch, 127) for ch in tilts]
        stage_vals += [(fid, ch, 0)   for ch in tilt_fine]
    if stage_vals:
        scenes.append((f"{prefix} » [COMBO] Stage Ready", path, stage_vals))

    blackout_vals = []
    if dimmers:
        blackout_vals += [(fid, ch, 0) for ch in dimmers]
    if shutter_close:
        blackout_vals.append((fid, shutter_close[0], shutter_close[1]))
    if blackout_vals:
        scenes.append((f"{prefix} » [COMBO] {T('Blackout Totale')}", path, blackout_vals))

    full_vals = []
    if dimmers:
        full_vals += [(fid, ch, 255) for ch in dimmers]
    if shutter_open:
        full_vals.append((fid, shutter_open[0], shutter_open[1]))
    if reds and greens and blues:
        full_vals += [(fid, ch, 255) for ch in reds]
        full_vals += [(fid, ch, 255) for ch in greens]
        full_vals += [(fid, ch, 255) for ch in blues]
    elif whites:
        full_vals += [(fid, ch, 255) for ch in whites]
    if gobos:
        for ch_num, info in gobos.items():
            caps = info["capabilities"]
            open_v, _ = cap_find(caps, "open", "bianco", "white", "no gobo")
            if open_v is not None:
                full_vals.append((fid, ch_num, open_v))
            break
    if len(full_vals) > (len(dimmers) + (1 if shutter_open else 0)):
        scenes.append((f"{prefix} » [COMBO] Full Show", path, full_vals))

    if reds and greens and blues and dimmers:
        for cn_key, r, g, b in [("Rosso Puro", 255, 0, 0), ("Bianco Puro", 255, 255, 255), ("Blu Puro", 0, 0, 255)]:
            cn = T(cn_key)
            solo = (
                [(fid, ch, 255) for ch in dimmers]
              + ([(fid, shutter_open[0], shutter_open[1])] if shutter_open else [])
              + [(fid, ch, r) for ch in reds]
              + [(fid, ch, g) for ch in greens]
              + [(fid, ch, b) for ch in blues]
            )
            scenes.append((f"{prefix} » [COMBO] {cn}", path, solo))

    return scenes


# ══════════════════════════════════════════════════════════════════════════════
# EFX — Effetti di movimento / Movement effects
# ══════════════════════════════════════════════════════════════════════════════

def _EFX_SIZES():
    return [(T("Piccolo"), 60, 60), (T("Medio"), 127, 127), (T("Grande"), 200, 200)]
EFX_SIZES = _EFX_SIZES()

def _EFX_SPEEDS():
    return [(T("Molto Lento"),20000),(T("Lento"),12000),(T("Medio"),6000),(T("Veloce"),3000),(T("Velocissimo"),1500)]
EFX_SPEEDS = _EFX_SPEEDS()

def _EFX_SPEEDS_SHORT():
    return [(T("Lento"),12000),(T("Medio"),6000),(T("Veloce"),3000)]
EFX_SPEEDS_SHORT = _EFX_SPEEDS_SHORT()


def make_efx(fn_id, name, path,
             algorithm,
             width=127, height=127,
             rotation=0,
             duration=6000,
             direction="Forward",
             run_order="Loop",
             start_offset=0,
             is_relative=0,
             x_offset=127, x_freq=1, x_phase=0,
             y_offset=127, y_freq=1, y_phase=90,
             fixture_entries=None):
    fn = ET.Element("Function")
    fn.set("ID",   str(fn_id))
    fn.set("Type", "EFX")
    fn.set("Name", name)
    fn.set("Path", path)

    ET.SubElement(fn, "PropagationMode").text = "Parallel"

    speed = ET.SubElement(fn, "Speed")
    speed.set("FadeIn",   "0")
    speed.set("FadeOut",  "0")
    speed.set("Duration", str(duration))

    ET.SubElement(fn, "Direction").text  = direction
    ET.SubElement(fn, "RunOrder").text   = run_order
    ET.SubElement(fn, "Algorithm").text  = algorithm
    ET.SubElement(fn, "Width").text      = str(int(width))
    ET.SubElement(fn, "Height").text     = str(int(height))
    ET.SubElement(fn, "Rotation").text   = str(int(rotation))
    ET.SubElement(fn, "StartOffset").text= str(int(start_offset))
    ET.SubElement(fn, "IsRelative").text = str(int(is_relative))

    ax0 = ET.SubElement(fn, "Axis")
    ax0.set("Name", "X")
    ET.SubElement(ax0, "Offset").text    = str(x_offset)
    ET.SubElement(ax0, "Frequency").text = str(x_freq)
    ET.SubElement(ax0, "Phase").text     = str(x_phase)

    ax1 = ET.SubElement(fn, "Axis")
    ax1.set("Name", "Y")
    ET.SubElement(ax1, "Offset").text    = str(y_offset)
    ET.SubElement(ax1, "Frequency").text = str(y_freq)
    ET.SubElement(ax1, "Phase").text     = str(y_phase)

    for fe in (fixture_entries or []):
        fix_el = ET.SubElement(fn, "Fixture")
        ET.SubElement(fix_el, "ID").text           = str(fe["fid"])
        ET.SubElement(fix_el, "Head").text         = str(fe.get("head", 0))
        ET.SubElement(fix_el, "Direction").text    = fe.get("direction", "Forward")
        ET.SubElement(fix_el, "StartOffset").text  = str(fe.get("start_offset", 0))

    return fn


def _fe(fid, direction="Forward", start_offset=0):
    return {"fid": fid, "direction": direction, "start_offset": start_offset}


EFX_SHAPES = [
    ("Circle",             "Circle",       0,  {}),
    ("Circle 45deg",       "Circle",      45,  {}),
    ("Eight Oriz",         "Eight",        0,  {}),
    ("Eight Vert",         "Eight",       90,  {}),
    ("Eight Diag",         "Eight",       45,  {}),
    ("Diamond",            "Diamond",      0,  {}),
    ("Diamond 45deg",      "Diamond",     45,  {}),
    ("Square",             "Square",       0,  {}),
    ("SquareChoppy",       "SquareChoppy", 0,  {}),
    ("Leaf",               "Leaf",         0,  {}),
    ("Pan Sweep",          "Line",         0,  {"height_factor": 0}),
    ("Tilt Swing",         "Line",        90,  {"height_factor": 1, "width_factor": 0}),
    ("Pan+Tilt Sweep",     "Line",        45,  {}),
    ("Lissajous 2:1",      "Lissajous",    0,  {"x_freq": 2, "y_freq": 1, "x_phase": 0,  "y_phase": 0}),
    ("Lissajous 3:2",      "Lissajous",    0,  {"x_freq": 3, "y_freq": 2, "x_phase": 0,  "y_phase": 90}),
    ("Lissajous 1:3",      "Lissajous",    0,  {"x_freq": 1, "y_freq": 3, "x_phase": 90, "y_phase": 0}),
    ("Lissajous 3:1",      "Lissajous",    0,  {"x_freq": 3, "y_freq": 1, "x_phase": 0,  "y_phase": 0}),
    ("Lissajous 4:3",      "Lissajous",    0,  {"x_freq": 4, "y_freq": 3, "x_phase": 0,  "y_phase": 90}),
    ("Lissajous 5:4",      "Lissajous",    0,  {"x_freq": 5, "y_freq": 4, "x_phase": 0,  "y_phase": 90}),
]


def _build_efx_kwargs(shape_extra, size_w, size_h):
    kw = {}
    kw["x_freq"]  = shape_extra.get("x_freq",  1)
    kw["y_freq"]  = shape_extra.get("y_freq",  1)
    kw["x_phase"] = shape_extra.get("x_phase", 0)
    kw["y_phase"] = shape_extra.get("y_phase", 90)

    wf = shape_extra.get("width_factor",  1)
    hf = shape_extra.get("height_factor", 1)
    kw["width"]   = int(size_w * wf)
    kw["height"]  = int(size_h * hf)
    return kw


def efx_single_fixture(fid, prefix, efx_path, efx_list_out,
                       next_id_ref, sizes=None, speeds=None):
    sizes  = sizes  or EFX_SIZES
    speeds = speeds or EFX_SPEEDS_SHORT

    for shape_name, algorithm, rotation, extra in EFX_SHAPES:
        for size_name, sw, sh in sizes:
            for speed_name, duration in speeds:
                kw = _build_efx_kwargs(extra, sw, sh)
                efx_name = f"{prefix} » EFX {shape_name} {size_name} {speed_name}"
                el = make_efx(
                    fn_id    = next_id_ref[0],
                    name     = efx_name,
                    path     = efx_path,
                    algorithm= algorithm,
                    rotation = rotation,
                    duration = duration,
                    fixture_entries=[_fe(fid)],
                    **kw
                )
                efx_list_out.append(el)
                next_id_ref[0] += 1

    for speed_name, duration in EFX_SPEEDS:
        for shape_name, algorithm, rotation, extra in [
            ("Circle",     "Circle",  0,  {}),
            ("Eight Oriz", "Eight",   0,  {}),
            ("Pan Sweep",  "Line",    0,  {"height_factor": 0}),
        ]:
            kw = _build_efx_kwargs(extra, 127, 127)
            efx_name = f"{prefix} » EFX {shape_name} Medio {speed_name}"
            el = make_efx(
                fn_id    = next_id_ref[0],
                name     = efx_name + " [v]",
                path     = efx_path,
                algorithm= algorithm,
                rotation = rotation,
                duration = duration,
                fixture_entries=[_fe(fid)],
                **kw
            )
            efx_list_out.append(el)
            next_id_ref[0] += 1

    for size_name, sw, sh in EFX_SIZES:
        for speed_name, duration in EFX_SPEEDS_SHORT:
            efx_name = f"{prefix} » EFX Circle {size_name} {speed_name} {T('Inverso')}"
            el = make_efx(
                fn_id    = next_id_ref[0],
                name     = efx_name,
                path     = efx_path,
                algorithm= "Circle",
                width=sw, height=sh,
                duration = duration,
                direction= "Backward",
                fixture_entries=[_fe(fid, direction="Backward")]
            )
            efx_list_out.append(el)
            next_id_ref[0] += 1

    for amp_key, amp in [("Stretto", 40), ("Medio", 100), ("Largo", 200), ("Full", 255)]:
        amp_name = T(amp_key)
        for speed_name, duration in EFX_SPEEDS_SHORT:
            efx_name = f"{prefix} » EFX Pan Sweep {amp_name} {speed_name}"
            el = make_efx(
                fn_id=next_id_ref[0], name=efx_name, path=efx_path,
                algorithm="Line", rotation=0,
                width=amp, height=0, duration=duration,
                fixture_entries=[_fe(fid)]
            )
            efx_list_out.append(el)
            next_id_ref[0] += 1

    for amp_key, amp in [("Stretto", 40), ("Medio", 100), ("Largo", 200), ("Full", 255)]:
        amp_name = T(amp_key)
        for speed_name, duration in EFX_SPEEDS_SHORT:
            efx_name = f"{prefix} » EFX Tilt Swing {amp_name} {speed_name}"
            el = make_efx(
                fn_id=next_id_ref[0], name=efx_name, path=efx_path,
                algorithm="Line", rotation=90,
                width=0, height=amp, duration=duration,
                fixture_entries=[_fe(fid)]
            )
            efx_list_out.append(el)
            next_id_ref[0] += 1

    for speed_name, duration in EFX_SPEEDS_SHORT:
        efx_name = f"{prefix} » EFX Pan Largo Tilt Stretto {speed_name}"
        el = make_efx(
            fn_id=next_id_ref[0], name=efx_name, path=efx_path,
            algorithm="Circle", rotation=0,
            width=200, height=50, duration=duration,
            fixture_entries=[_fe(fid)]
        )
        efx_list_out.append(el)
        next_id_ref[0] += 1

    for speed_name, duration in EFX_SPEEDS_SHORT:
        efx_name = f"{prefix} » EFX Pan Stretto Tilt Largo {speed_name}"
        el = make_efx(
            fn_id=next_id_ref[0], name=efx_name, path=efx_path,
            algorithm="Circle", rotation=0,
            width=50, height=200, duration=duration,
            fixture_entries=[_fe(fid)]
        )
        efx_list_out.append(el)
        next_id_ref[0] += 1


def _group_fixture_entries(group_infos, mode):
    n = len(group_infos)
    entries = []
    for i, gi in enumerate(group_infos):
        fid = gi["fid"]
        if mode == "sync":
            entries.append(_fe(fid, "Forward", 0))
        elif mode in ("fan", "chase"):
            offset = int(i * 360 / n)
            entries.append(_fe(fid, "Forward", offset))
        elif mode == "mirror":
            direction = "Forward" if i % 2 == 0 else "Backward"
            entries.append(_fe(fid, direction, 0))
        elif mode == "opposite":
            offset = 0 if i % 2 == 0 else 180
            entries.append(_fe(fid, "Forward", offset))
        elif mode == "wave":
            offset = int(i * 270 / max(n - 1, 1))
            entries.append(_fe(fid, "Forward", offset))
        elif mode == "pairs":
            j = n - 1 - i
            offset = int(j * 360 / max(n - 1, 1))
            entries.append(_fe(fid, "Forward", offset))
        else:
            entries.append(_fe(fid, "Forward", 0))
    return entries


EFX_GROUP_MODES = [
    ("Sync",     "sync"),
    ("Fan",      "fan"),
    ("Mirror",   "mirror"),
    ("Opposto",  "opposite"),
    ("Wave",     "wave"),
    ("Chase",    "chase"),
    ("Coppie",   "pairs"),
]

EFX_GROUP_SHAPES = [
    ("Circle",        "Circle",       0,  {}),
    ("Eight Oriz",    "Eight",        0,  {}),
    ("Eight Vert",    "Eight",       90,  {}),
    ("Pan Sweep",     "Line",         0,  {"height_factor": 0}),
    ("Tilt Swing",    "Line",        90,  {"height_factor": 1, "width_factor": 0}),
    ("Diamond",       "Diamond",      0,  {}),
    ("Square",        "Square",       0,  {}),
    ("SquareChoppy",  "SquareChoppy", 0,  {}),
    ("Lissajous 2:1", "Lissajous",    0,  {"x_freq": 2, "y_freq": 1, "x_phase": 0, "y_phase": 0}),
    ("Lissajous 3:2", "Lissajous",    0,  {"x_freq": 3, "y_freq": 2, "x_phase": 0, "y_phase": 90}),
]

EFX_GROUP_SIZES  = [("Piccolo", 60, 60), ("Medio", 127, 127), ("Grande", 200, 200)]
def _EFX_GROUP_SPEEDS():
    return [(T("Lento"),12000),(T("Medio"),6000),(T("Veloce"),3000)]
EFX_GROUP_SPEEDS = _EFX_GROUP_SPEEDS()


def efx_group_fixture(group_label, group_infos, efx_path, efx_list_out, next_id_ref):
    label = f"GRUPPO {group_label}"
    n     = len(group_infos)

    if n < 2:
        return

    for shape_name, algorithm, rotation, extra in EFX_GROUP_SHAPES:
        for size_name, sw, sh in EFX_GROUP_SIZES:
            for speed_name, duration in EFX_GROUP_SPEEDS:
                base_modes = [("Sync", "sync"), ("Fan", "fan"),
                              ("Mirror", "mirror"), (T("Opposto"), "opposite")]

                for mode_label, mode in base_modes:
                    kw = _build_efx_kwargs(extra, sw, sh)
                    efx_name = (f"{label} » EFX {shape_name} "
                                f"{size_name} {speed_name} {mode_label}")
                    entries = _group_fixture_entries(group_infos, mode)

                    el = make_efx(
                        fn_id     = next_id_ref[0],
                        name      = efx_name,
                        path      = efx_path,
                        algorithm = algorithm,
                        rotation  = rotation,
                        duration  = duration,
                        fixture_entries = entries,
                        **kw
                    )
                    efx_list_out.append(el)
                    next_id_ref[0] += 1

                if n >= 3:
                    for mode_label, mode in [("Wave", "wave"), (T("Coppie"), "pairs")]:
                        kw = _build_efx_kwargs(extra, sw, sh)
                        efx_name = (f"{label} » EFX {shape_name} "
                                    f"{size_name} {speed_name} {mode_label}")
                        entries = _group_fixture_entries(group_infos, mode)

                        el = make_efx(
                            fn_id     = next_id_ref[0],
                            name      = efx_name,
                            path      = efx_path,
                            algorithm = algorithm,
                            rotation  = rotation,
                            duration  = duration,
                            fixture_entries = entries,
                            **kw
                        )
                        efx_list_out.append(el)
                        next_id_ref[0] += 1

    for mode_label, mode in [("Fan", "fan"), ("Mirror", "mirror"), (T("Opposto"), "opposite")]:
        for speed_name, duration in EFX_GROUP_SPEEDS:
            entries = _group_fixture_entries(group_infos, mode)
            for shape_label, w, h in [
                ("Pan Wide Tilt Narrow", 200, 50),
                ("Pan Narrow Tilt Wide",  50, 200),
            ]:
                efx_name = f"{label} » EFX {shape_label} {speed_name} {mode_label}"
                el = make_efx(
                    fn_id=next_id_ref[0], name=efx_name, path=efx_path,
                    algorithm="Circle", rotation=0,
                    width=w, height=h, duration=duration,
                    fixture_entries=entries
                )
                efx_list_out.append(el)
                next_id_ref[0] += 1

    for mode_label, mode in [("Sync", "sync"), ("Fan", "fan"), ("Mirror", "mirror")]:
        for speed_name, duration in EFX_GROUP_SPEEDS:
            entries = _group_fixture_entries(group_infos, mode)
            entries_bwd = [
                {**e, "direction": "Backward"} for e in entries
            ]
            efx_name = f"{label} » EFX Circle {T('Medio')} {speed_name} {mode_label} {T('Inverso')}"
            el = make_efx(
                fn_id=next_id_ref[0], name=efx_name, path=efx_path,
                algorithm="Circle", width=127, height=127, duration=duration,
                direction="Backward",
                fixture_entries=entries_bwd
            )
            efx_list_out.append(el)
            next_id_ref[0] += 1


def scenes_group(group_label, group_infos, path):
    scenes = []

    has_rgb     = any(gi["fc"].has_rgb     for gi in group_infos)
    has_cmy     = any(gi["fc"].has_cmy     for gi in group_infos)
    has_moving  = any(gi["fc"].has_moving  for gi in group_infos)
    has_dimmer  = any(gi["fc"].has_dimmer  for gi in group_infos)
    has_shutter = any(gi["fc"].has(G_SHUTTER) for gi in group_infos)

    label = f"GRUPPO {group_label}"

    if has_dimmer:
        for lname, lval in DIMMER_LEVELS:
            v = []
            for gi in group_infos:
                v += [(gi["fid"], ch, lval) for ch in gi["fc"].get(G_INTENSITY)]
            if v:
                scenes.append((f"{label} » Dimmer {lname}", path, v))

        odds  = group_infos[0::2]
        evens = group_infos[1::2]
        if evens:
            for lname, lval in [("Full", 255), ("Zero", 0), ("50%", 127)]:
                v_odd  = [(gi["fid"], ch, lval) for gi in odds  for ch in gi["fc"].get(G_INTENSITY)]
                v_even = [(gi["fid"], ch, 0 if lval > 0 else 255) for gi in evens for ch in gi["fc"].get(G_INTENSITY)]
                if v_odd or v_even:
                    scenes.append((f"{label} » Dimmer ODD {lname}", path, v_odd + v_even))

    if has_shutter:
        open_vals  = []
        close_vals = []
        strobe_slow_v = strobe_med_v = strobe_fast_v = []
        for gi in group_infos:
            for ch_num, info in gi["fc"].get(G_SHUTTER).items():
                caps = info["capabilities"]
                ov, _ = cap_find(caps, "open", "on")
                cv, _ = cap_find(caps, "closed", "blackout", "off")
                if ov is not None:  open_vals.append((gi["fid"], ch_num, ov))
                if cv is not None:  close_vals.append((gi["fid"], ch_num, cv))
                st = strobe_values(caps)
                if "slow" in st:  strobe_slow_v.append((gi["fid"], ch_num, st["slow"]))
                if "med"  in st:  strobe_med_v.append((gi["fid"], ch_num, st["med"]))
                if "fast" in st:  strobe_fast_v.append((gi["fid"], ch_num, st["fast"]))
                break
        if open_vals:
            scenes.append((f"{label} » {T('Shutter Aperto')}",  path, open_vals))
            scenes.append((f"{label} » {T('Shutter Chiuso')}",  path, close_vals))
        if strobe_slow_v: scenes.append((f"{label} » Strobe Slow",  path, strobe_slow_v))
        if strobe_med_v:  scenes.append((f"{label} » Strobe Med",   path, strobe_med_v))
        if strobe_fast_v: scenes.append((f"{label} » Strobe Fast",  path, strobe_fast_v))

    if has_rgb:
        for color_name, r, g, b in RGB_PALETTE:
            v = []
            for gi in group_infos:
                fc = gi["fc"]
                v += [(gi["fid"], ch, r) for ch in fc.get(G_RED)]
                v += [(gi["fid"], ch, g) for ch in fc.get(G_GREEN)]
                v += [(gi["fid"], ch, b) for ch in fc.get(G_BLUE)]
                if fc.has_white:
                    w = 255 if r == g == b == 255 else 0
                    v += [(gi["fid"], ch, w) for ch in fc.get(G_WHITE)]
            scenes.append((f"{label} » {color_name}", path, v))

        for (n1, r1, g1, b1), (n2, r2, g2, b2) in [
            (("Rosso", 255, 0, 0),   ("Blu",     0, 0, 255)),
            (("Rosso", 255, 0, 0),   ("Verde",   0, 255, 0)),
            (("Giallo", 255, 255, 0),("Blu",     0, 0, 255)),
            (("Ciano",  0, 255, 255),("Magenta", 255, 0, 255)),
        ]:
            v = []
            for idx, gi in enumerate(group_infos):
                fc = gi["fc"]
                r, g, b = (r1, g1, b1) if idx % 2 == 0 else (r2, g2, b2)
                v += [(gi["fid"], ch, r) for ch in fc.get(G_RED)]
                v += [(gi["fid"], ch, g) for ch in fc.get(G_GREEN)]
                v += [(gi["fid"], ch, b) for ch in fc.get(G_BLUE)]
            scenes.append((f"{label} » {T('Alternato')} {n1}/{n2}", path, v))

    if has_cmy:
        for color_name, c, m, y in CMY_PALETTE:
            v = []
            for gi in group_infos:
                fc = gi["fc"]
                v += [(gi["fid"], ch, c) for ch in fc.get(G_CYAN)]
                v += [(gi["fid"], ch, m) for ch in fc.get(G_MAGENTA)]
                v += [(gi["fid"], ch, y) for ch in fc.get(G_YELLOW)]
            scenes.append((f"{label} » CMY {color_name}", path, v))

    if has_moving:
        for pos_name, pan_v, tilt_v in MOVING_POSITIONS:
            v = []
            for gi in group_infos:
                fc = gi["fc"]
                if pan_v is not None:
                    v += [(gi["fid"], ch, pan_v) for ch in fc.get(G_PAN)]
                    v += [(gi["fid"], ch, 0)     for ch in fc.get_fine(G_PAN)]
                if tilt_v is not None:
                    v += [(gi["fid"], ch, tilt_v) for ch in fc.get(G_TILT)]
                    v += [(gi["fid"], ch, 0)       for ch in fc.get_fine(G_TILT)]
            if v:
                scenes.append((f"{label} » {pos_name}", path, v))

        if len(group_infos) >= 2:
            v = []
            for idx, gi in enumerate(group_infos):
                fc = gi["fc"]
                tilt_v = 80 if idx % 2 == 0 else 170
                v += [(gi["fid"], ch, 127)   for ch in fc.get(G_PAN)]
                v += [(gi["fid"], ch, tilt_v) for ch in fc.get(G_TILT)]
            scenes.append((f"{label} » PT Fan Tilt ODD/EVEN", path, v))

            n = len(group_infos)
            v = []
            for idx, gi in enumerate(group_infos):
                fc = gi["fc"]
                if n > 1:
                    pan_v = int(30 + (idx / (n - 1)) * 196)
                else:
                    pan_v = 127
                v += [(gi["fid"], ch, pan_v) for ch in fc.get(G_PAN)]
                v += [(gi["fid"], ch, 127)   for ch in fc.get(G_TILT)]
            scenes.append((f"{label} » PT Fan Pan Spread", path, v))

    return scenes


# ══════════════════════════════════════════════════════════════════════════════
# Fallback per fixture Generic
# ══════════════════════════════════════════════════════════════════════════════

def make_generic_ch_map(model, mode, n_channels):
    model_low = model.lower().strip()
    mode_low = mode.lower().strip()

    def ch(num, group, byte=0, caps=None):
        return {num: {"name": group, "group": group,
                      "byte": byte, "capabilities": caps or []}}

    def dimmer_caps():
        return [(0, 255, "Intensity")]

    def color_caps():
        return [(0, 255, "0-255")]

    def shutter_caps():
        return [
            (0,   0,   "Open"),
            (1,   254, "Strobe slow to fast"),
            (255, 255, "Open"),
        ]

    is_dimmer_rgb = (
        "dimmer rgb" in mode_low or
        "rgb dimmer" in mode_low or
        "irgb" in model_low or
        (n_channels == 4 and "rgb" in model_low and "dimmer" in model_low)
    )

    if model_low in ("generic rgb", "rgb") and not is_dimmer_rgb:
        return {**ch(0, G_RED,   caps=color_caps()),
                **ch(1, G_GREEN, caps=color_caps()),
                **ch(2, G_BLUE,  caps=color_caps())}

    if model_low in ("generic rgbw", "rgbw"):
        if not is_dimmer_rgb:
            return {**ch(0, G_RED,   caps=color_caps()),
                    **ch(1, G_GREEN, caps=color_caps()),
                    **ch(2, G_BLUE,  caps=color_caps()),
                    **ch(3, G_WHITE, caps=color_caps())}
        else:
            return {**ch(0, G_INTENSITY, caps=dimmer_caps()),
                    **ch(1, G_RED,   caps=color_caps()),
                    **ch(2, G_GREEN, caps=color_caps()),
                    **ch(3, G_BLUE,  caps=color_caps()),
                    **ch(4, G_WHITE, caps=color_caps())}

    if model_low in ("generic rgba", "rgba"):
        if not is_dimmer_rgb:
            return {**ch(0, G_RED,   caps=color_caps()),
                    **ch(1, G_GREEN, caps=color_caps()),
                    **ch(2, G_BLUE,  caps=color_caps()),
                    **ch(3, G_AMBER, caps=color_caps())}
        else:
            return {**ch(0, G_INTENSITY, caps=dimmer_caps()),
                    **ch(1, G_RED,   caps=color_caps()),
                    **ch(2, G_GREEN, caps=color_caps()),
                    **ch(3, G_BLUE,  caps=color_caps()),
                    **ch(4, G_AMBER, caps=color_caps())}

    if model_low in ("generic rgbaw", "rgbaw"):
        return {**ch(0, G_RED,   caps=color_caps()),
                **ch(1, G_GREEN, caps=color_caps()),
                **ch(2, G_BLUE,  caps=color_caps()),
                **ch(3, G_AMBER, caps=color_caps()),
                **ch(4, G_WHITE, caps=color_caps())}

    if "rgbw" in model_low:
        if not is_dimmer_rgb:
            return {**ch(0, G_RED), **ch(1, G_GREEN),
                    **ch(2, G_BLUE), **ch(3, G_WHITE)}
        else:
            return {**ch(0, G_INTENSITY, caps=dimmer_caps()),
                    **ch(1, G_RED), **ch(2, G_GREEN),
                    **ch(3, G_BLUE), **ch(4, G_WHITE)}

    if "rgba" in model_low:
        if not is_dimmer_rgb:
            return {**ch(0, G_RED), **ch(1, G_GREEN),
                    **ch(2, G_BLUE), **ch(3, G_AMBER)}
        else:
            return {**ch(0, G_INTENSITY, caps=dimmer_caps()),
                    **ch(1, G_RED), **ch(2, G_GREEN),
                    **ch(3, G_BLUE), **ch(4, G_AMBER)}

    if "rgb" in model_low:
        if not is_dimmer_rgb and n_channels == 3:
            return {**ch(0, G_RED), **ch(1, G_GREEN), **ch(2, G_BLUE)}
        else:
            return {**ch(0, G_INTENSITY, caps=dimmer_caps()),
                    **ch(1, G_RED, caps=color_caps()),
                    **ch(2, G_GREEN, caps=color_caps()),
                    **ch(3, G_BLUE, caps=color_caps())}

    if "cmy" in model_low:
        return {**ch(0, G_CYAN), **ch(1, G_MAGENTA), **ch(2, G_YELLOW)}

    if "smoke" in model_low or "haze" in model_low or "fog" in model_low:
        return {**ch(0, G_EFFECT, caps=[(0, 0, "Off"), (1, 255, "Fog")])}

    result = {}
    result.update(ch(0, G_INTENSITY, caps=dimmer_caps()))
    if n_channels >= 2:
        result.update(ch(1, G_SHUTTER, caps=shutter_caps()))
    if n_channels >= 3 and "dimmer" not in model_low:
        result.update(ch(0, G_RED,   caps=color_caps()))
        result.update(ch(1, G_GREEN, caps=color_caps()))
        result.update(ch(2, G_BLUE,  caps=color_caps()))
    return result


# ══════════════════════════════════════════════════════════════════════════════
# Funzione principale di generazione / Main palette generation function
# ══════════════════════════════════════════════════════════════════════════════

def _is_likely_moving_head(name):
    name_lower = name.lower()
    keywords = ['mh', 'moving', 'head', 'beam', 'testa mobile', 'teste mobili', 'mh-', 'mh ']
    return any(kw in name_lower for kw in keywords)


def _extract_base_name(name):
    import re
    base = name.strip()
    patterns = [
        r"\s+(?:L|R|Left|Right|SX|DX|C|Center)$",
        r"\s+#?\d+$",
        r"\s+\d+$",
    ]
    for pattern in patterns:
        base = re.sub(pattern, "", base, flags=re.IGNORECASE)
    return base.strip()


def generate_palettes(fixtures_data, fixture_dirs, cfg):
    all_scenes = []
    all_efx    = []
    all_dimmer_vals  = []
    all_shutter_info = []
    all_moving_info  = []
    all_fixtures_info = []
    all_rgb_info     = []  # per scene GLOBAL colori / for GLOBAL color scenes

    min_cap   = cfg.get("min_cap_scenes", 2)
    skip_efx  = cfg.get("skip_efx", False)

    efx_id_ref = [0]

    for fix in fixtures_data:
        fid  = fix["id"]
        name = fix["name"]
        mfr  = fix["manufacturer"]
        mdl  = fix["model"]
        mode = fix["mode"]

        qxf = load_fixture_definition(mfr, mdl, fixture_dirs)
        if qxf is None:
            ch_map = make_generic_ch_map(mdl, mode, fix["channels"])
            if ch_map:
                print(f"  [INFO] Fallback generico: '{mfr} / {mdl}' ({name}) — {len(ch_map)} canali inferiti")
            else:
                print(f"  [WARN] Definizione non trovata e fallback impossibile: '{mfr} / {mdl}' ({name})")
                continue
        else:
            ch_map = parse_qxf_mode(qxf, mode)
            if _is_likely_moving_head(name):
                print(f"  [DEBUG] Canali trovati per {name} ({mfr} {mdl}):")
                for ch_num, ch_info in sorted(ch_map.items()):
                    print(f"    Ch{ch_num}: {ch_info.get('name', 'N/A')} (group: {ch_info.get('group', 'N/A')})")
        if not ch_map:
            print(f"  [WARN] Mode '{mode}' non trovato per '{mfr} / {mdl}'")
            continue

        fc = FixtureChannels(ch_map)
        prefix = name
        path   = f"Auto Palette/{name}"

        for ch in fc.get(G_INTENSITY):
            all_dimmer_vals.append((fid, ch))
        for ch_num, info in fc.get(G_SHUTTER).items():
            all_shutter_info.append((fid, ch_num, info))
        if fc.has_moving:
            all_moving_info.append((fid, fc))

        for scene_fn in [
            lambda: scenes_dimmer(fid, prefix, fc, path),
            lambda: scenes_rgb(fid, prefix, fc, path),
            lambda: scenes_cmy(fid, prefix, fc, path),
            lambda: scenes_white_standalone(fid, prefix, fc, path),
            lambda: scenes_amber_standalone(fid, prefix, fc, path),
            lambda: scenes_uv(fid, prefix, fc, path),
            lambda: scenes_color_wheel(fid, prefix, fc, path, min_cap),
            lambda: scenes_gobo(fid, prefix, fc, path, min_cap),
            lambda: scenes_prism(fid, prefix, fc, path),
            lambda: scenes_zoom(fid, prefix, fc, path),
            lambda: scenes_iris(fid, prefix, fc, path),
            lambda: scenes_focus(fid, prefix, fc, path),
            lambda: scenes_frost(fid, prefix, fc, path),
            lambda: scenes_speed(fid, prefix, fc, path),
            lambda: scenes_effect(fid, prefix, fc, path, min_cap),
            lambda: scenes_moving(fid, prefix, fc, path),
        ]:
            all_scenes += scene_fn()

        if not cfg.get("skip_combos"):
            all_scenes += scenes_combo(fid, prefix, fc, path)

        if not skip_efx and fc.has_moving:
            print(f"    [DEBUG] EFX per {fix['name']}: {len(fc.raw)} canali, Pan/Tilt rilevati")
            efx_path = f"Auto Palette/EFX/{name}"
            efx_single_fixture(fid, prefix, efx_path, all_efx, efx_id_ref)

        # Raccoglie i canali RGB per le scene globali colore
        # Collects RGB channels for global color scenes
        if fc.has_rgb:
            all_rgb_info.append({"fid": fid, "fc": fc})

        all_fixtures_info.append({"fid": fid, "fix": fix, "fc": fc})

    # ── Scene GLOBALI / Global scenes (all fixtures) ─────────────────────────────
    gp = "Auto Palette/GLOBAL"
    global_scenes = []

    if all_dimmer_vals:
        for lname, lval in DIMMER_LEVELS:
            global_scenes.append((
                f"GLOBAL » Dimmer {lname}", gp,
                [(fid, ch, lval) for (fid, ch) in all_dimmer_vals]
            ))

    if all_shutter_info:
        open_vals  = []
        close_vals = []
        sls, sms, sfs = [], [], []
        for (fid, ch_num, info) in all_shutter_info:
            caps = info["capabilities"]
            ov, _ = cap_find(caps, "open", "on", "lamp on")
            cv, _ = cap_find(caps, "closed", "blackout", "off")
            if ov is not None:  open_vals.append((fid, ch_num, ov))
            if cv is not None:  close_vals.append((fid, ch_num, cv))
            st = strobe_values(caps)
            if "slow" in st: sls.append((fid, ch_num, st["slow"]))
            if "med"  in st: sms.append((fid, ch_num, st["med"]))
            if "fast" in st: sfs.append((fid, ch_num, st["fast"]))
        if open_vals:  global_scenes.append((f"GLOBAL » {T('All Shutter Aperto')}", gp, open_vals))
        if close_vals: global_scenes.append((f"GLOBAL » {T('All Shutter Chiuso')}", gp, close_vals))
        if sls: global_scenes.append(("GLOBAL » All Strobe Slow",  gp, sls))
        if sms: global_scenes.append(("GLOBAL » All Strobe Med",   gp, sms))
        if sfs: global_scenes.append(("GLOBAL » All Strobe Fast",  gp, sfs))

    if all_moving_info:
        center_vals = []
        for (fid, fc) in all_moving_info:
            center_vals += [(fid, ch, 127) for ch in fc.get(G_PAN)]
            center_vals += [(fid, ch, 0)   for ch in fc.get_fine(G_PAN)]
            center_vals += [(fid, ch, 127) for ch in fc.get(G_TILT)]
            center_vals += [(fid, ch, 0)   for ch in fc.get_fine(G_TILT)]
        global_scenes.append(("GLOBAL » All Moving Center", gp, center_vals))

    # ── Scene GLOBAL colori RGB / GLOBAL RGB color scenes ─────────────────────────
    # IT: Imposta tutti i LED RGB allo stesso colore contemporaneamente
    # EN: Sets all RGB LEDs to the same color simultaneously
    if all_rgb_info:
        for color_name, r, g, b in RGB_PALETTE:
            vals = []
            for ri in all_rgb_info:
                fc_r = ri["fc"]
                vals += [(ri["fid"], ch, r) for ch in fc_r.get(G_RED)]
                vals += [(ri["fid"], ch, g) for ch in fc_r.get(G_GREEN)]
                vals += [(ri["fid"], ch, b) for ch in fc_r.get(G_BLUE)]
                if fc_r.has_white:
                    w = 255 if r == g == b == 255 else 0
                    vals += [(ri["fid"], ch, w) for ch in fc_r.get(G_WHITE)]
            if vals:
                global_scenes.append((f"GLOBAL » {color_name}", gp, vals))

    # ── Scene GRUPPO + EFX GRUPPO / Group scenes + Group EFX ──────────────────────
    group_scenes = []
    if not cfg.get("skip_groups"):
        by_model = defaultdict(list)
        for gi in all_fixtures_info:
            fix_name = gi["fix"]["name"]
            base_name = _extract_base_name(fix_name)
            mode = gi["fix"]["mode"]
            channels = gi["fix"]["channels"]
            key = (gi["fix"]["model"], mode, channels)
            by_model[key].append(gi)

        for (mdl, mode, channels), group in by_model.items():
            if len(group) < 2:
                continue
            # Label leggibile: aggiunge mode se non vuoto e ≠ al nome del modello
            group_label = f"{mdl} ({mode})" if mode and mode != mdl else mdl
            gpath      = f"Auto Palette/GRUPPI/{group_label}"
            efx_gpath  = f"Auto Palette/EFX/GRUPPI/{group_label}"
            group_scenes += scenes_group(group_label, group, gpath)

            has_moving_in_group = any(gi["fc"].has_moving for gi in group)
            if not skip_efx and has_moving_in_group:
                print(f"    [DEBUG] EFX gruppo {group_label}: {sum(1 for gi in group if gi['fc'].has_moving)} moving head")
                efx_group_fixture(group_label, group, efx_gpath, all_efx, efx_id_ref)

    all_ordered_scenes = global_scenes + group_scenes + all_scenes

    # ── Dizionario per i Chaser / Chaser scene-map dictionary ────────────────────
    # IT: La chiave include manufacturer, model, mode E channels per separare
    #     correttamente fixture con lo stesso modello ma configurazioni diverse
    #     (es. Generic RGB 3ch puro vs Generic RGB 4ch con dimmer = IRGB).
    # EN: Key includes manufacturer, model, mode AND channels to correctly separate
    #     fixtures with the same model name but different configurations
    #     (e.g. pure RGB 3ch vs Dimmer+RGB 4ch / IRGB).
    by_model_for_chasers = defaultdict(list)
    for gi in all_fixtures_info:
        key = (
            gi["fix"]["manufacturer"],
            gi["fix"]["model"],
            gi["fix"]["mode"],
            gi["fix"]["channels"],
        )
        by_model_for_chasers[key].append(gi)

    return all_ordered_scenes, all_efx, all_fixtures_info, dict(by_model_for_chasers), all_rgb_info, all_shutter_info, all_dimmer_vals


# ══════════════════════════════════════════════════════════════════════════════
# CHASER — Sequenze di effetti / Effect sequences
# ══════════════════════════════════════════════════════════════════════════════

def _CHASER_SPEEDS():
    return [(T("Lentissimo"),4000),(T("Lento"),2000),(T("Medio"),1000),(T("Veloce"),500),(T("Velocissimo"),250),(T("Strobo"),100),(T("Mega Strobo"),50)]
CHASER_SPEEDS = _CHASER_SPEEDS()

CHASER_COLOR_SPEEDS = CHASER_SPEEDS[:5]  # calcolato dopo CHASER_SPEEDS

def _CHASER_FLASH_SPEEDS():
    return [(T("Lento"),800),(T("Medio"),400),(T("Veloce"),200),(T("Strobo"),80),(T("Mega Strobo"),40)]
CHASER_FLASH_SPEEDS = _CHASER_FLASH_SPEEDS()

RGB_NAMES_FULL      = list([n for (n, r, g, b) in RGB_PALETTE])  # aggiornato da _init_lang()
RGB_NAMES_PASTELLI  = [n for (n, r, g, b) in RGB_PALETTE if "Pastello" in n]  # aggiornato da _init_lang()
RGB_NAMES_CALDI     = ["Rosso", "Arancio", "Ambra", "Gold", "Giallo", "Corallo",
                        "Fuoco", "Brace", "Bianco Caldo", "Rosso Scuro", "Cremisi"]  # aggiornato da _init_lang()
RGB_NAMES_FREDDI    = ["Blu", "Ciano", "Teal", "Acquamarina", "Lavanda", "Indaco",
                        "Blu Notte", "Azzurro Reale", "Ghiaccio", "Bianco Freddo",
                        "Pastello Azzurro", "Pastello Menta"]  # aggiornato da _init_lang()
RGB_NAMES_CLUB      = ["Rosso", "Verde", "Blu", "Bianco"]  # aggiornato da _init_lang()
RGB_NAMES_DISCOTECA = ["Rosso", "Verde", "Blu", "Giallo", "Ciano", "Magenta",
                        "Arancio", "Rosa", "Viola", "Ambra"]  # aggiornato da _init_lang()
RGB_NAMES_TEATRALI  = ["Rosso Scuro", "Blu Notte", "Verde Bosco", "Ambra",
                        "Viola", "Cremisi", "Gold", "Bianco Caldo"]  # aggiornato da _init_lang()
RGB_NAMES_PRIMARI   = ["Rosso", "Verde", "Blu"]  # aggiornato da _init_lang()
RGB_NAMES_SECONDARI = ["Giallo", "Ciano", "Magenta"]  # aggiornato da _init_lang()
RGB_NAMES_ARCOBALENO= ["Rosso", "Arancio", "Giallo", "Verde", "Ciano", "Blu",
                        "Indaco", "Viola", "Magenta"]  # aggiornato da _init_lang()

BICOLORI = [  # aggiornato da _init_lang()
    ("Rosso-Blu",     "Rosso",   "Blu"),
    ("Rosso-Bianco",  "Rosso",   "Bianco"),
    ("Blu-Bianco",    "Blu",     "Bianco"),
    ("Giallo-Blu",    "Giallo",  "Blu"),
    ("Verde-Magenta", "Verde",   "Magenta"),
    ("Arancio-Blu",   "Arancio", "Blu"),
    ("Rosso-Verde",   "Rosso",   "Verde"),
    ("Ciano-Rosso",   "Ciano",   "Rosso"),
    ("Giallo-Viola",  "Giallo",  "Viola"),
    ("Ambra-Blu",     "Ambra",   "Blu"),
    ("Bianco-Viola",  "Bianco",  "Viola"),
    ("Fuoco-Ghiaccio","Fuoco",   "Ghiaccio"),
]

TRICOLORI = [  # aggiornato da _init_lang()
    ("IT",    "Bianco", "Rosso",   "Verde"),
    ("RGB",   "Rosso",  "Verde",   "Blu"),
    ("CMY",   "Ciano",  "Magenta", "Giallo"),
    ("Fuoco", "Rosso",  "Arancio", "Giallo"),
    ("Party", "Rosso",  "Blu",     "Giallo"),
    ("Alpin", "Rosso",  "Bianco",  "Blu"),
]


def make_chaser(fn_id, name, path,
                steps,
                run_order="Loop",
                direction="Forward",
                fade_in_mode="Default",
                fade_out_mode="Default",
                duration_mode="PerStep",
                global_fade_in=0,
                global_fade_out=0):
    fn = ET.Element("Function")
    fn.set("ID",   str(fn_id))
    fn.set("Type", "Chaser")
    fn.set("Name", name)
    fn.set("Path", path)

    speed = ET.SubElement(fn, "Speed")
    speed.set("FadeIn",   str(global_fade_in))
    speed.set("FadeOut",  str(global_fade_out))
    speed.set("Duration", "0")

    ET.SubElement(fn, "Direction").text = direction
    ET.SubElement(fn, "RunOrder").text  = run_order

    sm = ET.SubElement(fn, "SpeedModes")
    sm.set("FadeIn",   fade_in_mode)
    sm.set("FadeOut",  fade_out_mode)
    sm.set("Duration", duration_mode)

    for i, step in enumerate(steps):
        sid   = step[0]
        hold  = step[1]
        fi    = step[2] if len(step) > 2 else 0
        fo    = step[3] if len(step) > 3 else 0
        se = ET.SubElement(fn, "Step")
        se.set("Number",  str(i))
        se.set("FadeIn",  str(fi))
        se.set("Hold",    str(hold))
        se.set("FadeOut", str(fo))
        se.text = str(sid)

    return fn


def _sid(scene_map, name):
    return scene_map.get(name)


def _steps_from_names(scene_map, prefix_sep, names, hold, fade_in=0, fade_out=0):
    steps = []
    for n in names:
        sid = _sid(scene_map, f"{prefix_sep}{n}")
        if sid is not None:
            steps.append((sid, hold, fade_in, fade_out))
    return steps


# ══════════════════════════════════════════════════════════════════════════════
# Chaser per singola fixture / Single-fixture chasers
# ══════════════════════════════════════════════════════════════════════════════

def chasers_single_fixture(fid, prefix, fc, scene_map, chaser_path, ch_list, next_id_ref):
    sep = f"{prefix} » "

    def add(name, steps, run_order="Loop", direction="Forward",
            fade_in_mode="Default", fade_out_mode="Default"):
        if not steps:
            return
        el = make_chaser(
            fn_id=next_id_ref[0], name=f"{prefix} » CHR {name}",
            path=chaser_path, steps=steps,
            run_order=run_order, direction=direction,
            fade_in_mode=fade_in_mode, fade_out_mode=fade_out_mode
        )
        ch_list.append(el)
        next_id_ref[0] += 1

    has_rgb     = fc.has_rgb
    has_cmy     = fc.has_cmy
    has_dimmer  = fc.has_dimmer
    has_shutter = fc.has(G_SHUTTER)
    has_moving  = fc.has_moving

    if has_dimmer:
        full_id = _sid(scene_map, f"{sep}Dimmer {T('Full')}")
        zero_id = _sid(scene_map, f"{sep}Dimmer Zero")
        h50_id  = _sid(scene_map, f"{sep}Dimmer 50%")
        h25_id  = _sid(scene_map, f"{sep}Dimmer 25%")
        h75_id  = _sid(scene_map, f"{sep}Dimmer 75%")
        h10_id  = _sid(scene_map, f"{sep}Dimmer 10%")

        if full_id and zero_id:
            for spd_name, hold in CHASER_FLASH_SPEEDS:
                add(f"Stomp {spd_name}",
                    [(full_id, hold), (zero_id, hold)])

            for spd_name, hold in [("Lento", 600), ("Medio", 300)]:
                steps = []
                if h25_id: steps.append((h25_id, hold))
                if h75_id: steps.append((h75_id, hold))
                if full_id: steps.append((full_id, hold * 2))
                if h75_id: steps.append((h75_id, hold))
                if h25_id: steps.append((h25_id, hold))
                if zero_id: steps.append((zero_id, hold * 3))
                add(f"Heartbeat {spd_name}", steps)

            breath_seq = []
            for n in ["Dimmer 10%", "Dimmer 25%", "Dimmer 50%",
                      "Dimmer 75%", "Dimmer Full",
                      "Dimmer 75%", "Dimmer 50%", "Dimmer 25%", "Dimmer 10%", "Dimmer Zero"]:
                sid = _sid(scene_map, f"{sep}{n}")
                if sid:
                    breath_seq.append((sid, 300, 200, 200))
            if breath_seq:
                for spd_name, mult in [("Lento", 3), ("Medio", 1)]:
                    steps = [(s, h * mult, fi * mult, fo * mult)
                             for (s, h, fi, fo) in breath_seq]
                    add(f"Breathing {spd_name}", steps,
                        fade_in_mode="PerStep", fade_out_mode="PerStep")

            for spd_name, hold in [("Medio", 120), ("Veloce", 60)]:
                blank = hold * 4
                steps = [(full_id, hold), (zero_id, hold),
                         (full_id, hold), (zero_id, blank)]
                add(f"Double Flash {spd_name}", steps)

            for spd_name, hold in [("Medio", 100), ("Veloce", 50)]:
                blank = hold * 5
                steps = [(full_id, hold), (zero_id, hold),
                         (full_id, hold), (zero_id, hold),
                         (full_id, hold), (zero_id, blank)]
                add(f"Triple Flash {spd_name}", steps)

            for spd_name, hold in [("Veloce", 60)]:
                blank = hold * 6
                steps = [(full_id, hold), (zero_id, hold)] * 4 + [(zero_id, blank)]
                add(f"Quad Flash {spd_name}", steps)

            for spd_name, base in [("Lento", 300), ("Veloce", 80)]:
                steps = [
                    (full_id, base // 3), (zero_id, base * 2),
                    (full_id, base),      (zero_id, base // 2),
                    (full_id, base // 4), (zero_id, base * 4),
                    (full_id, base // 2), (zero_id, base * 6),
                    (full_id, base // 3), (zero_id, base * 3),
                    (full_id, base),      (zero_id, base * 8),
                ]
                add(f"Lightning {spd_name}", steps)

            if full_id and zero_id and h50_id:
                steps = [
                    (full_id, 40), (zero_id, 60),
                    (h50_id,  80), (full_id, 30),
                    (zero_id, 40), (full_id, 90),
                    (h25_id,  50) if h25_id else (zero_id, 50),
                    (full_id, 30), (zero_id, 120),
                ]
                add("Flicker Fiamma", steps)

            ramp_up = [(full_id, 50), (h75_id, 50), (h50_id, 50),
                       (h25_id, 50), (zero_id, 50)] if all([full_id, h75_id, h50_id, h25_id, zero_id]) else []
            ramp_down = list(reversed(ramp_up))
            if ramp_up:
                add(T("Ramp Up Down"), ramp_up + ramp_down)

            for spd_name, hold in [("Lento", 1500), ("Medio", 800), ("Veloce", 300)]:
                add(f"Pulse {spd_name}", [(full_id, hold), (zero_id, hold * 2)],
                    run_order="Loop")

        if has_shutter:
            shut_open  = _sid(scene_map, f"{sep}{T('Shutter Aperto')}")
            shut_close = _sid(scene_map, f"{sep}{T('Shutter Chiuso')}")
            if shut_open and shut_close:
                for spd_name, hold in [("Lento", 500), ("Medio", 200), ("Veloce", 80)]:
                    add(f"Shutter Stomp {spd_name}",
                        [(shut_open, hold), (shut_close, hold)])

    if has_rgb:

        def rgb(name, colors, hold, run="Loop", fi=0, fo=0, fade_in_mode="Default"):
            steps = _steps_from_names(scene_map, sep, colors, hold, fi, fo)
            add(name, steps, run_order=run, fade_in_mode=fade_in_mode, fade_out_mode=fade_in_mode)

        for spd_name, hold in CHASER_COLOR_SPEEDS:
            rgb(f"{T('Arcobaleno')} {spd_name}", RGB_NAMES_ARCOBALENO, hold)

        for spd_name, hold in [("Lento", 1500), ("Medio", 800), ("Veloce", 400)]:
            rgb(f"{T('Arcobaleno')} Smooth {spd_name}", RGB_NAMES_ARCOBALENO,
                hold, fi=hold // 2, fo=hold // 2, fade_in_mode="PerStep")

        for spd_name, hold in [("Lento", 1000), ("Medio", 500)]:
            rgb(f"{T('Arcobaleno')} PingPong {spd_name}", RGB_NAMES_ARCOBALENO, hold, run="PingPong")

        for spd_name, hold in [("Lento", 1500), ("Medio", 800), ("Veloce", 400)]:
            rgb(f"{T('Rainbow Completo')} {spd_name}", RGB_NAMES_FULL, hold)

        for spd_name, hold in [("Medio", 800), ("Veloce", 400)]:
            rgb(f"{T('Rainbow Casuale')} {spd_name}", RGB_NAMES_FULL, hold, run="Random")

        for spd_name, hold in [("Lento", 1500), ("Medio", 800), ("Veloce", 400)]:
            rgb(f"{T('Pastelli')} {spd_name}", RGB_NAMES_PASTELLI, hold)
        rgb(f"{T('Pastelli')} Smooth {T('Lento')}", RGB_NAMES_PASTELLI, 1500, fi=700, fo=700, fade_in_mode="PerStep")

        for spd_name, hold in [("Lento", 1500), ("Medio", 800), ("Veloce", 400)]:
            rgb(f"{T('Colori Caldi')} {spd_name}", RGB_NAMES_CALDI, hold)

        for spd_name, hold in [("Lento", 1500), ("Medio", 800), ("Veloce", 400)]:
            rgb(f"{T('Colori Freddi')} {spd_name}", RGB_NAMES_FREDDI, hold)

        for spd_name, hold in [("Lento", 2000), ("Medio", 1000)]:
            rgb(f"{T('Colori Teatrali')} {spd_name}", RGB_NAMES_TEATRALI, hold)
        rgb(f"{T('Colori Teatrali')} Smooth {T('Lento')}", RGB_NAMES_TEATRALI, 2000, fi=800, fo=800, fade_in_mode="PerStep")

        for spd_name, hold in CHASER_COLOR_SPEEDS[:4]:
            rgb(f"{T('Club Colors')} {spd_name}", RGB_NAMES_CLUB, hold)

        for spd_name, hold in [("Medio", 500), ("Veloce", 250), ("Velocissimo", 120)]:
            rgb(f"{T('Discoteca')} {spd_name}", RGB_NAMES_DISCOTECA, hold)
        rgb(f"{T('Discoteca Casuale')} {T('Veloce')}", RGB_NAMES_DISCOTECA, 250, run="Random")

        for spd_name, hold in [("Lento", 1000), ("Medio", 500), ("Veloce", 200)]:
            rgb(f"{T('Primari')} {spd_name}", RGB_NAMES_PRIMARI, hold)
            rgb(f"{T('Secondari')} {spd_name}", RGB_NAMES_SECONDARI, hold)

        for bc_name, c1, c2 in BICOLORI:
            for spd_name, hold in [("Lento", 1000), ("Medio", 500), ("Veloce", 200), ("Strobo", 80)]:
                rgb(f"{T('Bicolore')} {bc_name} {spd_name}", [c1, c2], hold)

        for tc_name, c1, c2, c3 in TRICOLORI:
            for spd_name, hold in [("Lento", 1000), ("Medio", 500), ("Veloce", 200)]:
                rgb(f"{T('Tricolore')} {tc_name} {spd_name}", [c1, c2, c3], hold)

        if has_shutter:
            shut_close = _sid(scene_map, f"{sep}{T('Shutter Chiuso')}")
            shut_open  = _sid(scene_map, f"{sep}{T('Shutter Aperto')}")
            if shut_close and shut_open:
                for spd_name, hold in [("Veloce", 150), ("Strobo", 60)]:
                    steps = []
                    for cname in RGB_NAMES_ARCOBALENO:
                        sid = _sid(scene_map, f"{sep}{cname}")
                        if sid:
                            steps += [(sid, hold), (shut_close, hold // 3)]
                    add(f"{T('Strobe Arcobaleno')} {spd_name}", steps)

        bianco_id = _sid(scene_map, f"{sep}{T('Bianco')}")
        zero_id   = _sid(scene_map, f"{sep}Dimmer Zero")
        if bianco_id:
            for spd_name, hold in [("Lento", 800), ("Veloce", 200)]:
                steps = [(bianco_id, hold)]
                if zero_id:
                    steps.append((zero_id, hold * 3))
                add(f"{T('Lampo Bianco')} {spd_name}", steps, run_order="SingleShot")

        red_id  = _sid(scene_map, f"{sep}{T('Rosso')}")
        blue_id = _sid(scene_map, f"{sep}{T('Blu')}")
        if red_id and blue_id:
            for spd_name, hold, n_rep in [("Lento", 300, 3), ("Veloce", 100, 3)]:
                steps = []
                for _ in range(n_rep):
                    steps += [(red_id, hold), (red_id, hold)]
                for _ in range(n_rep):
                    steps += [(blue_id, hold), (blue_id, hold)]
                add(f"Police {spd_name}", steps)

        white_id = _sid(scene_map, f"{sep}{T('Bianco')}")
        if red_id and white_id:
            for spd_name, hold in [("Lento", 250), ("Veloce", 100)]:
                steps = [(red_id, hold)] * 2 + [(white_id, hold)] * 2
                add(f"{T('Ambulanza')} {spd_name}", steps)

        tecno_colors = [T("Rosso"), T("Blu"), T("Verde"), T("Giallo"), T("Ciano"), T("Magenta")]
        for spd_name, hold in [("Veloce", 120), ("Strobo", 60), ("Mega Strobo", 30)]:
            rgb(f"{T('Tecno')} {spd_name}", tecno_colors, hold)
        rgb(f"{T('Tecno Casuale')} {T('Veloce')}", tecno_colors, 120, run="Random")

        for spd_name, hold in [("Lento", 2000), ("Medio", 1000), ("Veloce", 500)]:
            rgb(f"{T('Warm-Cool')} {spd_name}", [T("Ambra"), T("Bianco Caldo"), T("Ghiaccio"), T("Bianco Freddo")], hold)

    if has_cmy:
        def cmy(name, colors, hold, run="Loop"):
            steps = _steps_from_names(scene_map, sep + "CMY ", colors, hold)
            add(name, steps, run_order=run)

        for spd_name, hold in [("Lento", 1500), ("Medio", 800), ("Veloce", 400)]:
            cmy(f"{T('CMY Arcobaleno')} {spd_name}",
                ["Rosso", "Arancio", "Giallo", "Verde", "Ciano", "Blu", "Indaco", "Viola", "Magenta"], hold)
        cmy(f"{T('CMY Rainbow Casuale')} {T('Veloce')}",
            ["Rosso", "Verde", "Blu", "Giallo", "Ciano", "Magenta", "Arancio", "Rosa", "Viola"], 400, run="Random")
        for spd_name, hold in [("Lento", 1000), ("Veloce", 300)]:
            cmy(f"{T('CMY Caldi')} {spd_name}", ["Rosso", "Arancio", "Gold", "Ambra", "Corallo"], hold)
            cmy(f"{T('CMY Freddi')} {spd_name}", ["Blu", "Ciano", "Teal", "Indaco", "Acquamarina"], hold)

    if has_moving:
        pos_names = [p for (p, pv, tv) in MOVING_POSITIONS
                     if pv is not None and tv is not None]
        ds_us_names = ["DS Stage Left", "DS Center", "DS Stage Right",
                       "US Stage Right", "US Center", "US Stage Left"]
        corner_names = ["DS Stage Left", "DS Stage Right",
                        "US Stage Left",  "US Stage Right"]

        def pt(name, pnames, hold, run="Loop", ping=False):
            steps = _steps_from_names(scene_map, sep, pnames, hold)
            add(name, steps,
                run_order="PingPong" if ping else run)

        for spd_name, hold in [("Lento", 3000), ("Medio", 1500), ("Veloce", 800)]:
            pt(f"{T('Position Chase DS-US')} {spd_name}", ds_us_names, hold)
            pt(f"{T('Position Chase Corner')} {spd_name}", corner_names, hold, ping=True)

        pan_names = ["Pan Far Left", "Pan Center", "Pan Far Right", "Pan Center"]
        for spd_name, hold in [("Lento", 2000), ("Medio", 1000), ("Veloce", 500)]:
            pt(f"{T('Pan Oscillazione')} {spd_name}", pan_names, hold)

        tilt_names = ["Tilt Down", "Tilt Center", "Tilt Up", "Tilt Center"]
        for spd_name, hold in [("Lento", 2000), ("Medio", 1000), ("Veloce", 500)]:
            pt(f"{T('Tilt Oscillazione')} {spd_name}", tilt_names, hold)

        all_pos_names = [p for (p, _, _) in MOVING_POSITIONS]
        for spd_name, hold in [("Medio", 2000), ("Veloce", 1000)]:
            steps = _steps_from_names(scene_map, sep, all_pos_names, hold)
            add(f"{T('Posizioni Casuali')} {spd_name}", steps, run_order="Random")

        stage_sweep = ["DS Stage Left", "DS Center", "DS Stage Right",
                       "Side Right",
                       "US Stage Right", "US Center", "US Stage Left",
                       "Side Left"]
        for spd_name, hold in [("Lento", 2500), ("Medio", 1200), ("Veloce", 600)]:
            pt(f"{T('Stage Sweep')} {spd_name}", stage_sweep, hold)
        for spd_name, hold in [("Lento", 2500), ("Medio", 1200)]:
            pt(f"{T('Stage Sweep')} PingPong {spd_name}", stage_sweep, hold, ping=True)

        aud_names = ["PT Audience", "Pan Far Left", "PT Audience",
                     "Pan Far Right", "PT Audience", "PT Balcony"]
        for spd_name, hold in [("Lento", 3000), ("Medio", 1500)]:
            pt(f"{T('Audience Scan')} {spd_name}", aud_names, hold)

        if has_rgb:
            paired = []
            pos_cycle = ["DS Stage Left", "DS Center", "DS Stage Right",
                         "US Stage Right", "US Center", "US Stage Left"]
            col_cycle = [T("Rosso"), T("Arancio"), T("Giallo"), T("Verde"), T("Ciano"), T("Blu")]
            for pos, col in zip(pos_cycle, col_cycle):
                ps = _sid(scene_map, f"{sep}{pos}")
                cs = _sid(scene_map, f"{sep}{col}")
                if ps and cs:
                    for hold in [1500]:
                        paired.append((ps, hold))
                        paired.append((cs, 0))
            if paired:
                add(T("Position + Color Chase Medio"), paired)


# ══════════════════════════════════════════════════════════════════════════════
# Chaser di gruppo / Group chasers
# ══════════════════════════════════════════════════════════════════════════════

def chasers_group(group_label, group_infos, scene_map, chaser_path, ch_list, next_id_ref):
    n     = len(group_infos)
    label = f"GRUPPO {group_label}"
    sep   = f"{label} » "

    def add(name, steps, run_order="Loop", direction="Forward",
            fade_in_mode="Default", fade_out_mode="Default"):
        if not steps:
            return
        el = make_chaser(
            fn_id=next_id_ref[0], name=f"{label} » CHR {name}",
            path=chaser_path, steps=steps,
            run_order=run_order, direction=direction,
            fade_in_mode=fade_in_mode, fade_out_mode=fade_out_mode
        )
        ch_list.append(el)
        next_id_ref[0] += 1

    single_full_ids  = []
    for gi in group_infos:
        fid  = gi["fid"]
        name = gi["fix"]["name"]
        sid  = _sid(scene_map, f"{name} » Dimmer Full")
        single_full_ids.append(sid)

    valid_seq = [(sid, gi) for sid, gi in zip(single_full_ids, group_infos) if sid]

    if valid_seq:
        for spd_name, hold in [("Lento", 2000), ("Medio", 1000),
                                ("Veloce", 500), ("Velocissimo", 200), ("Strobo", 80)]:
            steps = [(sid, hold) for sid, _ in valid_seq]
            add(f"{T('Chase Sequenziale')} {spd_name}", steps)

        for spd_name, hold in [("Lento", 1500), ("Medio", 800), ("Veloce", 400)]:
            steps = [(sid, hold) for sid, _ in valid_seq]
            add(f"{T('Chase PingPong')} {spd_name}", steps, run_order="PingPong")

        for spd_name, hold in [("Medio", 1000), ("Veloce", 500)]:
            steps = [(sid, hold) for sid, _ in valid_seq]
            add(f"{T('Chase Casuale')} {spd_name}", steps, run_order="Random")

        if n >= 3:
            for spd_name, hold in [("Lento", 1500), ("Medio", 700), ("Veloce", 300)]:
                fwd  = [(sid, hold) for sid, _ in valid_seq]
                bwd  = list(reversed(fwd[1:-1]))
                add(f"{T('Knight Rider')} {spd_name}", fwd + bwd, run_order="Loop")

        if n >= 2:
            ids = [sid for sid, _ in valid_seq]
            if ids:
                for spd_name, hold in [("Medio", 800), ("Veloce", 400)]:
                    steps = []
                    for i in range(len(ids)):
                        if i < len(ids) and ids[i]:
                            steps.append((ids[i], hold))
                    add(f"{T('Chase A Coppie')} {spd_name}", steps)

    odd_scene  = _sid(scene_map, f"{sep}Dimmer ODD Full")
    even_scene = _sid(scene_map, f"{sep}Dimmer ODD Zero")
    grp_full   = _sid(scene_map, f"{sep}Dimmer Full")
    grp_zero   = _sid(scene_map, f"{sep}Dimmer Zero") or _sid(scene_map, f"{sep}Dimmer Blackout")

    if odd_scene and even_scene:
        for spd_name, hold in [("Lento", 800), ("Medio", 400),
                                ("Veloce", 200), ("Strobo", 80)]:
            add(f"{T('ODD/EVEN Flash')} {spd_name}", [(odd_scene, hold), (even_scene, hold)])

        if grp_full and grp_zero:
            for spd_name, hold in [("Medio", 400), ("Veloce", 200)]:
                add(f"{T('ODD/EVEN + Full')} {spd_name}",
                    [(odd_scene, hold), (even_scene, hold), (grp_full, hold), (grp_zero, hold)])

    if grp_full and grp_zero:
        for spd_name, hold in CHASER_FLASH_SPEEDS:
            add(f"{T('Stomp Gruppo')} {spd_name}", [(grp_full, hold), (grp_zero, hold)])

        for spd_name, base in [("Lento", 300), ("Veloce", 80)]:
            steps = [
                (grp_full, base//3), (grp_zero, base*2),
                (grp_full, base),    (grp_zero, base//2),
                (grp_full, base//4), (grp_zero, base*4),
                (grp_full, base//3), (grp_zero, base*3),
                (grp_full, base*2),  (grp_zero, base*6),
            ]
            add(f"{T('Lightning Gruppo')} {spd_name}", steps)

        for spd_name, hold in [("Medio", 120), ("Veloce", 60)]:
            blank = hold * 5
            add(f"{T('Double Flash Gruppo')} {spd_name}",
                [(grp_full, hold), (grp_zero, hold)] * 2 + [(grp_zero, blank)])
            add(f"{T('Triple Flash Gruppo')} {spd_name}",
                [(grp_full, hold), (grp_zero, hold)] * 3 + [(grp_zero, blank)])

    has_rgb = any(gi["fc"].has_rgb for gi in group_infos)
    if has_rgb:
        def rgb_grp(name, colors, hold, run="Loop", fi=0, fo=0, fim="Default"):
            steps = _steps_from_names(scene_map, sep, colors, hold, fi, fo)
            add(name, steps, run_order=run, fade_in_mode=fim, fade_out_mode=fim)

        for spd_name, hold in CHASER_COLOR_SPEEDS:
            rgb_grp(f"{T('Arcobaleno')} {spd_name}", RGB_NAMES_ARCOBALENO, hold)
        for spd_name, hold in [("Lento", 1500), ("Medio", 800)]:
            rgb_grp(f"{T('Arcobaleno')} Smooth {spd_name}", RGB_NAMES_ARCOBALENO,
                    hold, fi=hold//2, fo=hold//2, fim="PerStep")

        for spd_name, hold in [("Lento", 1000), ("Medio", 500), ("Veloce", 200)]:
            rgb_grp(f"{T('Rainbow Completo')} {spd_name}", RGB_NAMES_FULL, hold)
        rgb_grp(f"{T('Rainbow Casuale')} {T('Veloce')}", RGB_NAMES_FULL, 400, run="Random")

        for spd_name, hold in [("Medio", 500), ("Veloce", 200)]:
            rgb_grp(f"{T('Club Colors')} {spd_name}", RGB_NAMES_CLUB, hold)
            rgb_grp(f"{T('Discoteca')} {spd_name}", RGB_NAMES_DISCOTECA, hold)
        rgb_grp(f"{T('Discoteca Casuale')}", RGB_NAMES_DISCOTECA, 300, run="Random")

        for spd_name, hold in [("Lento", 1500), ("Medio", 800), ("Veloce", 400)]:
            rgb_grp(f"{T('Pastelli')} {spd_name}", RGB_NAMES_PASTELLI, hold)
            rgb_grp(f"{T('Colori Caldi')} {spd_name}", RGB_NAMES_CALDI, hold)
            rgb_grp(f"{T('Colori Freddi')} {spd_name}", RGB_NAMES_FREDDI, hold)

        for bc_name, c1, c2 in BICOLORI:
            for spd_name, hold in [("Medio", 500), ("Veloce", 200), ("Strobo", 80)]:
                rgb_grp(f"{T('Bicolore')} {bc_name} {spd_name}", [c1, c2], hold)

        for tc_name, c1, c2, c3 in TRICOLORI:
            for spd_name, hold in [("Medio", 500), ("Veloce", 200)]:
                rgb_grp(f"{T('Tricolore')} {tc_name} {spd_name}", [c1, c2, c3], hold)

        red_id  = _sid(scene_map, f"{sep}{T('Rosso')}")
        blue_id = _sid(scene_map, f"{sep}{T('Blu')}")
        if red_id and blue_id:
            for spd_name, hold, n_rep in [("Lento", 250, 4), ("Veloce", 80, 4)]:
                steps = [(red_id, hold)] * n_rep + [(blue_id, hold)] * n_rep
                add(f"Police {spd_name}", steps)

        for spd_name, hold in [(T("Veloce"), 120), (T("Strobo"), 60)]:
            rgb_grp(f"{T('Tecno')} {spd_name}",
                    [T("Rosso"), T("Blu"), T("Verde"), T("Giallo"), T("Ciano"), T("Magenta")], hold)
        rgb_grp(T("Tecno Casuale"), [T("Rosso"), T("Blu"), T("Verde"), T("Giallo"), T("Ciano"), T("Magenta")],
                120, run="Random")

    # ── Nuovi chaser colore di gruppo / New group color chasers ──────────────────
    if has_rgb:

        # COLOR STOMP: ogni fixture lampeggia su un colore diverso in sequenza
        # COLOR STOMP: each fixture flashes on a different sequential color
        stomp_colors = RGB_NAMES_ARCOBALENO
        if len(stomp_colors) >= n and n >= 2:
            for spd_name, hold in [(T("Veloce"), 150), (T("Strobo"), 60)]:
                steps = []
                for idx, gi in enumerate(group_infos):
                    col = stomp_colors[idx % len(stomp_colors)]
                    sid = _sid(scene_map, f"{gi['fix']['name']} » {col}")
                    if sid:
                        steps.append((sid, hold))
                if steps:
                    add(f"{T('Stomp Colore')} {spd_name}", steps)

        # COLOR WAVE: onda cromatica — ogni fixture prende il colore successivo
        # COLOR WAVE: chromatic wave — each fixture takes the next rainbow color
        wave_colors = RGB_NAMES_ARCOBALENO
        if n >= 2 and len(wave_colors) >= 2:
            for spd_name, hold in [(T("Lento"), 800), (T("Medio"), 400), (T("Veloce"), 200)]:
                steps = []
                n_colors = len(wave_colors)
                for offset in range(n_colors):
                    step_block = []
                    for idx, gi in enumerate(group_infos):
                        col = wave_colors[(offset + idx) % n_colors]
                        sid = _sid(scene_map, f"{gi['fix']['name']} » {col}")
                        if sid:
                            step_block.append((sid, hold))
                    steps += step_block
                if steps:
                    add(f"{T('Onda Colore')} {spd_name}", steps)

        # SUNRISE: progressione da Rosso Scuro → Arancio → Giallo → Bianco Caldo → Bianco
        # SUNRISE: ramp from Dark Red → Orange → Yellow → Warm White → White
        _sunrise_seq = [T("Rosso"), T("Arancio"), T("Giallo"), T("Bianco Caldo"), T("Bianco")]
        for spd_name, hold in [(T("Lento"), 1500), (T("Medio"), 800)]:
            steps = _steps_from_names(scene_map, sep, _sunrise_seq, hold,
                                      fade_in=hold // 2, fade_out=hold // 2)
            add(f"{T('Alba')} {spd_name}", steps,
                fade_in_mode="PerStep", fade_out_mode="PerStep")

        # SUNDOWN: l'inverso dell'Alba — da Bianco → Giallo → Arancio → Rosso Scuro
        # SUNDOWN: reverse of Sunrise — White → Yellow → Orange → Dark Red
        _sundown_seq = list(reversed(_sunrise_seq))
        for spd_name, hold in [(T("Lento"), 1500), (T("Medio"), 800)]:
            steps = _steps_from_names(scene_map, sep, _sundown_seq, hold,
                                      fade_in=hold // 2, fade_out=hold // 2)
            add(f"{T('Tramonto')} {spd_name}", steps,
                fade_in_mode="PerStep", fade_out_mode="PerStep")

        # SPLIT COLORS: fixture dispari = colori caldi, pari = colori freddi, alternati
        # SPLIT COLORS: odd fixtures = warm colors, even fixtures = cool colors, alternating
        odds  = group_infos[0::2]
        evens = group_infos[1::2]
        if evens:
            warm_colors = [c for c in RGB_NAMES_CALDI if _sid(scene_map, f"{sep}{c}")]
            cool_colors = [c for c in RGB_NAMES_FREDDI if _sid(scene_map, f"{sep}{c}")]
            if warm_colors and cool_colors:
                for spd_name, hold in [(T("Lento"), 1200), (T("Medio"), 600)]:
                    steps = []
                    cycles = min(len(warm_colors), len(cool_colors), 6)
                    for i in range(cycles):
                        wc = warm_colors[i % len(warm_colors)]
                        cc = cool_colors[i % len(cool_colors)]
                        for gi in group_infos:
                            idx = group_infos.index(gi)
                            col = wc if idx % 2 == 0 else cc
                            sid = _sid(scene_map, f"{gi['fix']['name']} » {col}")
                            if sid:
                                steps.append((sid, hold))
                    if steps:
                        add(f"{T('Split Colori')} {spd_name}", steps)


    if has_rgb:
        ripple_colors = RGB_NAMES_ARCOBALENO
        for spd_name, hold in [("Medio", 600), ("Veloce", 300)]:
            steps = []
            for offset in range(len(ripple_colors)):
                col = ripple_colors[offset % len(ripple_colors)]
                sid = _sid(scene_map, f"{sep}{col}")
                if sid:
                    steps.append((sid, hold))
            add(f"{T('Ripple Colori')} {spd_name}", steps)

    has_moving = any(gi["fc"].has_moving for gi in group_infos)
    if has_moving:
        ds_us = ["DS Stage Left", "DS Center", "DS Stage Right",
                 "US Stage Right", "US Center", "US Stage Left"]
        for spd_name, hold in [("Lento", 3000), ("Medio", 1500), ("Veloce", 800)]:
            steps = _steps_from_names(scene_map, sep, ds_us, hold)
            add(f"{T('PT Chase Palco')} {spd_name}", steps)

        corner = ["DS Stage Left", "DS Stage Right", "US Stage Left", "US Stage Right"]
        for spd_name, hold in [("Lento", 2500), ("Medio", 1200), ("Veloce", 600)]:
            steps = _steps_from_names(scene_map, sep, corner, hold)
            add(f"{T('PT Corner Chase')} {spd_name}", steps)
            add(f"{T('PT Corner PingPong')} {spd_name}", steps, run_order="PingPong")

        all_pos = [p for (p, _, _) in MOVING_POSITIONS]
        for spd_name, hold in [("Medio", 2000), ("Veloce", 1000)]:
            steps = _steps_from_names(scene_map, sep, all_pos, hold)
            add(f"{T('PT Posizioni Casuali')} {spd_name}", steps, run_order="Random")

    if valid_seq and n >= 3:
        for spd_name, hold in [("Lento", 1000), ("Medio", 500)]:
            steps = [(sid, hold) for sid, _ in valid_seq]
            add(f"{T('Waterfall')} {spd_name}", steps)




# ══════════════════════════════════════════════════════════════════════════════
# Chaser globali (tutte le fixture) / Global chasers (all fixtures)
# IT: Chasers che coinvolgono tutte le fixture del progetto simultaneamente,
#     usando le scene GLOBAL pregenerate.
# EN: Chasers involving all project fixtures simultaneously,
#     using pre-generated GLOBAL scenes.
# ══════════════════════════════════════════════════════════════════════════════

def chasers_global(scene_map, fixtures_info, rgb_info, all_shutter_info,
                   all_dimmer_vals, ch_list, next_id_ref):
    """
    IT: Genera chaser globali che agiscono su tutte le fixture insieme.
    EN: Generates global chasers that act on all fixtures together.
    """
    gpath = "Auto Palette/CHASER/GLOBAL"

    def add(name, steps, run_order="Loop", fade_in_mode="Default", fade_out_mode="Default"):
        if not steps:
            return
        el = make_chaser(
            fn_id=next_id_ref[0], name=f"GLOBAL » CHR {name}",
            path=gpath, steps=steps,
            run_order=run_order,
            fade_in_mode=fade_in_mode, fade_out_mode=fade_out_mode
        )
        ch_list.append(el)
        next_id_ref[0] += 1

    def gs(name):
        """Shortcut: restituisce l'ID della scena GLOBAL con questo nome.
        Shortcut: returns the ID of the GLOBAL scene with this name."""
        return _sid(scene_map, f"GLOBAL » {name}")

    has_rgb     = bool(rgb_info)
    has_dimmer  = bool(all_dimmer_vals)
    has_shutter = bool(all_shutter_info)

    # ── GLOBAL dimmer: stomp / heartbeat / strobe ──────────────────────────────
    g_full = gs("Dimmer Full")
    g_zero = gs("Dimmer Zero")
    g_50   = gs("Dimmer 50%")
    g_25   = gs("Dimmer 25%")
    g_75   = gs("Dimmer 75%")

    if g_full and g_zero:
        # Stomp globale / Global stomp
        for spd_name, hold in [(T("Lento"), 600), (T("Medio"), 300),
                                (T("Veloce"), 120), (T("Strobo"), 50)]:
            add(f"{T('Stomp Globale')} {spd_name}", [(g_full, hold), (g_zero, hold)])

        # Battito globale / Global heartbeat
        if g_25 and g_75:
            for spd_name, hold in [(T("Lento"), 600), (T("Medio"), 280)]:
                steps = []
                if g_25: steps.append((g_25, hold))
                if g_75: steps.append((g_75, hold))
                steps.append((g_full, hold * 2))
                if g_75: steps.append((g_75, hold))
                if g_25: steps.append((g_25, hold))
                steps.append((g_zero, hold * 3))
                add(f"{T('Battito Globale')} {spd_name}", steps)

        # Impulso globale / Global pulse
        for spd_name, hold in [(T("Lento"), 1200), (T("Medio"), 600), (T("Veloce"), 250)]:
            add(f"{T('Impulso Globale')} {spd_name}",
                [(g_full, hold), (g_zero, hold * 2)], run_order="Loop")

    # ── GLOBAL shutter strobe ─────────────────────────────────────────────────
    g_sopen = gs(T("All Shutter Aperto"))
    g_sclose = gs(T("All Shutter Chiuso"))
    if g_sopen and g_sclose:
        add(f"{T('Strobo Globale')} {T('Lento')}",  [(g_sopen, 300), (g_sclose, 300)])
        add(f"{T('Strobo Globale')} {T('Medio')}",  [(g_sopen, 100), (g_sclose, 100)])
        add(f"{T('Strobo Globale')} {T('Veloce')}", [(g_sopen,  40), (g_sclose,  40)])

    # ── GLOBAL colori RGB ─────────────────────────────────────────────────────
    if has_rgb:
        def gc(name):
            """Scena GLOBAL colore. / GLOBAL color scene."""
            return gs(name)

        def rgbg(name, color_names, hold, run="Loop", fi=0, fo=0, fim="Default"):
            steps = []
            for c in color_names:
                sid = gc(c)
                if sid:
                    steps.append((sid, hold, fi, fo))
            add(name, steps, run_order=run, fade_in_mode=fim, fade_out_mode=fim)

        # Arcobaleno globale / Global rainbow
        for spd_name, hold in [(T("Lento"), 1500), (T("Medio"), 800),
                                (T("Veloce"), 400), (T("Strobo"), 80)]:
            rgbg(f"{T('Arcobaleno Globale')} {spd_name}", RGB_NAMES_ARCOBALENO, hold)

        for spd_name, hold in [(T("Lento"), 1500), (T("Medio"), 800)]:
            rgbg(f"{T('Arcobaleno Globale')} Smooth {spd_name}", RGB_NAMES_ARCOBALENO,
                 hold, fi=hold // 2, fo=hold // 2, fim="PerStep")

        # Polizia globale / Global police
        r_id = gc(T("Rosso"))
        b_id = gc(T("Blu"))
        if r_id and b_id:
            for spd_name, hold, reps in [(T("Lento"), 250, 4), (T("Veloce"), 80, 4)]:
                steps = [(r_id, hold)] * reps + [(b_id, hold)] * reps
                add(f"{T('Polizia Globale')} {spd_name}", steps)

        # Alba globale / Global sunrise
        _sun = [T("Rosso"), T("Arancio"), T("Giallo"), T("Bianco Caldo"), T("Bianco")]
        for spd_name, hold in [(T("Lento"), 2000), (T("Medio"), 1000)]:
            steps = [(gc(c), hold, hold // 2, hold // 2) for c in _sun if gc(c)]
            add(f"{T('Alba Globale')} {spd_name}", steps,
                fade_in_mode="PerStep", fade_out_mode="PerStep")

        # Colori caldi globali / Global warm colors
        rgbg(f"{T('Colori Caldi')} Globale {T('Medio')}", RGB_NAMES_CALDI, 800)
        rgbg(f"{T('Colori Freddi')} Globale {T('Medio')}", RGB_NAMES_FREDDI, 800)

        # Club colors / Discoteca globali
        rgbg(f"{T('Club Colors')} Globale {T('Veloce')}", RGB_NAMES_CLUB, 200)
        rgbg(f"{T('Discoteca')} Globale {T('Veloce')}", RGB_NAMES_DISCOTECA, 200)

# ══════════════════════════════════════════════════════════════════════════════
# Orchestratore Chaser / Chaser orchestrator
# ══════════════════════════════════════════════════════════════════════════════

def generate_chasers(scene_map, fixtures_info, by_model, cfg, next_id_ref,
                       rgb_info=None, all_shutter_info=None, all_dimmer_vals=None):
    """
    IT: Genera tutti i chaser: singola fixture, gruppi e (novità v1.1) globali.
    EN: Generates all chasers: single fixture, groups and (new in v1.1) global ones.

    scene_map:        dict  nome_scena → function_id
    fixtures_info:    lista di {"fid":…, "fix":…, "fc":…}
    by_model:         dict  (mfr, mdl, mode, channels) → [fixture_info, …]
    rgb_info:         lista di {"fid":…, "fc":…} per fixture con RGB (per chaser globali)
    all_shutter_info: lista di (fid, ch_num, info) per chaser strobe globali
    all_dimmer_vals:  lista di (fid, ch_num) per chaser dimmer globali
    """
    ch_list = []

    for gi in fixtures_info:
        fid    = gi["fid"]
        fc     = gi["fc"]
        prefix = gi["fix"]["name"]
        cpath  = f"Auto Palette/CHASER/{prefix}"
        chasers_single_fixture(fid, prefix, fc, scene_map, cpath, ch_list, next_id_ref)

    if not cfg.get("skip_groups"):
        # IT: La chiave è una 4-tupla: (manufacturer, model, mode, channels)
        # EN: Key is a 4-tuple: (manufacturer, model, mode, channels)
        for (mfr, mdl, mode, channels), group in by_model.items():
            if len(group) < 2:
                continue
            # Label leggibile: aggiunge il mode se informativo
            # Readable label: adds mode if informative
            group_label = f"{mdl} ({mode})" if mode and mode != mdl else mdl
            cpath = f"Auto Palette/CHASER/GRUPPI/{group_label}"
            chasers_group(group_label, group, scene_map, cpath, ch_list, next_id_ref)

    # ── Chaser GLOBALI (tutte le fixture) / GLOBAL chasers (all fixtures) ─────────
    if not cfg.get("skip_groups"):
        chasers_global(
            scene_map, fixtures_info,
            rgb_info or [],
            all_shutter_info or [],
            all_dimmer_vals or [],
            ch_list, next_id_ref
        )

    return ch_list


# ══════════════════════════════════════════════════════════════════════════════
# Main / Entry point
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="QLC+ Auto Palette FX Engine v1.1alpha by Marco Coldagelli",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input",            help="File .qxw di input")
    parser.add_argument("--output",         help="File .qxw di output (default: input_palette.qxw)")
    parser.add_argument("--fixture-dir",    help="Directory aggiuntiva con i file .qxf")
    parser.add_argument("--fade-in",  type=int, default=0,
                        help="FadeIn delle scene in ms (default 0)")
    parser.add_argument("--fade-out", type=int, default=2000,
                        help="FadeOut delle scene in ms (default 2000)")
    parser.add_argument("--overwrite",    action="store_true",
                        help="Sovrascrive funzioni con lo stesso nome se già presenti")
    parser.add_argument("--skip-groups",  action="store_true",
                        help="Non genera scene/EFX/Chaser di gruppo")
    parser.add_argument("--skip-combos", action="store_true",
                        help="Non genera scene combo")
    parser.add_argument("--skip-efx",    action="store_true",
                        help="Non genera funzioni EFX di movimento")
    parser.add_argument("--skip-chasers", action="store_true",
                        help="Non genera Chaser (sequenze di effetti)")
    parser.add_argument("--min-cap-scenes", type=int, default=2,
                        help="Min capability per generare scene (color wheel/gobo/effect), default 2")
    parser.add_argument("--lang", choices=["it", "en"], default="it",
                        help="Lingua delle scene generate: it=Italiano (default), en=English")
    args = parser.parse_args()

    global LANG
    LANG = args.lang
    _init_lang()  # reinizializza tutte le costanti lingua-dipendenti

    input_path  = args.input
    output_path = args.output or input_path.replace(".qxw", "_palette.qxw")

    if not os.path.isfile(input_path):
        print(f"Errore: file '{input_path}' non trovato.")
        sys.exit(1)

    print(f"\n{'═'*64}")
    print(f"  QLC+ Auto Palette FX Engine v1.1alpha by Marco Coldagelli")
    print(f"  Language / Lingua: {LANG.upper()}")
    print(f"{'═'*64}")
    print(f"  Input : {input_path}")
    print(f"  Output: {output_path}")

    qxw_root = strip_ns(safe_xml_parse(input_path))
    _eng = qxw_root.find("Engine"); engine = _eng if _eng is not None else qxw_root

    fixture_dirs = find_fixture_dirs(args.fixture_dir)
    if not fixture_dirs:
        print("\n[ERRORE] Nessuna directory fixture QLC+ trovata!")
        print("  Specifica il percorso con --fixture-dir /path/to/fixtures")
        sys.exit(1)

    print(f"\n  Fixture dirs:")
    for d in fixture_dirs:
        print(f"    • {d}")

    fixtures_data = parse_qxw_fixtures(qxw_root)
    print(f"\n  Fixture patchate: {len(fixtures_data)}")
    for f in fixtures_data:
        print(f"    [{f['id']:3d}] {f['name']:<30}  {f['manufacturer']} {f['model']} "
              f"({f['mode']})  U{f['universe']+1}@{f['address']+1}")

    if not fixtures_data:
        print("\n[ERRORE] Nessuna fixture trovata nel file .qxw")
        sys.exit(1)

    cfg = {
        "skip_groups":    args.skip_groups,
        "skip_combos":    args.skip_combos,
        "skip_efx":       args.skip_efx,
        "min_cap_scenes": args.min_cap_scenes,
    }

    print(f"\n  Generazione palette in corso...")
    scenes, efx_elements, fixtures_info, by_model, rgb_info, all_shutter_info, all_dimmer_vals = generate_palettes(
        fixtures_data, fixture_dirs, cfg
    )

    existing_by_name = {}
    for fn in engine.findall("Function"):
        existing_by_name[fn.get("Name", "")] = fn

    next_id  = get_next_function_id(qxw_root)
    scene_map = {}
    added_scenes = skipped_scenes = 0
    new_functions   = []
    names_overwrite = set()

    print(f"\n  ── Passata 1: Scene statiche ──")
    for (scene_name, scene_path, channel_values) in scenes:
        if not channel_values:
            continue
        if scene_name in existing_by_name:
            if args.overwrite:
                names_overwrite.add(scene_name)
            else:
                scene_map[scene_name] = int(existing_by_name[scene_name].get("ID", -1))
                skipped_scenes += 1
                continue
        fn_el = make_scene(
            next_id, scene_name, channel_values,
            path=scene_path,
            fade_in=args.fade_in,
            fade_out=args.fade_out
        )
        new_functions.append(fn_el)
        scene_map[scene_name] = next_id
        print(f"    + [{next_id:5d}] {scene_name}")
        next_id += 1
        added_scenes += 1

    added_efx = skipped_efx = 0
    if efx_elements:
        print(f"\n  ── Passata 2: EFX di movimento ──")
        for efx_el in efx_elements:
            efx_name = efx_el.get("Name", "")
            if efx_name in existing_by_name:
                if args.overwrite:
                    names_overwrite.add(efx_name)
                else:
                    skipped_efx += 1
                    continue
            efx_el.set("ID", str(next_id))
            new_functions.append(efx_el)
            print(f"    ~ [{next_id:5d}] {efx_name}")
            next_id += 1
            added_efx += 1

    added_chasers = skipped_chasers = 0
    if not args.skip_chasers:
        print(f"\n  ── Passata 3: Chaser (sequenze effetti) ──")
        next_id_ref = [next_id]
        chasers = generate_chasers(
            scene_map, fixtures_info, by_model, cfg, next_id_ref,
            rgb_info=rgb_info,
            all_shutter_info=all_shutter_info,
            all_dimmer_vals=all_dimmer_vals
        )
        next_id = next_id_ref[0]

        for ch_el in chasers:
            ch_name = ch_el.get("Name", "")
            if ch_name in existing_by_name:
                if args.overwrite:
                    names_overwrite.add(ch_name)
                else:
                    skipped_chasers += 1
                    continue
            new_functions.append(ch_el)
            print(f"    ≫ [{ch_el.get('ID'):>5}] {ch_name}")
            added_chasers += 1

    import re as _re

    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        file_text = f.read()

    for fn_name in names_overwrite:
        escaped = _re.escape(fn_name)
        pattern = rf'\s*<Function\b[^>]*\bName="{escaped}"[^>]*>.*?</Function>'
        file_text = _re.sub(pattern, "", file_text, flags=_re.DOTALL)

    if new_functions:
        xml_parts = []
        for fn_el in new_functions:
            indent_xml(fn_el)
            xml_str = ET.tostring(fn_el, encoding="unicode")
            xml_str = "\n".join(
                "  " + line if line.strip() else line
                for line in xml_str.splitlines()
            )
            xml_parts.append(xml_str)
        insert_block = "\n".join(xml_parts) + "\n"

        insert_pos = -1
        for closing_tag in ["</Engine>", "</qlcplus:Engine>"]:
            insert_pos = file_text.rfind(closing_tag)
            if insert_pos != -1:
                file_text = (file_text[:insert_pos]
                             + insert_block
                             + file_text[insert_pos:])
                break
        if insert_pos == -1:
            print("\n[ERRORE] Tag </Engine> non trovato nel file di input!")
            sys.exit(1)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(file_text)

    print(f"\n{'─'*64}")
    print(f"  Scene    aggiunte : {added_scenes:4d}  (saltate: {skipped_scenes})")
    print(f"  EFX      aggiunti : {added_efx:4d}  (saltati: {skipped_efx})")
    print(f"  Chaser   aggiunti : {added_chasers:4d}  (saltati: {skipped_chasers})")
    print(f"  Output            : {output_path}")
    if skipped_scenes or skipped_efx or skipped_chasers:
        print(f"  → usa --overwrite per aggiornare le funzioni già presenti")
    print(f"{'═'*64}\n")


if __name__ == "__main__":
    main()
