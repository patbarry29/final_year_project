from AreaMap import *
from pathfinding import *
from follow_edge import *

range_in_kms = 30
start, end = getTwoPoints(range_in_kms)

# start = (54.317747, -5.930471) # to test algorithms on
# end = (54.262201, -6.341939)

# start= (53.589281, -9.286851) # A* BETTER
# end= (53.469393, -9.664609)

start = (52.552282, -9.091245) # BETTER SOLUTION
end = (52.382904, -8.815093)

# start=(52.083474, -8.971788) # a* better
# end=(51.845846, -9.059459)

# start= (54.90919, -6.503733) # 1 km less than greedy
# end= (54.880591, -6.373118)

# start = (54.922688, -7.105262) # a* better
# end = (55.11686, -7.402312)

# start = (54.122147, -6.750097)
# end = (54.242453, -6.614721)

# start= (52.496613, -8.914968) # long exec time, a star much better route
# end= (53.190386, -6.809367)

# start = (52.882839, -8.181586) # has to go backwards away from goal and does do that
# end = (52.688233, -8.265582)

# start = (54.707204, -6.951608) # short exec, a star better
# end = (54.808895, -7.367185)


output = 'start = ' + str(start) + '\nend = ' + str(end)
write_to_clipboard(output)


straight_line = Line(start, end)
start_alt = Altitude(start).getAltitude()
max_alt = start_alt+120
# max_alt = 200

# print(max_alt)

step_dist = 60
width = 200

graph1 = AreaMap(start, end, width, max_alt, step_dist)
# graph2 = AreaMap(start, end, width, max_alt-60, step_dist)

path1 = greedy(graph1, start, end)
path = cleanPath(path1, max_alt, start, end)
if path.getMaxAlt() > max_alt:
        sys.exit('No solution')
print('greedy found')
path2 = a_star(graph1, start_alt+80, start, end)
# path2 = a_star(graph2, start, end)
# path2 = path1

pts1 = getWaypoints(path1, start, end)
pts2 = getWaypoints(path2, start, end)

path1 = Line(0,0)
for i in range(len(pts1)-1):
    path1.addLine(Line(pts1[i], pts1[i+1]))

path2 = Line(0,0)
for i in range(len(pts2)-1):
    path2.addLine(Line(pts2[i], pts2[i+1]))

alt_matrix = graph1.getMap()
for line in alt_matrix:
    print()
    for point, dist in line.items():
        point_alt = Altitude(point).getAltitude()

        if point in pts1:
            print(' ', end=' ')
        # elif point in pts2:
        #     print('#', end=' ')
        elif point_alt < max_alt:
            print('1', end=' ')
        elif point_alt > max_alt+180:
            print(' ', end=' ')
        elif point_alt >= max_alt+60:
            print('-', end=' ')
        else:
            print('/', end=' ')

# path1 = cleanPath(path1, max_alt, start, end)
# path2 = cleanPath(path2, max_alt, start, end)
# alt_matrix = graph1.getMap()
# for line in alt_matrix:
#     dist1 = 1
#     dist2 = 1
#     print()
#     for point, info in line.items():
#         point_alt = Altitude(point).getAltitude()
#         p1 = point
#         for p in path1.getLine():
#             new_dist = graph1.getDist2Points(point, p)
#             if new_dist < dist1:
#                 dist1 = new_dist
#                 p1 = p
#         for p in path2.getLine():
#             new_dist = graph1.getDist2Points(point, p)
#             if new_dist < dist2:
#                 dist2 = new_dist
#                 p1 = p
#         if dist1 < 0.0009:
#             dist1 = 1
#             print(' ', end=' ')
#         if dist2 < 0.0009:
#             dist2 = 1
#             print('#', end=' ')
#         elif info != 'obs':
#             print('1', end=' ')
#         elif point_alt > max_alt+180:
#             print(' ', end=' ')
#         elif point_alt >= max_alt+60:
#             print('-', end=' ')
#         elif info == 'obs':
#             print('/', end=' ')


print('\n'*10)
print('start =', start)
print('end =', end)