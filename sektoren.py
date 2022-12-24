from geographiclib.geodesic import Geodesic
import math

from constants import *

def sektorname(s):
    return chr(ord('A') + s[0]) + str(s[1]+1)

def sektoren(track):
    seen = set()
    for point in track:
        g = Geodesic.WGS84.Inverse(schaui[0], schaui[1],  point['lat'], point['lon'])
        phi = g['azi1']
        d = g['s12']/1000

        if d < r0:
            seen.add((0,0))
        else:
            for i in range(1,rings):
                r     = radius[i-1]
                rnext = radius[i]
                s     = segments[i-1]
                o     = offset[i-1]

                if r <= d and d < rnext:
                    si = int((360 + (phi - o)) // (360/s)) % s
                    seen.add((i,si))
                    break

    return sorted(list(seen))


def point(bearing, r):
    g = Geodesic.WGS84.Direct(schaui[0], schaui[1], bearing, r)
    return (round(g['lon2'],4), round(g['lat2'],4))

def geojson():
    lines = []
    radius = [r0 + dr0 * (drf**i - 1)/(drf-1) for i in range(rings) ]
    segments = [ 2**(round(math.log(2*math.pi*(radius[i]+radius[i+1])/2 / (radius[i+1]-radius[i]), 2))) for i in range(rings-1) ]
    offset = [0 for i in range(rings-1)]
    for i in range(1,rings-1):
        offset[i] = offset[i-1] + 0.5 * 260/segments[i]

    for i in range(rings):
        r     = radius[i]

        arcpoints = 3*32 #  math.floor((r * 1000 * math.pi * 2) // 200)
        ps = [ point(bearing * 360 / arcpoints, r*1000) for bearing in range(0, arcpoints) ]
        ps.append(ps[0])
        lines.append(ps)

        if i + 1 < rings:
            s     = segments[i]
            o     = offset[i]
            rnext = radius[i+1]
            for si in range(s):
                bearing = o + si * 360 / s
                lines.append( [ point(bearing, r*1000), point(bearing, rnext*1000) ])

    return {
      "type": "FeatureCollection",
      "features": [
        # { "type": "MultiPolygon", "coordinates": [ [ps] for ps in polygons], },
        { "type": "MultiLineString", "coordinates": lines, },
      ]
    }
