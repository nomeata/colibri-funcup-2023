import constants
from geographiclib.geodesic import Geodesic

window_size = 5

def roundcoord(c):
    return (round(c['lat'], 6), round(c['lon'],6))

def landepunkt(ps):

    # first time in the last track points where speed is less than 5km/s
    for i in range(max(0,len(ps)-420), len(ps)-window_size):
        # average over n samples
        window = ps[i:i+window_size]
        ds = sum([
          Geodesic.WGS84.Inverse(window[i]['lat'], window[i]['lon'],
            window[i+1]['lat'], window[i+1]['lon'])['s12'] for i in range(len(window)-1) ])
        dt = window[-1]['time'] - window[0]['time']
        v = ds/dt
        if abs(v) < 1:
            return roundcoord(ps[i])

    return roundcoord(ps[-1])

    # for i in range(len(ps)-1, 1, -1):
    #     dt = (ps[i].time - ps[i-1]['time']).seconds
    #     dh = ps[i].elevation - ps[i-1].elevation
    #     if dt > 0 and abs(dh/dt) > constants.flightstop:
    #         return (ps[i]['lat'], ps[i]['lon'])

def landepunktabstand(punkt):
    (lat, lon) = punkt
    g = Geodesic.WGS84.Inverse(constants.landepunkt[0], constants.landepunkt[1], lat, lon)
    return round(g['s12'])






