#!/usr/bin/env python3

from sektoren import *
from constants import *

from pyopenair.helper import generate_coords

for i in range(rings-1):
    for (name, ps) in sektoren_daten():
        print(f"""AC W
AN {name}
AL 0
AH UNLIM
""")
        for p in ps:
            print(generate_coords(lonlat(p)))
        print("")
