#!/usr/bin/env bash

set -e

for file in schauinsland2022/pilots/*.json
do
  id=$(basename $file .json)
  echo $id
  ./sektoren-map.py schauinsland2022/out/map$id.html $(jq  -r '.[]["IDFlight"]' < schauinsland2022/pilots/407.json | perl -ne 'chomp; print "schauinsland2022/$_.igc.gz\n"')
done
