#!/usr/bin/env python3

from sektoren import *
from constants import *

from pyopenair.helper import generate_coords

nmPerm = 0.000539957

smoothness = 2

for i in range(rings-1):
    if i == 0:
        r = radius[0]
        print(f"""
AC W
AN {sektorname((0,0))}
V x={generate_coords(lonlat(schaui))}
DC {r * nmPerm}

""")
    else:
        r     = radius[i-1]
        rnext = radius[i]
        segs  = segments[i-1]
        o     = offset[i-1]

        for si in range(segs):
            bearing1 = o + si * 360 / segs
            bearing2 = o + (si + 1) * 360 / segs

            print(f"""
AC W
AN {sektorname((i,si))}
V D=-
V x={generate_coords(lonlat(schaui))}
DC {r * nmPerm} {bearing1} {bearing2}
V D=+
DC {rnext * nmPerm} {bearing2} {bearing1}

""")
