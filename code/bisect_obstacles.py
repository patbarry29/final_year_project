from queue import PriorityQueue
from Line import *
from Obstacles import *
from random_points import getTwoPoints

'''
Bisect Obstacles algorithm
'''

def bisect(line, max_alt, safe_pts, waypts, target, main_line):
    '''
        Function to bisect obstacles and return a path if found.
    '''
    if target in waypts:
        return waypts
    
    start = line.getPoint(0)
    end = line.getPoint(-1)
    obstacles = Obstacles(line, max_alt).getObstacles()
    if len(obstacles) > 0:
        for obs in obstacles:
            halfway_pt = obs[1]

            safe_l = getPerpPoint(halfway_pt, line, max_alt, left=True)
            safe_r = getPerpPoint(halfway_pt, line, max_alt, left=False)

            dist_l = haversine(safe_l, halfway_pt)
            dist_r = haversine(safe_r, halfway_pt)

            # Put in priority queue for checking the next point
            safe_pts.put((dist_l, [start, safe_l, end]))
            safe_pts.put((dist_r, [start, safe_r, end]))
            
            # pop from top of the queue
            safe_pt = safe_pts.get()[1]
            line = Line(safe_pt[0], safe_pt[1])
            
            try:
                checkSide(line, max_alt, safe_pt, safe_pts, waypts, target, main_line)
            except:
                if len(waypts) > 1000:
                    sys.exit('No solution')
                return
    else:
        # if no obstacles, then add path from start to end
        waypts[end] = start

def checkSide(line, max_alt, pt_list, safe_pts, waypts, target, main_line):
    '''
        Check if safe point can be connected to the start safely.
        If yes, then connect to the end and check that for obstacles.
        If either the start line or end line encounter an obstacle, then bisect again.
    '''
    start = pt_list[0]
    safe_pt = pt_list[1]
    end = pt_list[2]
    if line.getMaxAlt() > max_alt:
        bisect(line, max_alt, safe_pts, waypts, target, main_line)
    else:
        waypts[safe_pt] = start
        line_end = Line(safe_pt, end)
        if line_end.getMaxAlt() > max_alt:
            bisect(line_end, max_alt, safe_pts, waypts, target, main_line)
        else:
            waypts[end] = safe_pt
            line = Line(end, target)
            bisect(line, max_alt, safe_pts, waypts, target, main_line)

def getPerpPoint(point, line, max_alt, left):
    '''
        Find a safe point to the left/right of given point.
    '''
    lat = point[0]
    lon = point[1]
    x_slope, y_slope = line.getSlopes()
    x_slope /= 10
    y_slope /= 10
    
    if left:
        y_slope = -1 * y_slope
    else:
        x_slope = -1 * x_slope
    
    lat += (y_slope)
    lon += (x_slope)
    while Altitude((lat, lon)).getAltitude() > max_alt:
        lat += (y_slope)
        lon += (x_slope)
    lat += (y_slope)
    lon += (x_slope)
    return (lat, lon)

def bisectObstacles(line, max_alt, start, end):
    '''
        Get waypoints that are safe and traverse them to reach the target.
    '''
    waypts = {start:None}
    safe_pts = PriorityQueue()
    bisect(line, max_alt, safe_pts, waypts, end, line)

    # create path from waypts dict
    path = [end]
    point = list(waypts)[-1]
    while point != start:
        path.append(point)
        point = waypts[point]
    path.append(point)
    path.reverse()

    # create path using points from path
    bisect_path = Line(start, start)
    for p in range(1,len(path)):
        new_line = Line(bisect_path.getPoint(-1), path[p])
        if new_line.getMaxAlt() <= max_alt:
            bisect_path.addLine(new_line)
    if end not in bisect_path.getLine():
        new_line = Line(bisect_path.getPoint(-1), end)
        bisect_path.addLine(new_line)

    return bisect_path


if __name__ == '__main__':
    range_in_kms = 30
    start, end = getTwoPoints(range_in_kms)

    # start = (52.552282, -9.091245) # BETTER SOLUTION
    # end = (52.382904, -8.815093)
    # start = (54.317747, -5.930471) # to test algorithms on WORKS
    # end = (54.262201, -6.341939)

    print("start =", start)
    print("end =", end)

    straight_line = Line(start, end)
    max_alt = Altitude(start).getAltitude() + 120
    straight_dist = straight_line.getTotalDistance()

    path = bisectObstacles(straight_line, max_alt, start, end)

    print()
    print("Drone Max Altitude:\t", max_alt)
    print("Bisect Max Altitude\t", path.getMaxAlt())
    print("Straight Max Altitude:\t", straight_line.getMaxAlt())
