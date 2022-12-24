#!/usr/bin/env python3

import math
import sys
import subprocess
import igc
import argparse
import json

from constants import *
import kreise
import sektoren
import landepunkt

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('-i', type=str, help='Gzipped IGC file to read', required=True)
args = parser.parse_args()

gunzip = subprocess.Popen(('gunzip',), stdin=open(args.i), stdout=subprocess.PIPE)
#gpsbabel = subprocess.Popen(('gpsbabel', '-i', 'igc', '-o', 'gpx', '-f', '-', '-F', '-'), stdin=gunzip.stdout, stdout=subprocess.PIPE)
track = igc.parse(gunzip.stdout)

p = landepunkt.landepunkt(track)
landepunktabstand = landepunkt.landepunktabstand(p)
turns = kreise.turns(track)
seen = sektoren.sektoren(track)


json.dump({
    'left_turns': turns['left_turns'],
    'right_turns': turns['right_turns'],
    'sektoren': sorted([ sektoren.sektorname(isi) for isi in seen]),
    'landepunkt': p,
    'landepunktabstand': landepunktabstand,
}, sys.stdout, indent=True)
