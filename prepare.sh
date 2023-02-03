#!/usr/bin/env bash

set -e

mkdir -p _out
./sektoren-geojson.py > sektoren.json
./sektoren-airspacepy > sektoren-airspace.txt
cp sektoren.json sektoren-airspace.txt _out

./login.sh
