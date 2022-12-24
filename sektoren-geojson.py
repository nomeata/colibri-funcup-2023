#!/usr/bin/env python3
import sys
import json
import sektoren
json.dump(sektoren.geojson(), sys.stdout)
