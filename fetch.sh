#!/usr/bin/env bash

set -e

if [ ! -e schauinsland2022/flights.json ]; then
  echo "flights.json: fetching"
  wget 'https://de.dhv-xc.de/api/fli/flights?y=2022&l-y=2022&fkto%5B%5D=9306&l-fkto%5B%5D=Schauinsland%20(DE)&navpars=%7B%22start%22%3A0%2C%22limit%22%3A2000%2C%22sort%22%3A%5B%7B%22field%22%3A%22FlightDuration%22%2C%22dir%22%3A-1%7D%2C%7B%22field%22%3A%22FlightDate%22%2C%22dir%22%3A-1%7D%5D%7D' -O flights.json
fi

for id in $(jq -r '.data[]["IDFlight"]' < schauinsland2022/flights.json); do

if [ ! -e "schauinsland2022/$id.igc.gz" ]; then
  echo "$id: fetching"
  wget --header 'Cookie: xclogin=3ac0e635c772f3580d2a36581e66dcf33d3c4f7ff1ce365076736491d707e984; xcsid=f20b8ec9857850fb79704a60868fa4cb' "https://de.dhv-xc.de/flight/$id/igc" -O - | gzip -9 -> "schauinsland2022/$id.igc.gz"
fi

if [ ! -e "schauinsland2022/$id.stats.json" ]; then
  echo "$id: stats"
  ./flightstats.py -i "schauinsland2022/$id.igc.gz" > "schauinsland2022/$id.stats.json"
fi

done
