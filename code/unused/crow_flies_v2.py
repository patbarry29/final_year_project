import haversine as hs
from Altitude import *

def getStraightLine(start, end, step=100):
    if start == end:
        return {}
    
    dist = measureDistance(start, end)
    step_dist = calcStepDistance(dist, step)
    inc_lat, inc_lon = extraCalcs(start, end, step_dist)
    alt_dict = getAltitudes(start, end, inc_lat, inc_lon)
    return alt_dict
    

def measureDistance(start, end):
    distance = hs.haversine(start, end)
    return distance


def calcStepDistance(dist, step):
    # define how many kilometres to travel before measuring
    step = step/1000
    # we will measure the altitude distance/step times
    return dist / step


def extraCalcs(start, end, step_dist):
    # we will then subtract start latitude from end latitude
    # and repeat for longitude to get distance
    lat_dist = start[0] - end[0]
    lon_dist = start[1] - end[1]

    # then divide by number of steps to calculate the number to be
    # added to each
    inc_lat = lat_dist / step_dist
    inc_lon = lon_dist / step_dist

    return inc_lat, inc_lon


def getAltitudes(start, end, inc_lat, inc_lon):
    lat, lon = start[0], start[1]

    # now start a loop to find altitude at each step from start to end
    alt_dict = {}
    if lat < end[0]:
        while lat < end[0]:
            alt = Altitude((lat, lon))
            alt_dict[lat, lon] = alt.getAltitude()
            lat -= inc_lat
            lon -= inc_lon
    else:
        while lat > end[0]:
            alt = Altitude((lat, lon))
            alt_dict[lat, lon] = alt.getAltitude()
            lat -= inc_lat
            lon -= inc_lon

    alt = Altitude(end)
    alt_dict[lat, lon] = alt.getAltitude()

    return alt_dict


if __name__ == "__main__":
    start = (53.37731900994556, -6.234298920712984)
    end = 51.89585756404622, -8.458530434991815
    line = getStraightLine(start, end)