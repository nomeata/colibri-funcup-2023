#!/usr/bin/env bash

set -e


./prepare.sh
./fetch-flights.sh
./fetch-igc.sh
./flightstats.sh

./sektoren-map.py
./website.py
