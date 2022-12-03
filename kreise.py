#!/usr/bin/env python3

import math

def turns(gpx):
    left_turns = 0
    right_turns = 0
    left_angle = 0
    right_angle = 0


    for track in gpx.tracks:
        if track.name == "PRESALTTRK":
            continue

        for segment in track.segments:
            if len(segment.points) < 3:
                continue

            points = segment.points[:1]
            for p in segment.points[1:]:
                if (points[-1].latitude - p.latitude)**2 + (points[-1].longitude - p.longitude)**2 > 1e-8:
                    points.append(p)

            dir = 0
            max_dir = 0
            min_dir = 0

            for i in range (1, len(points)-1):
                x0 = points[i-1].latitude
                y0 = points[i-1].longitude
                x1 = points[i].latitude
                y1 = points[i].longitude
                x2 = points[i+1].latitude
                y2 = points[i+1].longitude

                alpha = math.atan2(y1-y0, x1-x0) - math.atan2(y2-y1, x2-x1)
                if   alpha > math.pi:   alpha -= 2 * math.pi
                elif alpha <= -math.pi: alpha += 2 * math.pi
                #print ((x0,y0), (x1,y1), (x2,y2), alpha * 180/math.pi)
                dir += alpha

                max_dir = max(dir, max_dir)
                min_dir = min(dir, min_dir)

                if dir - min_dir > 2*math.pi:
                    left_turns += 1
                    dir     -= 2*math.pi
                    max_dir = dir
                elif max_dir - dir > 2*math.pi:
                    right_turns += 1
                    dir     += 2*math.pi
                    min_dir = dir

                if alpha > 0: left_angle  += alpha
                else:         right_angle += -alpha

                #assert max_dir < 2*math.pi
                #assert min_dir > - 2*math.pi

                #print(dir/(2*math.pi))

    return {'left_turns': left_turns, 'right_turns': right_turns}
