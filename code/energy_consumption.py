import math
from haversine import haversine
from Altitude import *

'''
Functions to use in evaluating energy usage
'''

def getEnergy(pt1, pt2):
    '''
    Return energy between 2 points in 3 different metrics
        Mega Joules
        Kilowatt-hours
        Milliamp-hours
    '''
    dist_in_m = haversine(pt1, pt2)

    energy_per_m = 108.1 # Joules per metre
    payload = 1.6 # kgs

    energy_joules = dist_in_m*energy_per_m
    energy_MJ = energy_joules/(1000**2) # mega Joules

    energy_kWh = energy_MJ*(5/8)

    voltage = 22.8 # average voltage of battery

    mAh_used = energy_kWh/voltage * 100000000

    # print("Mega Joules used:", energy_MJ)
    # print("Kilowatt-hours used:", energy_kWh)
    # print("Milli amp-hours used:", mAh_used)

    return (energy_MJ, energy_kWh, mAh_used)

def angle3pts(pt1, pt2, pt3):
    '''
        Returns angle between 3 points from 0-180
    '''
    ang_rads = math.atan2(pt3[1]-pt2[1], pt3[0]-pt2[0]) - math.atan2(pt1[1]-pt2[1], pt1[0]-pt2[0])
    ang = math.degrees(ang_rads)
    if ang < 0:
        ang += 360
    ang = max(180-ang, ang-180)
    return ang
