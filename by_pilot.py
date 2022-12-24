#!/usr/bin/env python3

# Splits flights.json by pilot, sorted by date

import json
import os

try:
    os.mkdir('schauinsland2022/pilots')
except FileExistsError:
    pass

flight_data = json.load(open('schauinsland2022/flights.json'))

flights = {}

for flight in flight_data['data']:
    id = flight['IDFlight']
    pid = flight['FKPilot']

    if pid not in flights:
        flights[pid] = []
    flights[pid].append(flight)

for pid, flights in flights.items():
    flights.sort(key = lambda f: f['FlightStartTime'])
    json.dump(flights, open(f'schauinsland2022/pilots/{pid}.json','w'), indent=True)
