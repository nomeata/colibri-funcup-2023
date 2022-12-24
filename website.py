#!/usr/bin/env python3

# Generates the website

import json
import os
import jinja2
import math
import shutil
import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

def pretty_duration(s):
    s = int(s)
    if s < 60:
        return f"{s}s"
    elif s < 60*60:
        return f"{math.floor(s/60)} min"
    else:
        return f"{math.floor(s/(60*60))} h {math.floor((s % (60*60))/60)} min"

def pretty_landepunktabstand(d):
    if d < 200:
        return f"{d} m"
    else:
        return ""

# prepare output directory

try:
    os.mkdir('schauinsland2022/out')
except FileExistsError:
    pass
shutil.copytree('templates/static', 'schauinsland2022/out/static', dirs_exist_ok=True)

flight_data = json.load(open('schauinsland2022/flights.json'))

flights = {}

# Group flights by pilot, read stats
for flight in flight_data['data']:
    id = flight['IDFlight']
    pid = flight['FKPilot']

    flight['stats'] = json.load(open(f'schauinsland2022/{id}.stats.json'))

    if pid not in flights:
        flights[pid] = []
    flights[pid].append(flight)

# Sort by date
for pid, pflights in flights.items():
    pflights.sort(key = lambda f: f['FlightStartTime'])

# Create per pilot website, and gather stats
pilots = []
pilottemplate = env.get_template("pilot.html")
for pid, pflights in flights.items():
    name = pflights[0]['FirstName'] + ' ' + pflights[0]['LastName']
    covered = set()

    # stats
    stats = {
        'schauiflights': 0,
        'lindenflights': 0,
        'flighttime': 0,
        'hikes': 0,
        'fotos': 0,
        'sektoren': 0,
        'landepunkt1': 0,
        'landepunkt2': 0,
        'landepunkt3': 0,
        'drehrichtung': "",
        'drehueberschuss': 0,
        'left_turns': 0,
        'right_turns': 0,
    }


    data = {}
    data['flights'] = []
    for n, f in enumerate(pflights):
        # Neue sektoren
        new = set(f['stats']['sektoren']).difference(covered)
        covered.update(new)

        # update stats
        stats['flighttime'] += int(f['FlightDuration'])
        stats['left_turns'] += f['stats']['left_turns']
        stats['right_turns'] += f['stats']['right_turns']
        if f['stats']['landepunktabstand'] < 10:
            stats['landepunkt1'] += 1
        elif f['stats']['landepunktabstand'] < 25:
            stats['landepunkt2'] += 1
        elif f['stats']['landepunktabstand'] < 100:
            stats['landepunkt3'] += 1

        data['flights'].append({
          'n': n+1,
          'id': f['IDFlight'],
          'datum': datetime.date.fromisoformat(f['FlightDate']).strftime("%d.%m."),
          'flugzeit': pretty_duration(f['FlightDuration']),
          'linkskreise': f['stats']['left_turns'],
          'rechtskreise': f['stats']['right_turns'],
          'landepunktabstand': pretty_landepunktabstand(f['stats']['landepunktabstand']),
          'neue_sektoren': " ".join(sorted(list(new))),
          'neue_sektoren_anzahl': len(new),
          'url': f"https://de.dhv-xc.de/flight/{id}",
        })

    # Finalize stats
    stats['sektoren'] = len(covered)
    if stats['left_turns'] > stats['right_turns']:
        stats['drehrichtung'] = "(nach links)"
        stats['drehueberschuss'] = stats['left_turns'] - stats['right_turns']
    elif stats['left_turns'] < stats['right_turns']:
        stats['drehrichtung'] = "(nach rechts)"
        stats['drehueberschuss'] = stats['right_turns'] - stats['left_turns']
    stats['prettyflighttime'] = pretty_duration(stats['flighttime'])


    # Calculate points
    points = {
        'schauiflights': stats['schauiflights'] * 5,
        'lindenflights': stats['lindenflights'] * 10,
        'flighttime': stats['flighttime'] // 60,
        'hikes': stats['hikes'] * 20,
        'fotos': stats['fotos'] * 50,
        'sektoren': stats['sektoren'] * 100,
        'landepunkt1': stats['landepunkt1'] * 100,
        'landepunkt2': stats['landepunkt2'] * 100,
        'landepunkt3': stats['landepunkt3'] * 100,
        'drehueberschuss': stats['drehueberschuss'] * -20,
    }
    points['total'] = sum(points.values())

    pilots.append({
        'pid': pid,
        'name': name,
        'stats': stats,
        'points': points,
    })

    # Write per-pilot website
    data['pid'] = pid
    data['name'] = name
    data['stats'] = stats
    data['points'] = points
    pilottemplate\
      .stream(data) \
      .dump(open(f'schauinsland2022/out/pilot{pid}.html', 'w'))


# Write main website
pilots.sort(key = lambda p: - p['points']['total'])
for i, p in enumerate(pilots):
    p['rank'] = i + 1

data = {}
data['pilots'] = pilots
env.get_template("index.html") \
  .stream(data) \
  .dump(open(f'schauinsland2022/out/index.html', 'w'))
