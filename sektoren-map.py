#!/usr/bin/env python3

import pandas as pd
import folium
import math
import sys
import subprocess
import igc
import json

import constants
from constants import *
import sektoren
import landepunkt

outfile = sys.argv[1]

# Read flights
tracks = []
seen = set()
lps = []
for file in sys.argv[2:]:
    # Track
    gunzip = subprocess.Popen(('gunzip',), stdin=open(file), stdout=subprocess.PIPE)
    track = igc.parse(gunzip.stdout)
    tracks += [ [(round(p['lat'],5), round(p['lon'],5)) for p in track ][::5] ]

    # Remember landepunkte and segments
    stats = json.load(open(file.removesuffix('.igc.gz') + '.stats.json'))
    lps += [ stats['landepunkt'] ]
    seen.update(stats['sektoren'])

m = folium.Map(
    location=schaui,
    zoom_start=12,
    tiles = 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    maxZoom = 17,
    attr = 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
    )

# Draw sektoren
# Only draw those that are actually seen
def style_function(feature):
    if feature['id'] in seen:
        return { 'weight': 2 }
    else:
        return {'fill': False, 'stroke': False}

folium.features.GeoJson(
 data = "sektoren.json",
 style_function = style_function,
 overlay = False,
).add_to(m)

# Draw target
for r in [lpradius1, lpradius2, lpradius3]:
    folium.Circle(radius = r, location=constants.landepunkt, color = 'green', fill=True).add_to(m)

# Draw tracks
for track in tracks:
    folium.PolyLine([track], color="crimson").add_to(m)

# Draw Landepunkt
for lp in lps:
    folium.Circle(radius = 3, location = lp, color="black", fill=True, fill_opacity = 1, stroke=False).add_to(m)


m.save(outfile)
