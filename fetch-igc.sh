#!/usr/bin/env bash

set -e

mkdir -p _flights

for id in $(jq -r '.data[]["IDFlight"]' < _tmp/flights.json | sort -n ); do

  if [ ! -e "_flights/$id.igc.gz" ]; then
    echo "$id: fetching"
    wget \
      --no-verbose \
      --header 'Accept: application/x-igc' \
      --load-cookies _tmp/cookies.txt \
      "https://de.dhv-xc.de/flight/$id/igc" \
      -O "_flights/$id.igc"
    gzip -9 "_flights/$id.igc"
  fi

done

for id in $(jq -r '.data[] | select(.CountComments != "0") | .IDFlight' < _tmp/flights.json | sort -n ); do
  if [ ! -e "_flights/$id.comments.json" ]; then
    echo "$id: comments"
    wget \
        --no-verbose \
	--header 'Accept: application/x-igc' \
	--load-cookies _tmp/cookies.txt \
	"https://de.dhv-xc.de/api/fli/comments?fkflight=$id" \
	-O "_flights/$id.comments.json"
  fi
done
