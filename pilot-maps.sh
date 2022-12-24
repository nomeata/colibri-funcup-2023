#!/usr/bin/env bash

set -e

if [ -z "$*" ]
then
  files=( schauinsland2022/pilots/*.json )
else
  files=( "$@" )
fi

for file in "${files[@]}"
do
  id=$(basename $file .json)
  echo schauinsland2022/out/map$id.html
  ./sektoren-map.py schauinsland2022/out/map$id.html $(jq  -r '.[]["IDFlight"]' < schauinsland2022/pilots/407.json | perl -ne 'chomp; print "schauinsland2022/$_.igc.gz\n"')
done
