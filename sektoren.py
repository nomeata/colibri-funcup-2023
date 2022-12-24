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
