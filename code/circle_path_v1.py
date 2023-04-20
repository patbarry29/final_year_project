from Line import *
import math
from Circle import *
from random_points import *

'''
Implementation using circles
'''

def separateCircles(line, circles, num_steps):
    '''
        Takes in circles, a list of the circles drawn around the obstacles.
        Splits these circles in half and chooses the one with the smaller 
        maximum altitude.
        Replaces the full circle in circles with a semi-circle.
    '''
    for c in circles:
        circle = circles[c]
        closest_point = (0,0)

        # calculate the point on the circle closest to the straight line
        for p in circle:
            distance = haversine(p, list(line)[0])
            min_dist = haversine(closest_point, list(line)[0])

            if distance < min_dist:
                closest_point = p

        # split the circle in half, starting from closest point
        circle_l = list(circle)
        i = circle_l.index(closest_point)
        circle_l = circle_l[i:] + circle_l[:i+1]
        semi_circle1 = circle_l[:num_steps+1]
        semi_circle2 = [circle_l[0]] + circle_l[:num_steps:-1]

        semi_circle1_d = {}
        for p in semi_circle1:
            semi_circle1_d[p] = circle[p]
        
        semi_circle2_d = {}
        for p in semi_circle2:
            semi_circle2_d[p] = circle[p]

        try:
            max1 = max(semi_circle1_d.values())
            max2 = max(semi_circle2_d.values())
            if max1 < max2:
                circles[c] = semi_circle1_d
            else:
                circles[c] = semi_circle2_d

        except:
            sys.exit("No solution found - Circles")
    

def checkCircles(peaks, circles, max_alt):
    '''
        Function to check altitude of each semi-circle in circles
        Checks if the max altitude of the semi-circle is greater than
        the max altitude of the drone.
        If max altitude of drone violated, increase circle radius
    '''
    too_high = False
    for c in range(len(circles)):
        circle = circles[list(circles)[c]]
        try:
            max_on_circle = max(list(circle.values()))
            if max_on_circle > max_alt:
                peaks_key = list(peaks)[c]
                peaks[peaks_key] = peaks[peaks_key]*1.05
                too_high = True

        except:
            sys.exit("No solution found - Circles")
    return too_high


def circleAlgV1(peaks, line, inc, max_alt):
    '''
    Run circle algorithm.
    '''
    circle = Circle(list(peaks)[0])
    circles = circle.drawCircles(peaks, inc)
    separateCircles(line, circles, int(180/inc))
    
    # while there is a circle radius too small, increase it
    while checkCircles(peaks, circles, max_alt):
        circles = circle.drawCircles(peaks, inc)
        separateCircles(line, circles, int(180/inc))


    start = list(line)[0]
    end = list(line)[-1]
    points = [start]
    for p,circle in circles.items():
        for pt in circle:
            points.append(pt)
    points.append(end)

    circle_path = Line(0,0)
    for point in range(len(points)-1):
        line = Line(points[point], points[point+1])
        circle_path.addLine(line)

    return circle_path
