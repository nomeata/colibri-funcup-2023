#!/usr/bin/env bash

set -e

pwd
ls

mkdir schauinsland2022
mkdir schauinsland2022/out
./sektoren-geojson.py > sektoren.json
cp sektoren.json schauinsland2022/out
./fetch.sh
./by_pilot.py
./pilot-maps.sh
./website.py
