#!/usr/bin/env bash

set -e

mkdir schauinsland2022
./fetch.sh
./by_pilot.py
./pilot-maps.sh
./website.py
