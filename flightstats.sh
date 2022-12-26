#!/usr/bin/env bash

set -e

mkdir -p _stats

for id in $(jq -r '.data[]["IDFlight"]' < _tmp/flights.json | sort -n ); do
  if [ ! -e "_stats/$id.stats.json" ]; then
    echo "$id: stats"
    ./flightstats.py -i "_flights/$id.igc.gz" > "_stats/$id.stats.json.tmp"
    mv "_stats/$id.stats.json.tmp" "_stats/$id.stats.json"
  fi
done
