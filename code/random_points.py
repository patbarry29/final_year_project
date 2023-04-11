from Altitude import *
from random import randint
from haversine import haversine
from Line import *

def getTwoPoints(range):
    pt1 = generatePoint()
    pt2 = generatePoint()
    pt1, pt2 = checkPoints(pt1,pt2,range)
    
    return pt1, pt2

def checkPoints(pt1,pt2,range):
    dist = haversine(pt1,pt2)
    start_alt = Altitude(pt1).getAltitude()
    end_alt = Altitude(pt2).getAltitude()
    while dist > range or end_alt > start_alt+120 or Line(pt1, pt2).getMaxAlt() <= start_alt+120:
        pt1, pt2 = getTwoPoints(range)
        dist = haversine(pt1, pt2)
        start_alt = Altitude(pt1).getAltitude()
        end_alt = Altitude(pt2).getAltitude()
    return pt1,pt2

def generatePoint():
    coords1 = randPoint()
    try:
        while Altitude(coords1).getAltitude() <= 0: # find point on land
            coords1 = randPoint()
    except TypeError:
        coords1 = generatePoint()
        
    return coords1

def randPoint():
    min = (51.21,-10.689) # bottom left corner of Ireland
    max = (55.484,-5.281) # top right corner of Ireland

    precision = 1000000 # how random will the coord be

    lat = randint(int(min[0]*precision), int(max[0]*precision))
    lon = randint(int(min[1]*precision), int(max[1]*precision))
    lat /= precision
    lon /= precision

    return (lat, lon)


if __name__ == "__main__":
    '''
        Test best value for range_in_kms
        Setting to 20 results in recursion depth exceeded 33% of the time
        Setting to 30 leads to 3% fail rate
    '''
    sum = 0
    range_in_kms = 30
    for i in range(200):
        try:
            start, end = getTwoPoints(range_in_kms)
        except:
            sum+=1
    print(sum)