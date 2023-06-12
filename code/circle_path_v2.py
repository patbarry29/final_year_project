from Circle import Circle
from Line import *
import haversine as hs
import math

'''
Implementation of circles with waypoints
'''

def makeSquares(start, circles):
    '''
    Makes a square around each peak. Consists of 4 points, the entry point,
    one point at either side of the circle, and the exit point.
    '''
    squares = {}
    for p, circle in circles.items():
        closest_point = (0,0)
        key_points = [0]*4

        for p in circle:
            dist1 = haversine(closest_point, start)
            dist2 = haversine(p, start)
            
            if dist2 < dist1:
                closest_point = p
        
        key_points[0] = closest_point

        circle = list(circle)
        i = circle.index(closest_point)
        circle = circle[i:] + circle[:i]
        key_points[1] = circle[int(len(circle)*.25)]
        key_points[2] = circle[int(len(circle)*.75)]
        key_points[3] = circle[int(len(circle)*.5)]

        squares[p] = key_points
    
    return squares


def checkAltitude(peaks, squares, max_alt):
    '''
    Checks if there is a path that can be followed around the obstacle.
    Checks both the top waypoint and the bottom waypoint for a path.
    '''
    too_high = False

    for index in range(len(squares)):
        square = squares[list(squares)[index]]
        
        top_point = square[1]
        path = Line(square[0], top_point)
        path.addLine(Line(top_point, square[3]))
        try:
            max_on_top = path.getMaxAlt()

            if max_on_top > max_alt:
                bottom_point = square[2]
                path = Line(square[0], bottom_point)
                path.addLine(Line(bottom_point, square[3]))
                max_on_bottom = path.getMaxAlt()
                if max_on_bottom > max_alt:
                    peaks_key = list(peaks)[index]
                    peaks[peaks_key] = peaks[peaks_key]*1.05
                    too_high = True
            
        except:
            sys.exit("No solution found - Circle w/ Waypts")
            
    return too_high

def selectPoints(line, squares):
    '''
    Checks each square, containing 4 points, and removes one point.
    Then stores the remaining 3 to be used for the drone's path.
    '''
    start = list(line)[0]
    end = list(line)[-1]
    waypts = [start]
    for peak, square in squares.items():
        top_point = square[1]
        top_path = Line(square[0], top_point)
        top_path.addLine(Line(top_point, square[3]))
        try:
            max_on_top = top_path.getMaxAlt()

            bottom_point = square[2]
            bottom_path = Line(square[0], bottom_point)
            bottom_path.addLine(Line(bottom_point, square[3]))
            max_on_bottom = bottom_path.getMaxAlt()

            if max_on_top < max_on_bottom:
                squares[peak][2] = 0
            else:
                squares[peak][1] = 0

            for point in square:
                if point != 0:
                    waypts.append(point)
        
        except:
            sys.exit("No solution found - Circle w/ Waypts")

    waypts.append(end)
    return waypts


def removeContainedPoints(pts_list):
    '''
    Due to circle radius getting bigger, it can often happen that one circle
    will reach around over another circle.
    This function checks each set of 3 points to see if one is contained within the 
    other. If yes, then remove the 3 points.
    '''
    start = pts_list[0]
    end = pts_list[-1]
    i = 1
    num_of_edges = 3
    while i < len(pts_list):
        square1 = pts_list[i:i+num_of_edges]
        d1_start = math.dist(start, square1[0])
        d1_end = math.dist(end, square1[-1])
        j = 1
        while j < len(pts_list):
            square2 = pts_list[j:j+num_of_edges]
            d2_start = math.dist(start,square2[0])
            d2_end = math.dist(end,square2[-1])
            
            if d1_start>d2_start and i<j:
                # remove this set of points from the list
                pts_list = pts_list[:i] + pts_list[i+num_of_edges:]
                i = i-num_of_edges
                break

            elif d1_end<d2_end and i<j:
                pts_list = pts_list[:j] + pts_list[j+num_of_edges:]

            j += num_of_edges
        i += num_of_edges
    
    return pts_list


def circleAlgV2(peaks, line, inc, max_alt):
    '''
        Run Circles w/ Waypoints algorithm
    '''
    start = list(line)[0]

    circle = Circle(list(peaks)[0])
    circles = circle.drawCircles(peaks, inc)

    squares = makeSquares(start, circles)
    while checkAltitude(peaks, squares, max_alt):
        circles = circle.drawCircles(peaks, inc)
        squares = makeSquares(start, circles)

    waypts = selectPoints(line, squares)
    waypts = removeContainedPoints(waypts)

    square_path = Line(0, 0)
    for i in range(len(waypts)-1):
        line = Line(waypts[i], waypts[i+1])
        square_path.addLine(line)

    return square_path