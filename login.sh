#!/usr/bin/env bash

set -e

echo "Logging in"

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

mkdir -p _tmp

rm -f _tmp/cookies.txt
wget \
  --no-verbose \
  --save-cookies _tmp/cookies.txt \
  --keep-session-cookies \
  https://de.dhv-xc.de/api/xc/login/status\
  -O _tmp/status.json

token=$(jq -r .meta.token < _tmp/status.json)
echo "Token: $token"
rm -f _tmp/status.json

wget \
  --no-verbose \
  --save-cookies _tmp/cookies.txt \
  --load-cookies _tmp/cookies.txt \
  --keep-session-cookies \
  --post-data "uid=$DHV_USERNAME&pwd=$DHV_PASSWORD&dhvfetch=0&stay=0" \
  --header "X-Csrf-Token: $token" \
  -O /dev/null \
  https://de.dhv-xc.de/api/xc/login/login
echo
