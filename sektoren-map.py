#!/usr/bin/env python3

import folium
# import geopy.distance
from geographiclib.geodesic import Geodesic
import math
import sys
import subprocess
import igc

from constants import *
import sektoren
import landepunkt

m = folium.Map(location=schaui, zoom_start=12)

folium.features.GeoJson(data = "sektoren.json", embed=False).add_to(m)

radius = [r0 + dr0 * (drf**i - 1)/(drf-1) for i in range(rings) ]
segments = [ 2**(round(math.log(2*math.pi*(radius[i]+radius[i+1])/2 / (radius[i+1]-radius[i]), 2))) for i in range(rings-1) ]
offset = [0 for i in range(rings-1)]
for i in range(1,rings-1):
    offset[i] = offset[i-1] + 0.5 * 260/segments[i]


# Draw flights, note segments

seen = set()
outfile = sys.argv[1]
for file in sys.argv[2:]:
    gunzip = subprocess.Popen(('gunzip',), stdin=open(file), stdout=subprocess.PIPE)
    track = igc.parse(gunzip.stdout)
    points = [ (round(p['lat'],4), round(p['lon'],4)) for p in track ]
    folium.PolyLine(points, color="crimson").add_to(m)

    p = landepunkt.landepunkt(track)
    folium.Marker(p).add_to(m)

    seen.update(sektoren.sektoren(track))

# mark segments
for (i, si) in seen:
  if i == 0:
    folium.CircleMarker(
        radius=10,
        location=schaui,
        color="green",
        fill=True,
    ).add_to(m)
  else:
    r     = radius[i-1]
    rnext = radius[i]
    s     = segments[i-1]
    o     = offset[i-1]

    bearing = o + (si + 0.5) * 360 / s
    p = sektoren.point(bearing, (r + rnext)/2*1e3)
    folium.CircleMarker(p,radius=10,color="green").add_to(m)

m.save(outfile)
