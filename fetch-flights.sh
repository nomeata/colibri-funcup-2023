#!/usr/bin/env bash

set -e

limit=2000
year=2023

echo "flights.json: fetching"
wget \
    --no-verbose \
	--load-cookies _tmp/cookies.txt \
    "https://de.dhv-xc.de/api/fli/flights?d0=1.1.$year&d1=15.9.$year&fkto%5B%5D=9306&fkto%5B%5D=11362&clubde%5B%5D=130&navpars=%7B%22start%22%3A0%2C%22limit%22%3A$limit%7D" \
	-O _tmp/flights.json.tmp
echo -n "Flights before opt-out: "
jq '.data | length' < _tmp/flights.json.tmp
# pilot opt-out
jq '.data |= map(select(.FKPilot != "14677" and .FKPilot != "1284" ))' < _tmp/flights.json.tmp > _tmp/flights.json
echo -n "Flights after opt-out: "
jq '.data | length' < _tmp/flights.json
