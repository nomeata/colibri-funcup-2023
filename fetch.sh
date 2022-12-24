#!/usr/bin/env bash

set -e

echo "Loggin in"

if [ -z "$DHV_PASSWORD" ]
then
   echo "Missing environment variable \$DHV_PASSWORD"
   exit 1
fi

if [ -z "$DHV_USERNAME" ]
then
   echo "Missing environment variable \$DHV_USERNAME"
   exit 1
fi


rm -f cookies.txt
rm -f status.json
wget \
  --save-cookies cookies.txt \
  --keep-session-cookies \
  https://de.dhv-xc.de/api/xc/login/status\
  -O status.json

token=$(jq -r .meta.token < status.json)
echo "Token: $token"
rm -f status.json

wget \
  --save-cookies cookies.txt \
  --load-cookies cookies.txt \
  --keep-session-cookies \
  --post-data "uid=$DHV_USERNAME&pwd=$DHV_PASSWORD&dhvfetch=0&stay=0" \
  --header "X-Csrf-Token: $token" \
  -O - \
  https://de.dhv-xc.de/api/xc/login/login


limit=2000
# for testing:
limit=10


if [ ! -e schauinsland2022/flights.json ]; then
  echo "flights.json: fetching"
  wget \
	--load-cookies cookies.txt \
    "https://de.dhv-xc.de/api/fli/flights?y=2022&l-y=2022&fkto%5B%5D=9306&l-fkto%5B%5D=Schauinsland%20(DE)&navpars=%7B%22start%22%3A0%2C%22limit%22%3A$limit%2C%22sort%22%3A%5B%7B%22field%22%3A%22FlightDuration%22%2C%22dir%22%3A-1%7D%2C%7B%22field%22%3A%22FlightDate%22%2C%22dir%22%3A-1%7D%5D%7D" \
	-O schauinsland2022/flights.json
fi

for id in $(jq -r '.data[]["IDFlight"]' < schauinsland2022/flights.json); do

if [ ! -e "schauinsland2022/$id.igc.gz" ]; then
  echo "$id: fetching"
  wget \
	--header 'Accept: application/x-igc' \
	--load-cookies cookies.txt \
	"https://de.dhv-xc.de/flight/$id/igc" \
	-O "schauinsland2022/$id.igc"
  gzip -9 "schauinsland2022/$id.igc"
fi

if [ ! -e "schauinsland2022/$id.stats.json" ]; then
  echo "$id: stats"
  ./flightstats.py -i "schauinsland2022/$id.igc.gz" > "schauinsland2022/$id.stats.json.tmp"
  mv "schauinsland2022/$id.stats.json.tmp" "schauinsland2022/$id.stats.json"
fi

done

rm -f cookies.txt
