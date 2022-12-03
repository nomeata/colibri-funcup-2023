#!/usr/bin/env python3

import json
import csv

flight_data = json.load(open('schauinsland2022/flights.json'))

writer = csv.DictWriter(open("schauinsland2022.csv","w"), fieldnames=["id", "pilot", "pilotid", "flugzeit", "linkskreise", "rechtskreise", "url", "landepunktabstand", "neue_sektoren", "neue_sektoren_anzahl"])
writer.writeheader()

covered = {}

for flight in flight_data['data']:
    id = flight['IDFlight']
    pid = flight['FKPilot']
    stats = json.load(open(f'schauinsland2022/{id}.stats.json'))

    if pid not in covered:
        covered[pid] = set()

    new = set(stats['sektoren']).difference(covered[pid])
    covered[pid].update(new)

    writer.writerow({
      'id': id,
      'pilot': flight['FirstName'] + ' ' + flight['LastName'],
      'pilotid': flight['FKPilot'],
      'flugzeit': flight['FlightDuration'],
      'linkskreise': stats['left_turns'],
      'rechtskreise': stats['right_turns'],
      'landepunktabstand': stats['landepunktabstand'],
      'neue_sektoren': " ".join(sorted(list(new))),
      'neue_sektoren_anzahl': len(new),
      'url': f"https://de.dhv-xc.de/flight/{id}",
    })

