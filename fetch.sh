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
  --no-verbose \
  --save-cookies cookies.txt \
  --keep-session-cookies \
  https://de.dhv-xc.de/api/xc/login/status\
  -O status.json

token=$(jq -r .meta.token < status.json)
echo "Token: $token"
rm -f status.json

wget \
  --no-verbose \
  --save-cookies cookies.txt \
  --load-cookies cookies.txt \
  --keep-session-cookies \
  --post-data "uid=$DHV_USERNAME&pwd=$DHV_PASSWORD&dhvfetch=0&stay=0" \
  --header "X-Csrf-Token: $token" \
  -O /dev/null \
  https://de.dhv-xc.de/api/xc/login/login
echo

limit=2000
# for testing:
limit=100


if [ ! -e schauinsland2022/flights.json ]; then
  echo "flights.json: fetching"
  wget \
        --no-verbose \
	--load-cookies cookies.txt \
    "https://de.dhv-xc.de/api/fli/flights?y=2022&fkto%5B%5D=9306&fkto%5B%5D=11362&navpars=%7B%22start%22%3A0%2C%22limit%22%3A$limit%7D" \
	-O schauinsland2022/flights.json
fi

for id in $(jq -r '.data[]["IDFlight"]' < schauinsland2022/flights.json | sort -n ); do

if [ ! -e "schauinsland2022/$id.igc.gz" ]; then
  echo "$id: fetching"
  wget \
        --no-verbose \
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

for id in $(jq -r '.data[] | select(.CountComments != "0") | .IDFlight' < schauinsland2022/flights.json | sort -n ); do
  if [ ! -e "schauinsland2022/$id.comments.json" ]; then
    wget \
        --no-verbose \
	--header 'Accept: application/x-igc' \
	--load-cookies cookies.txt \
	"https://de.dhv-xc.de/api/fli/comments?fkflight=$id" \
	-O "schauinsland2022/$id.comments.json"
  fi
done

rm -f cookies.txt
