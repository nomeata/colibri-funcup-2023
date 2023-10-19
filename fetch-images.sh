#!/usr/bin/env bash

set -e

mkdir -p images
cd images

for id in $(jq -r '.data[]|select(.["HasPhotos"]=="1")|.["IDFlight"]' < ../_tmp/flights.json | sort -n ); do

  if [ ! -e "$id.json" ]; then
    echo "$id: fetching"
    wget \
      --no-verbose \
      --header 'Accept: application/json' \
      --load-cookies ../_tmp/cookies.txt \
      "https://de.dhv-xc.de/api/fli/photos?fkflight=$id" \
      -O "$id.json"
  fi

  jq -r '.data[]|"https://de.dhv-xc.de/photos/"+.["Path"]+"/"+.["FilenameHd"]' < "$id.json" | while read -r url ; do
    wget \
      --no-verbose \
      --load-cookies ../_tmp/cookies.txt \
      -r \
      "$url"

   done

done

