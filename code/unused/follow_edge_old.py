from random_points import *
from Line import *
from find_peaks import *


def getObstacles(line, max_alt):
    i = 0
    obstacles = []
    too_high = []
    for p in line:
        altitude = line[p]
        point_index = list(line).index(p)
        if altitude >= max_alt and point_index != len(line)-1:
            if len(too_high) == 0 and point_index > 0:
                # add start of obstacle
                too_high.append(list(line)[point_index-1])
            too_high.append(p)
        elif len(too_high) > 0:
            if point_index < len(line)-2:
                # add end of obstacle
                too_high.append(list(line)[point_index+1])
            obstacles.append([])
            obstacles[i] = [too_high[0], too_high[-1]]
            i += 1
            too_high = []

    return obstacles


def getSlope(start, end, step_dist):
    # get distance from start to end
    dist = haversine(start,end)
    dist /= (step_dist/1000)
    # find x values that are 'step_dist' metres apart
    x_slope = (start[0]-end[0]) / dist
    # find y values that are 'step_dist' metres apart
    y_slope = (start[1]-end[1]) / dist
    return x_slope, y_slope


def getObstacleEnds(start, end, x_slope, y_slope, dist=100):
    if dist != 100:
        x_slope, y_slope = getSlope(start, end, step_dist)
    if start[0] > end[0]:
        start_lat = start[0] - (x_slope)
        start_lon = start[1] - (y_slope)
        end_lat = end[0] + (x_slope)
        end_lon = end[1] + (y_slope)
    else:
        start_lat = start[0] + (x_slope)
        start_lon = start[1] + (y_slope)
        end_lat = end[0] - (x_slope)
        end_lon = end[1] - (y_slope)
    
    return (start_lat, start_lon), (end_lat, end_lon)


def findPoint(point, max_alt, x_slope, y_slope, left):
    lat = point[0]
    lon = point[1]
    if left:
        # print(point[0], point[1], sep=', ')
        lat -= (y_slope)
        lon += (x_slope)
        while Altitude((lat, lon)).getAltitude() > max_alt:
            # print(lat, lon, sep=', ')
            lat -= (y_slope)
            lon += (x_slope)
    else:
        lat += (y_slope)
        lon -= (x_slope)
        while Altitude((lat, lon)).getAltitude() > max_alt:
            lat += (y_slope)
            lon -= (x_slope)

    # print(lat, lon, sep = ', ')

    return (lat, lon)


def findEdge(point, i, pts_list, max_alt, x_slope, y_slope, step_dist, left):
    pts_dict = {}
    if point == (54.287751, -7.594472):
        print(point, i, len(pts_list))
    # point = findPoint(point, max_alt, x_slope, y_slope, left)
    test_line = Line(point, pts_list[-1], step_dist)
    pts_dict[point] = test_line.getMaxAlt()
    count = 0
    while test_line.getMaxAlt() > max_alt:
        if count < (500/step_dist):
            point = findPoint(point, max_alt, x_slope, y_slope, left)
            test_line = Line(point, pts_list[-1], step_dist)
            pts_dict[point] = test_line.getMaxAlt()
            count += 1
        else:
            min_point = min(pts_dict.items(), key=lambda x: x[1])
            point = min_point[0]
            test_line = Line(point, pts_list[-1], step_dist)
            break
    
    obs_max_alt = test_line.getMaxAlt()
    # print(obs_max_alt, left)
    # if test_line.getMaxAlt() > max_alt:
    #     print(test_line.getMaxAlt(), max_alt, '\t', i, left)
    pts_list.append(point)

    return obs_max_alt


def followEdge(start, end, line, obstacles, max_alt, x_slope, y_slope, step_dist):
    checkpoints = [start]
    # print("IM HEREEEEEEEEE")
    # print(start[0], start[1], sep=', ')
    print("Maximum altitude of the UAV: {}m".format(max_alt))
    for obstacle in obstacles:
        # for p in obstacle:
        #     print(p[0], p[1], sep=', ')

        obs_num = obstacles.index(obstacle)
        print("On obstacle", obs_num+1, end=' - ')
        # if obstacle[0] == obstacle[1]:
        #     obstacles.remove(obstacle)
        #     # print("go left")
        #     s1, s2 = line.getSteps()
        #     obs_start, obs_end = getObstacleEnds(obstacle[0], obstacle[1], s1, s2)
        #     checkpoints.append(obs_start)
        #     findEdge(obstacle[0], 0, checkpoints, max_alt, x_slope, y_slope, step_dist, left=True)
        #     checkpoints.append(obs_end)
        #     continue
        # store start point of obstacle
        # s1, s2 = line.getSteps()
        # obs_start, obs_end = getObstacleEnds(obstacle[0], obstacle[1], s1, s2)
        # checkpoints.append(obstacle[0])

        # print(obs_start, start)

        obs_line = Line(obstacle[0], obstacle[1], step_dist)
        print(obstacle[0])

        # print(obs_line.getPoint(0)[0], obs_line.getPoint(0)[1], sep=', ')
        left_path = checkpoints.copy()
        i = 0
        left_max_alt = 0
        while i < obs_line.getLength():
            point = obs_line.getPoint(i)
            temp_max_alt = findEdge(point, i, left_path, max_alt, x_slope, y_slope, step_dist, left=True)
            left_max_alt = max(temp_max_alt, left_max_alt)
            i += 1
        
        right_path = checkpoints.copy()
        i = 0
        right_max_alt = 0
        while i < obs_line.getLength():
            point = obs_line.getPoint(i)
            temp_max_alt = findEdge(point, i, right_path, max_alt, x_slope, y_slope, step_dist, left=False)
            right_max_alt = max(temp_max_alt, right_max_alt)
            i += 1

        left = True
        if left_max_alt < right_max_alt:
            print("go left with a maximum of {}m".format(left_max_alt))
            checkpoints += left_path[1:]
        else:
            print("go right with a maximum of {}m".format(right_max_alt))
            checkpoints += right_path[1:]
            left = False
        # print(obs_line.getPoint(-1)[0], obs_line.getPoint(-1)[1], sep=', ')

    # if len(obstacles) > 1:
    #     print("CHECK LAST POINT")
    #     test_line = Line(checkpoints[-1], end, step_dist)
    #     p, new_end = getObstacleEnds(start, obs_line.getPoint(-1), x_slope, y_slope, step_dist)
    #     d1 = haversine(new_end, end)
    #     while test_line.getMaxAlt() > max_alt:
    #         p, new_end = getObstacleEnds(start, new_end, x_slope, y_slope, step_dist)
    #         d2 = haversine(new_end, end)
    #         # print(d1, d2)
    #         if d2 > d1:
    #             break
    #         # print(test_line.getMaxAlt(), i)
    #         # print(haversine(new_end, end))
    #         d1 = haversine(new_end, end)
    #         findEdge(new_end, i, checkpoints, max_alt, x_slope, y_slope, step_dist, left)
    #         test_line = Line(new_end, end, step_dist)
    #         i+=1
        
    # print(end[0],end[1], sep=', ')
    checkpoints += [end]
    return checkpoints


def createPath(pts_list, step_dist):
    path = Line(0,0)
    for i in range(len(pts_list)-1):
        line = Line(pts_list[i],pts_list[i+1], step_dist)
        path.addLine(line)
        # print(pts_list[i][0], pts_list[i][1], sep = ', ')
        # print(i, path.getMaxAlt(), path.getLength())
    return path































if __name__ == "__main__":
    range_in_kms = 30
    start, end = getTwoPoints(range_in_kms)
    # start= (52.8838411, -8.5146466) # 1 obstacles
    # end= (53.0204914, -8.4933211)
    # start= (51.9078787, -8.9924612) # 1 obstacles
    # end= (51.768131, -8.9780161)
    # start= (52.180058, -7.99371) # 1 obstacle
    # end= (52.325791, -7.999908)
    # start= (52.429367, -9.317902) # 2 obstacles
    # end= (52.296735, -9.136351)
    # start= (53.600975, -9.901837) # 2
    # end= (53.703304, -9.653155)
    # start= (54.026801, -7.949722) # 3 obstacles
    # end= (54.119972, -8.004171)
    # start= (55.066292, -8.152927) # 3 obstacles
    # end= (54.983136, -8.027814)
    # start= (54.28975, -7.980695) # 4 obstacles
    # end= (54.257052, -7.806686)

    # start= (53.569554, -9.490858) # 1 obstacle
    # end= (53.594508, -9.705984)

    # start= (53.539344, -9.678252)
    # end= (53.400684, -10.042603)

    # start= (54.287751, -7.594472) # 5 obstacles
    # end= (54.391446, -7.457022)

    # start= (55.043063, -6.77983) # 1 obstacle, WORKS
    # end= (55.000384, -7.004581)
    # start= (52.731114, -7.608729)# 1 obstacle, WORKS
    # end= (52.73384, -7.405407)
    # start= (52.380765, -8.32299)
    # end= (52.301254, -8.118864)
    print("start=", start)
    print("end=", end)
    
    
    start_alt = Altitude(start).getAltitude()
    max_alt = start_alt+120
    # max_alt = start_alt

    step_dist = 50

    straight_line = Line(start, end, step_dist)

    obstacles = getObstacles(straight_line.getLine(), max_alt)
    print(len(obstacles))


    x_slope, y_slope = getSlope(start, end, step_dist)

    checkpoints = followEdge(start, end, obstacles, max_alt, x_slope, y_slope)
    # try:
        # checkpoints = followEdge(start, end, obstacles, max_alt, x_slope, y_slope)
    # except:
    #     print("No solution found")

    edge_path = createPath(checkpoints, step_dist)

    # print(start[0], start[1], sep=', ')
    # for o in obstacles:
    #     for p in o:
    #         print(p[0], p[1], sep=', ')
    # print(end[0], end[1], sep=', ')
    # for point in edge_path.getLine():
    #     print(point[0], point[1], sep=', ')

    # print(edge_path.getLength())

    print()
    print("drone max\t",start_alt+120)

    print("Straight max\t",straight_line.getMaxAlt())

    print("edge max\t",edge_path.getMaxAlt())

    # print(haversine(start, end))

    # print(start_alt, Altitude(end).getAltitude())