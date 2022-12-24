#!/usr/bin/env bash

set -e

if [ ! -e schauinsland2022/flights.json ]; then
  echo "flights.json: fetching"
  wget 'https://de.dhv-xc.de/api/fli/flights?y=2022&l-y=2022&fkto%5B%5D=9306&l-fkto%5B%5D=Schauinsland%20(DE)&navpars=%7B%22start%22%3A0%2C%22limit%22%3A2000%2C%22sort%22%3A%5B%7B%22field%22%3A%22FlightDuration%22%2C%22dir%22%3A-1%7D%2C%7B%22field%22%3A%22FlightDate%22%2C%22dir%22%3A-1%7D%5D%7D' -O flights.json
fi

for id in $(jq -r '.data[]["IDFlight"]' < schauinsland2022/flights.json); do

if [ ! -e "schauinsland2022/$id.igc.gz" ]; then
  echo "$id: fetching"
  wget \
	--header 'Accept: application/x-igc' \
    --header 'Cookie: xclogin=71687891d25ab74168ddbe45ac2a1ab17fe8e2fa20cb1065489373bc547fb00e; xcsid=d40963b9be6c432cb79d01534e3d4dec' "https://de.dhv-xc.de/flight/$id/igc" \
	-O "schauinsland2022/$id.igc"
	gzip -9 "schauinsland2022/$id.igc"
fi

if [ ! -e "schauinsland2022/$id.stats.json" ]; then
  echo "$id: stats"
  ./flightstats.py -i "schauinsland2022/$id.igc.gz" > "schauinsland2022/$id.stats.json.tmp"
  mv "schauinsland2022/$id.stats.json.tmp" "schauinsland2022/$id.stats.json"
fi

done
