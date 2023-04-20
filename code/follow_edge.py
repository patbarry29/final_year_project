from Obstacles import Obstacles
from random_points import *
from Line import *
from find_peaks import *

def runFollowEdge(start, end, start_alt, straight_line, step_dist):
    '''
        Runs follow edge of obstacles algorithm.
        Similar to greedy but not always guaranteed to find solution if exists.
    '''
    max_alt = 120
    # i = 1
    path = followEdge(start, end, straight_line, start_alt+max_alt, step_dist)
    max_alt -= 60

    paths = {path: path.getMaxAlt()}
    try:
        # if path violates maximum altitude, try reducing the max_alt
        while path.getMaxAlt() > start_alt+120 and max_alt >= 0:
            path = followEdge(start, end, straight_line, start_alt+max_alt, step_dist)
            max_alt -= 60
            paths[path] = path.getMaxAlt()
    except:
        print("Algorithm interrupted")
    
    min_path = min(paths.items(), key=lambda x: x[1])
    path = min_path[0]
    min_path = min(paths.items(), key=lambda x: x[1])
    path = min_path[0]
    return path

def followEdge(start, end, line, max_alt, step_dist):
    '''
        For each obstacle, finds a path around it that sticks to the edge.
    '''
    obstacles = Obstacles(line, max_alt).getObstacles()
    x_slope,y_slope = getSlope(start, end, step_dist)
    checkpoints = [start]
    for obstacle in obstacles:
        # obs_num = obstacles.index(obstacle)
        # print("On obstacle", obs_num+1, end=' - ')

        obs_line = Line(obstacle[0], obstacle[-1], step_dist)

        left_path = [checkpoints[-1]]
        left_max_alt = 0
        for point in obs_line.getLine():
            point_max_alt = findEdge(point, left_path, max_alt, x_slope, y_slope, step_dist, left=True)
            left_max_alt = max(point_max_alt, left_max_alt)
        
        right_path = [checkpoints[-1]]
        right_max_alt = 0
        for point in obs_line.getLine():
            point_max_alt = findEdge(point, right_path, max_alt, x_slope, y_slope, step_dist, left=False)
            right_max_alt = max(point_max_alt, right_max_alt)

        left = True
        if left_max_alt < right_max_alt:
            # print("go left with a maximum of {}m".format(left_max_alt))
            checkpoints += left_path[1:]
        else:
            # print("go right with a maximum of {}m".format(right_max_alt))
            checkpoints += right_path[1:]
            left = False

        new_end = getNewPoint(end, obstacle[-1], x_slope, y_slope)
        test_line = Line(checkpoints[-1], new_end, step_dist)
        d1 = haversine(new_end, end)
        while test_line.getMaxAlt() > max_alt:
            findEdge(new_end, checkpoints, max_alt, x_slope, y_slope, step_dist, left)
            new_end = getNewPoint(end, new_end, x_slope, y_slope)
            d2 = haversine(new_end, end)
            if d2 > d1:
                break
            d1 = d2
            test_line = Line(checkpoints[-1], new_end, step_dist)
        checkpoints.append(new_end)
    
    checkpoints += [end]

    return createPath(checkpoints, step_dist)

def getSlope(start, end, step_dist):
    # get distance from start to end
    dist = haversine(start,end)
    dist /= (step_dist/1000)
    # find x values that are 'step_dist' metres apart
    x_slope = (start[0]-end[0]) / dist
    # find y values that are 'step_dist' metres apart
    y_slope = (start[1]-end[1]) / dist
    return x_slope, y_slope

def findEdge(point, pts_list, max_alt, x_slope, y_slope, step_dist, left):
    '''
        Finds a waypoint for the drone to fly to.
    '''
    pts_dict = {}
    test_line = Line(point, pts_list[-1], step_dist)
    pts_dict[point] = test_line.getMaxAlt()
    count = 0
    max_dist = 500 # how far away from the obstacle the drone can travel in metres
    while test_line.getMaxAlt() > max_alt:
        if count < (max_dist/step_dist):
            point = getPerpPoint(point, max_alt, x_slope, y_slope, left)
            test_line = Line(point, pts_list[-1], step_dist)
            pts_dict[point] = test_line.getMaxAlt()
            count += 1
        else:
            min_point = min(pts_dict.items(), key=lambda x: x[1])
            point = min_point[0]
            test_line = Line(point, pts_list[-1], step_dist)
            break
    
    obs_max_alt = test_line.getMaxAlt()
    # if test_line.getMaxAlt() > max_alt:
    #     print(test_line.getMaxAlt(), max_alt, '\t', left)
    pts_list.append(point)

    return obs_max_alt


def getPerpPoint(point, max_alt, x_slope, y_slope, left):
    '''
        Returns a point perpendicular to x_slope and y_slope.
        left indicates whether to find point to the "left" or "right" of 
        the line.
        Point returned must be below max_alt
    '''
    lat = point[0]
    lon = point[1]
    
    if left:
        y_slope = -1 * y_slope
    else:
        x_slope = -1 * x_slope
    
    lat += (y_slope)
    lon += (x_slope)
    while Altitude((lat, lon)).getAltitude() > max_alt:
        lat += (y_slope)
        lon += (x_slope)
    return (lat, lon)


def getNewPoint(point1, point2, x_slope, y_slope):
    '''
        Returns point which is closer to point2.
    '''
    if point1[1] > point2[1]:
        lat = point2[0] - x_slope
        lon = point2[1] - y_slope
        point2 = (lat, lon)
    else:
        lat = point2[0] + x_slope
        lon = point2[1] + y_slope
        point2 = (lat, lon)
    return point2


def createPath(pts_list, step_dist):
    '''
    Create a line from pts_list
    '''
    path = Line(0,0)
    for i in range(len(pts_list)-1):
        line = Line(pts_list[i],pts_list[i+1], step_dist)
        path.addLine(line)
        # print(path.getMaxAlt(), path.getLength())
    return path