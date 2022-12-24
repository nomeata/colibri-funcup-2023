#!/usr/bin/env bash

set -e

./fetch.sh
./by_pilot.py
./pilot-maps.sh
./website.py
