#!/usr/bin/env bash

set -e


# For testing
limit=20

echo "flights.json: fetching"
wget \
    --no-verbose \
	--load-cookies _tmp/cookies.txt \
    "https://de.dhv-xc.de/api/fli/flights?y=2022&fkto%5B%5D=9306&fkto%5B%5D=11362&clubde%5B%5D=130&navpars=%7B%22start%22%3A0%2C%22limit%22%3A$limit%7D" \
	-O _tmp/flights.json
