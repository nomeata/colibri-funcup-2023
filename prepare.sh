#!/usr/bin/env bash

set -e

mkdir -p _out
./sektoren-geojson.py > sektoren.json
cp sektoren.json _out

./login.sh
