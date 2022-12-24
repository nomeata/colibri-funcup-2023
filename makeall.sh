#!/usr/bin/env bash

set -e

pwd
ls

mkdir schauinsland2022
./fetch.sh
./by_pilot.py
./pilot-maps.sh
./website.py
