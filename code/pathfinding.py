import time
from AreaMap import *
from queue import PriorityQueue
# from copy_coords import write_to_clipboard
from random_points import *
from energy_consumption import *

'''
    File with Greedy and A* implementation
'''

def greedy(graph, start, end):
    '''
        Greedy algorithm implementation
        A node's neighbours are to the left, right, above and below.
    '''
    agenda = PriorityQueue()
    agenda.put((0,start))
    path = {start:None}
    costs = {start:0}
    max_alt = Altitude(start).getAltitude() + 120

    while agenda.qsize() > 0:
        curr_point = agenda.get()
        curr_point = curr_point[1]

        if curr_point == end:
            break
        
        # retrieve neighbours
        index1, index2 = graph.getIndex(curr_point)
        neighbours = getNeighbours(graph, index1, index2)

        for neighbour in neighbours:
            if neighbour[1] > max_alt:
                # if neighbour is an obstacle, skip
                continue
            cost_to_here = costs[curr_point] + 1
            if neighbour[0] not in costs or cost_to_here < costs[neighbour[0]]:
                costs[neighbour[0]] = cost_to_here
                dist_to_target = graph.getDist2Points(neighbour[0], end)
                potential_cost = dist_to_target
                index1, index2 = graph.getIndex(curr_point)
                agenda.put((potential_cost, neighbour[0]))
                path[neighbour[0]] = curr_point
    
    return path

def a_star(graph, fly_alt, start, end):
    '''
        Implementation of A* algorithm.
        Uses distance to current point, altitude, and turn angle to 
        evaluate the optimal path.
    '''
    agenda = PriorityQueue()
    agenda.put((0,start))
    path = {start:None}
    costs = {start:0}
    max_alt = Altitude(start).getAltitude() + 120
    max_alt_diff = max_alt-fly_alt # constant value of 40 in my tests

    while agenda.qsize() > 0:
        curr_point = agenda.get()
        curr_point = curr_point[1]

        if curr_point == end:
            break
        
        # retrieve neighbours
        index1, index2 = graph.getIndex(curr_point)
        neighbours = getNeighbours(graph, index1, index2)

        for neighbour in neighbours:
            if neighbour[1] > max_alt:
                continue
            new_dist = graph.getDist2Points(neighbour[0], curr_point)
            
            energy_used = evaluateEnergy(graph, path, curr_point, neighbour[0])

            # evaluate altitude
            factor = 0
            neighbour_alt = Altitude(neighbour[0]).getAltitude()
            if neighbour_alt > fly_alt:
                alt_difference = neighbour_alt-fly_alt # range = (1,max_alt_diff)
                factor = (alt_difference**2*(1000/(max_alt_diff**2)))/100
                # turn the # of metres flown above flying altitude into percentage
                # range of factor = (0.00625, 10)
            
            cost_to_here = costs[curr_point] + new_dist + (energy_used*(1+factor))
            if neighbour[0] not in costs or cost_to_here < costs[neighbour[0]]:
                costs[neighbour[0]] = cost_to_here
                energy_cost, w, a = getEnergy(neighbour[0], end)
                dist_to_target = graph.getDist2Points(neighbour[0], end)
                potential_cost = (cost_to_here*1) + (dist_to_target*1) + (energy_cost*(1+factor))
                agenda.put((potential_cost, neighbour[0]))
                path[neighbour[0]] = curr_point

    return path

def getNeighbours(graph, i1, i2):
    '''
        Get neighbours of a point using point's indices in the graph.
    '''
    neighbours = []
    if i1 < len(graph.getMap())-1:
        neighbours.append(graph.getPoint(i1+1, i2))
    if i2 < graph.getWidth()-1:
        neighbours.append(graph.getPoint(i1, i2+1))
    if i2 > 0:
        neighbours.append(graph.getPoint(i1, i2-1))
    if i1 > 0:
        neighbours.append(graph.getPoint(i1-1, i2))
    
    return neighbours

def evaluateEnergy(graph, path, curr_point, next_point):
    joules_used, w, a = getEnergy(next_point, curr_point)
    prev_pt = path[curr_point]
    if prev_pt != None:
        prev_i1, prev_i2 = graph.getIndex(prev_pt)
        next_i1, next_i2 = graph.getIndex(next_point)
        # check if drone moving diagonally
        if abs(next_i1-prev_i1) == 1 and abs(next_i2-prev_i2) == 1:
            prev_pt2 = path[prev_pt]
            prev_i1, prev_i2 = graph.getIndex(prev_pt2)
            curr_i1, curr_i2 = graph.getIndex(curr_point)
            # check if drone moving diagonally but changed direction
            if not (abs(curr_i1-prev_i1) == 1 and abs(curr_i2-prev_i2) == 1):
                joules_used *= 1.2
        
        # check if drone changed direction
        elif next_i1-prev_i1 == 1 or next_i2-prev_i2 == 1:
            joules_used *= 1.2
    
    return joules_used

# def a_starOptimised(graph, start, end):
#     '''
#         Uses the ObstacleMap obtained from the line function to 
#         decrease A* execution time.
#         However, massively increases execution time in building the graph.
#     '''
#     agenda = PriorityQueue()
#     agenda.put((0,start))
#     path = {start:None}
#     costs = {start:0}
#     obs_map = graph.getObsMap()

#     while agenda.qsize() > 0:
#         curr_point = agenda.get()
#         curr_point = curr_point[1]

#         if curr_point == end:
#             break

#         neighbours = obs_map[curr_point]
        
#         for neighbour in neighbours:
#             cost_to_here = costs[curr_point] + graph.getDist2Points(neighbour, curr_point)
#             if neighbour not in costs or cost_to_here < costs[neighbour]:
#                 costs[neighbour] = cost_to_here
#                 dist_to_target = graph.getDist2Points(neighbour, end)
#                 potential_cost = (cost_to_here*1) + (dist_to_target*1) # + (point_max*0)
#                 agenda.put((potential_cost, neighbour))
#                 path[neighbour] = curr_point
#     return path


def getWaypoints(path, start, end):
    '''
        Takes in a path dict and extracts waypoints from the end until 
        reaching the start point. 
        Returns waypoints list
    '''
    waypts = [end]
    point = list(path)[-1]
    while point != start:
        waypts.append(point)
        point = path[point]
    waypts.append(point)
    waypts.reverse()

    return waypts

def cleanPath(path, fly_alt, start, end, clean=True):
    '''
        If clean is True, will remove any unnecessary waypoints. 
        To do this, we check each set of 3 points in a row. If point 1 and 
        point 3 can be safely connected, then point 2 is unnecessary and 
        can be removed.
    '''
    waypts = getWaypoints(path, start, end)
    if clean:
        i = 0
        while i < len(waypts)-2:
            pt1 = waypts[i]
            pt2 = waypts[i+1]
            pt3 = waypts[i+2]
            test_line = Line(pt1, pt3, 20)
            if test_line.getMaxAlt() < fly_alt:
                waypts.remove(pt2)
            else:
                i += 1

    line = Line(0,0)
    for i in range(len(waypts)-1):
        new_line = Line(waypts[i], waypts[i+1])
        line.addLine(new_line)
    return line



if __name__ == '__main__':
    range_in_kms = 30
    start, end = getTwoPoints(range_in_kms)

    # start = (52.552282, -9.091245)
    # end = (52.382904, -8.815093)

    print("start=",start)
    print("end=",end)

    straight_line = Line(start, end)
    max_alt = Altitude(start).getAltitude() + 120
    fly_alt = max_alt-40

    step_dist = 100
    width = 200
    graph = AreaMap(start, end, width, max_alt, step_dist)

    st = time.time()
    g_path = greedy(graph, start, end)
    g_line = cleanPath(g_path, max_alt, start, end)
    et = time.time()
    print()
    print('greedy found in ', et-st)
    
    if g_line.getMaxAlt() > max_alt:
        sys.exit('No solution')
    # print()
    st = time.time()
    a_path = a_star(graph, fly_alt, start, end)
    a_line = cleanPath(a_path, max_alt, start, end)
    et = time.time()
    print("a star found in ", et-st)
    print()


    print('drone max alt:\t\t', max_alt)
    print('straight max alt:\t', straight_line.getMaxAlt())
    print('greedy max alt:\t\t', g_line.getMaxAlt())
    print('a* max alt:\t\t', a_line.getMaxAlt())
    print()
    print('dist straight:\t\t', straight_line.getTotalDistance())
    print('dist greedy:\t\t', g_line.getTotalDistance())
    print('dist a*:\t\t', a_line.getTotalDistance())

    # output = ''
    # for p in a_line.getLine():
    #     output += str(p[0]) + ', ' + str(p[1]) + '\n'
    # write_to_clipboard(output)