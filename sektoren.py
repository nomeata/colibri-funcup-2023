from geographiclib.geodesic import Geodesic
import math

from constants import *

def sektorname(s):
    return chr(ord('A') + s[0]) + str(s[1]+1)

def parsesektorname(s):
    i = ord(s[0]) - ord('A')
    si = int(s[1:]) - 1
    assert s == sektorname((i, si))
    return (i,si)

def sektor_of_point(point):
    g = Geodesic.WGS84.Inverse(schaui[0], schaui[1], point[0], point[1])
    phi = g['azi1']
    d = g['s12']/1000

    if d < r0:
        return (0,0)
    else:
        for i in range(1,rings):
            r     = radius[i-1]
            rnext = radius[i]
            s     = segments[i-1]
            o     = offset[i-1]

            if r <= d and d < rnext:
                si = int((360 + (phi - o)) // (360/s)) % s
                return (i,si)

def sektoren(track):
    seen = set()
    for point in track:
        sektor = sektor_of_point((point['lat'],point['lon']))
        if sektor:
            seen.add(sektor)
    return sorted(list(seen))


def point(bearing, r):
    g = Geodesic.WGS84.Direct(schaui[0], schaui[1], bearing, r)
    return (round(g['lat2'],5), round(g['lon2'],5))

# for geojson
def lonlat(p):
    return (p[1], p[0])


def midpoint(s):
    if s[0] == 0:
        return schaui
    else:
        r     = radius[s[0]-1]
        rnext = radius[s[0]]
        segs  = segments[s[0]-1]
        o     = offset[s[0]-1]

        bearing = o + (s[1] + 0.5) * 360 / segs
        p = point(bearing, (r + rnext)/2*1e3)
        assert (sektor_of_point(p) == s)
        return p

def sektoren_daten():
    sektoren = []
    smoothness = 2

    for i in range(rings-1):
        if i == 0:
            r = radius[0]
            pts = smoothness * segments[0]
            ps = [ point(bearing * 360 / pts, r*1000) for bearing in range(pts) ]

            sektoren += [(sektorname((0,0)), ps)]
        else:
            r     = radius[i-1]
            rnext = radius[i]
            segs  = segments[i-1]
            o     = offset[i-1]

            for si in range(segs):
                bearing = o + si * 360 / segs

                bearings_inner = [ bearing + db/smoothness * 360/segs
                  for db in range(smoothness+1) ]

                outer_smootheness = smoothness
                if segments[i] > segs:
                    outer_smootheness = 2 * smoothness
                bearings_outer = [ bearing + db/outer_smootheness * 360/segs
                  for db in range(outer_smootheness+1) ]
                bearings_outer.reverse()

                ps = [ point(b, r*1000) for b in bearings_inner ] + \
                     [ point(b, rnext*1000) for b in bearings_outer ]
                sektoren += [( sektorname((i,si)), ps)]

    return sektoren

def geojson():
    return {
      "type": "FeatureCollection",
      "features": [
        { "type": "Feature",
          "id": name,
          "geometry": {
              "type": "Polygon",
              "coordinates": [list(map(lonlat, ps))],
          }
        } for (name, ps) in sektoren_daten()
      ]
    }
