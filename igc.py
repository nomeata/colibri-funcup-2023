import re

r = re.compile('^B' + '(\d\d)(\d\d)(\d\d)'
        + '(\d\d)(\d\d)(\d\d\d)([NS])'
        + '(\d\d\d)(\d\d)(\d\d\d)([EW])'
        + '([AV])' + '([-\d]\d\d\d\d)' + '([-\d]\d\d\d\d)'
        + '([0-9a-zA-Z\-]*).*$')
def parse(f):
    track = []
    for line in f:
        match = r.match(line.decode('utf8',errors='ignore'))
        if match is not None:
            (hours, minutes, seconds,
             lat_deg, lat_min, lat_min_dec, lat_sign,
             lon_deg, lon_min, lon_min_dec, lon_sign,
             validity, press_alt, gnss_alt,
             extras) = match.groups()

            seconds = 3600*int(hours) + 60*int(minutes) + int(seconds)

            lat = float(lat_deg) + float(lat_min) / 60.0 + float(lat_min_dec) / 1000.0 / 60.0
            if lat_sign == 'S': lat = -lat

            lon = float(lon_deg) + float(lon_min) / 60.0 + float(lon_min_dec) / 1000.0 / 60.0
            if lon_sign == 'W': lon = -lon

            track.append({ 'time': seconds, 'lat': lat, 'lon': lon})
    return track

