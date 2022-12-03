#!/usr/bin/env python3

import folium
# import geopy.distance
from geographiclib.geodesic import Geodesic
import math
import sys
import subprocess
import gpxpy

from constants import *
import sektoren
import landepunkt

m = folium.Map(location=schaui, zoom_start=12)

radius = [r0 + dr0 * (drf**i - 1)/(drf-1) for i in range(rings) ]
segments = [ 2**(round(math.log(2*math.pi*(radius[i]+radius[i+1])/2 / (radius[i+1]-radius[i]), 2))) for i in range(rings-1) ]
offset = [0 for i in range(rings-1)]
for i in range(1,rings-1):
    offset[i] = offset[i-1] + 0.5 * 260/segments[i]

for i in range(rings):
    r     = radius[i]

    folium.Circle(
        radius=r*1000,
        location=schaui,
        fill=False,
    ).add_to(m)
    if i + 1 < rings:
        s     = segments[i]
        o     = offset[i]
        rnext = radius[i+1]
        for si in range(s):
            bearing = o + si * 360 / s
            g1 = Geodesic.WGS84.Direct(schaui[0], schaui[1], bearing, r*1e3)
            g2 = Geodesic.WGS84.Direct(schaui[0], schaui[1], bearing, rnext*1e3)
            folium.PolyLine([(g1['lat2'],g1['lon2']), (g2['lat2'],g2['lon2'])]).add_to(m)

# Draw flights, note segments

seen = set()
for file in sys.argv[1:]:
    gunzip = subprocess.Popen(('gunzip',), stdin=open(file), stdout=subprocess.PIPE)
    gpsbabel = subprocess.Popen(('gpsbabel', '-i', 'igc', '-o', 'gpx', '-f', '-', '-F', '-'), stdin=gunzip.stdout, stdout=subprocess.PIPE)
    gpx = gpxpy.parse(gpsbabel.stdout)
    points = [ (point.latitude, point.longitude) for track in gpx.tracks if track.name != "PRESALTTRK" for segment in track.segments for point in segment.points ]
    folium.PolyLine(points, color="crimson").add_to(m)

    p = landepunkt.landepunkt(gpx)
    folium.Marker(p).add_to(m)

    seen.update(sektoren.sektoren(gpx))

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
    g = Geodesic.WGS84.Direct(schaui[0], schaui[1], bearing, (r + rnext)/2*1e3)
    folium.CircleMarker((g['lat2'],g['lon2']),radius=10,color="green").add_to(m)

m.save("sektoren.html")
