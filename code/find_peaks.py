from Altitude import *
from Line import *
import math


def findPeaks(line, max_alt):
    '''
    Find obstacles on path of given line.
    Store the obstacle's highest point, as well as radius of the circle.
    '''
    peaks = {}
    too_high = {}
    for c in line:
        altitude = line[c]
        if altitude >= max_alt and list(line).index(c) != len(line)-1:
            too_high[c] = altitude
        elif len(too_high) > 0:
            peak_coords = max(too_high, key=too_high.get)
            # all_coords = list(too_high.keys())
            # d1 = math.dist(peak_coords, all_coords[-1])
            # d2 = math.dist(peak_coords, all_coords[0])
            # peaks[peak_coords] = max([d1, d2])
            peaks[peak_coords] = 0.0005
            too_high = {}

    return peaks



if __name__ == "__main__":
    start = (53.37731900994556, -6.234298920712984)
    end = (51.89585756404622, -8.458530434991815)
    max_alt = 487
    line = Line(start, end).getLine()
    peaks = findPeaks(line, max_alt)

    print(peaks)