#!/usr/bin/env python3

import pandas as pd
import folium
import math
import sys
import subprocess
import igc
import json
import os

import constants
from constants import *
import sektoren
import landepunkt


def write_map(outfile, flights):
    print(f"Writing {outfile}")

    # Read flights
    tracks = []
    seen = set()
    lps = []
    for flight in flights:
        id = flight['IDFlight']

        # Track
        gunzip = subprocess.Popen(('gunzip',), stdin=open(f'_flights/{id}.igc.gz'), stdout=subprocess.PIPE)
        track = igc.parse(gunzip.stdout)
        tracks += [ [(round(p['lat'],5), round(p['lon'],5)) for p in track ][::5] ]

        # Remember landepunkte and segments
        stats = json.load(open(f'_stats/{id}.stats.json'))
        lps += [ stats['landepunkt'] ]
        seen.update(stats['sektoren'])

    # Create map
    m = folium.Map(
        location=schaui,
        zoom_start=12,
        tiles = None,
        )

    tile_layer = folium.TileLayer(
        tiles = 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attr = 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
        max_zoom=17,
        name='OpenTopoMap',
        control=False,
    )
    tile_layer.add_to(m)


    # Draw sektoren
    # Only draw those that are actually seen
    def style_function(feature):
        if feature['id'] in seen:
            return { 'weight': 2 }
        else:
            return {'fill': False, 'stroke': False}

    sektoren_layer = folium.FeatureGroup(name="Sektoren").add_to(m)
    folium.features.GeoJson(
     data = "sektoren.json",
     style_function = style_function,
     overlay = False,
    ).add_to(sektoren_layer)

    # Draw target
    target_layer = folium.FeatureGroup(name="Zielscheibe").add_to(m)
    for r in [lpradius1, lpradius2, lpradius3]:
        folium.Circle(radius = r, location=constants.landepunkt, color = 'green', fill=True).add_to(target_layer)

    # Draw tracks
    track_layer = folium.FeatureGroup(name="Tracks").add_to(m)
    for track in tracks:
        folium.PolyLine([track], color="crimson").add_to(track_layer)

    # Draw Landepunkt
    landing_layer = folium.FeatureGroup(name="Landepunkte").add_to(m)
    for lp in lps:
        folium.Circle(radius = 3, location = lp, color="black", fill=True, fill_opacity = 1, stroke=False).add_to(landing_layer)

    folium.LayerControl(collapsed = False).add_to(m)

    m.save(outfile)

# Read flight data, grouped by pilot

print("Reading _tmp/flights.json")
flight_data = json.load(open('_tmp/flights.json'))

flights = {}
all_flights = []

for flight in flight_data['data']:
    id = flight['IDFlight']
    pid = flight['FKPilot']

    if len(sys.argv) > 1:
        if pid not in sys.argv[1:]:
            continue

    if pid not in flights:
        flights[pid] = []
    flights[pid].append(flight)
    all_flights.append(flight)

for pid, pflights in flights.items():
    write_map(f"_out/map{pid}.html", pflights)

if not len(sys.argv) > 1:
    write_map(f"_out/map_all.html", all_flights)

