from AreaMap import *
from a_star import *


range_in_kms = 100
start, end = getTwoPoints(range_in_kms)


# start = (52.552282, -9.091245) # BETTER SOLUTION
# end = (52.382904, -8.815093)

# start = (54.317747, -5.930471)
# end = (54.262201, -6.341939)

straight_line = Line(start, end)
max_alt = Altitude(start).getAltitude()+120

step_dist = 100
width = 29
st1 = time.time()
graph = AreaMap(start, end, width, max_alt, step_dist)


def getObsMap(graph):
    obstacle_map = {graph.getStart():[]}
    for line in graph._matrix:
        for point, val in line.items():
            if val == 'obs':
                obs = []
                obs_i1, obs_i2 = graph.getIndex(point)
                obs.append(graph.getPoint(max(0, obs_i1-1), obs_i2))
                obs.append(graph.getPoint(obs_i1, max(0, obs_i2-1)))
                if obs_i1 < len(graph.getMap())-1:
                    obs.append(graph.getPoint(obs_i1+1, obs_i2))
                if obs_i2 < graph.getWidth()-1:
                    obs.append(graph.getPoint(obs_i1, obs_i2+1))
                
                i = 0
                while i < len(obstacle_map):
                    p1 = list(obstacle_map.keys())[i]
                    adj_list = list(obstacle_map.values())[i]
                    for p2 in obs:
                        if p2[1] != 'obs':
                            obstacle_map[p2[0]] = []
                            obs_on_path = Line(p1, p2[0], 20).getMaxAlt()
                            if p2[0] in adj_list:
                                obstacle_map[p2[0]].append(p1)
                            elif obs_on_path < graph.getMaxAltDrone():
                                obstacle_map[p2[0]].append(p1)
                                adj_list.append(p2[0])
                    i += 1
                print(len(obstacle_map))
    return obstacle_map


# obs_map = getObsMap(graph)

# for p, adj_list in obs_map.items():
#     print(p, adj_list)
#     print()



# alt_matrix = graph.getMap()
# for line in alt_matrix:
#     print()
#     for point, dist in line.items():
#         point_alt = Altitude(point).getAltitude()
#         if point in obs_map:
#             print(' ', end=' ')
#         else:
#             print('#', end=' ')





# st = time.time()
path = a_starOptimised(graph, start, end)
et = time.time()
print("TIME", et-st1)



st = time.time()
a_path = a_star(graph, start, end)
et = time.time()
print("TIME", et-st)


# pts1 = getWaypoints(path, start, end)

# a_line = Line(0,0)
# for i in range(len(pts1)-1):
#     new_line = Line(pts1[i], pts1[i+1], 10)
#     a_line.addLine(new_line)

# print(max_alt, a_line.getMaxAlt())

# alt_matrix = graph.getMap()
# for line in alt_matrix:
#     print()
#     for point, dist in line.items():
#         point_alt = Altitude(point).getAltitude()
#         if point in a_line.getLine():
#             print(' ', end=' ')
#         elif dist != 'obs':
#             print('#', end=' ')
#         elif point_alt > max_alt+150:
#             print(' ', end=' ')
#         elif point_alt > max_alt+60:
#             print('-', end=' ')
#         elif dist == 'obs':
#             print('/', end=' ')

# print('\n'*10)
# print('start =', start)
# print('end =', end)
# # print(len(graph.getMap())*graph.getWidth())
# # print(len(obs_map))



print()