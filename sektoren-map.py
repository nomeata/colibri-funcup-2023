#!/usr/bin/env python3

import folium
import math
import sys
import subprocess
import igc
import json

from constants import *
import sektoren
import landepunkt


m = folium.Map(
    location=schaui,
    zoom_start=12,
    tiles = 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    maxZoom = 17,
    attr = 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
    )

# Draw sektoren
folium.features.GeoJson(data = "sektoren.json", embed=False).add_to(m)

# Draw flights
seen = set()
outfile = sys.argv[1]
for file in sys.argv[2:]:
    # Track
    gunzip = subprocess.Popen(('gunzip',), stdin=open(file), stdout=subprocess.PIPE)
    track = igc.parse(gunzip.stdout)
    points = [ (round(p['lat'],5), round(p['lon'],5)) for p in track ][::5]
    folium.PolyLine(points, color="crimson").add_to(m)

    # Draw Landepunkt
    stats = json.load(open(file.removesuffix('.igc.gz') + '.stats.json'))
    folium.Marker(stats['landepunkt']).add_to(m)
    # Remember segments
    seen.update(stats['sektoren'])

# mark segments
for s in seen:
  p = sektoren.midpoint(sektoren.parsesektorname(s))
  folium.CircleMarker(radius=10, location=(p[1], p[0]), color="green", fill=True).add_to(m)

m.save(outfile)
