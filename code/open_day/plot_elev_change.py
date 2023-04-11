import matplotlib.pyplot as plt
import numpy as np
from AreaMap import AreaMap
from Line import *
from circle_path_v1 import *
from circle_path_v2 import *
from find_peaks import *
from follow_edge import *
from pathfinding import *
from random_points import *

range_in_kms = 30
try:
    start, end = getTwoPoints(range_in_kms)
except:
    print('fail')
    start = (52.552282, -9.091245)
    end = (52.382904, -8.815093)



straight_line = Line(start, end)
start_alt = Altitude(start).getAltitude()

# find all points above max altitude
max_alt = start_alt+120
peaks = findPeaks(straight_line.getLine(), max_alt)

# ---------------PRINT SOME INFORMATION--------------- #
max_straight = straight_line.getMaxAlt()
dist_flown = round(haversine(start, end), 2)
print()
print("start =", start)
print("end =", end)

print()

print("Distance between points\t\t {}km".format(dist_flown))

print("Drone max height\t\t {}m".format(max_alt))
print("Max height as crow flies\t {}m".format(max_straight))
print("# of obstacles\t\t\t", len(peaks))
# ---------------PRINT SOME INFORMATION--------------- #

print()

# ---------------Method 1 - Circle Algorithm--------------- #
inc = 1
try:
    pathv1 = circleAlgV1(peaks, straight_line.getLine(), inc, max_alt)
    print("Solution found for V1")
except:
    pathv1 = Line(start, end)
    print("No solution found for V1")
maxv1 = pathv1.getMaxAlt()
# ---------------Method 1 - Circle Algorithm--------------- #

# print()

# ---------------Method 2 - Circle Algorithm with Waypoints--------------- #
try:
    pathv2 = circleAlgV2(peaks, straight_line.getLine(), inc, max_alt)
    print("Solution found for V2")
except:
    pathv2 = Line(start, end)
    print("No solution found for V2")
maxv2 = pathv2.getMaxAlt()
# ---------------Method 2 - Circle Algorithm with Waypoints--------------- #

# print()

# ---------------Method 3 - Follow Edge--------------- #
try:
    step_dist = 100
    pathv3 = runFollowEdge(start, end, start_alt, straight_line, step_dist)
    print("Solution found for V3")
except:
    pathv3 = Line(start, end)
    print("No solution found for V3")
maxv3 = pathv3.getMaxAlt()
# ---------------Method 3 - Follow Edge--------------- #



# ---------------Method 4 - Greedy--------------- #
try:
    step_dist = 50
    width = 300
    fly_alt = start_alt + 80
    graph = AreaMap(start, end, width, max_alt, step_dist)
    waypts = greedy(graph, start, end)
    pathv4 = cleanPath(waypts, fly_alt, start, end, True)
    print("Solution found for V4")
except:
    pathv4 = Line(start, end)
    print("No solution found for V4")
maxv4 = pathv4.getMaxAlt()
# ---------------Method 4 - Greedy--------------- #


# ---------------Method 5 - A*--------------- #
pathv5 = 0
if maxv4 <= max_alt+1:
    waypts = a_star(graph, fly_alt, start, end)
    pathv5 = cleanPath(waypts, fly_alt, start, end, True)
    print("Solution found for V5")
else:
    pathv5 = Line(start, end)
    print("No solution found for V5")
maxv5 = pathv5.getMaxAlt()
# ---------------Method 5 - A*--------------- #



def plotAltChange(path, num, max_alt):
    

    # plot points
    plt.plot(x, y)
    
    # set figure size
    plt.figure(figsize=(15, 4))

    # plot fly alt
    fly_alt = [max_alt-40] * len(y)
    plt.plot(x, fly_alt, linestyle='dashed')
    
    # plot max alt
    max_alt = [max_alt] * len(y)
    plt.plot(x, max_alt, linestyle='dashed')
    

    plt.xlabel('Distance (km)')
    plt.ylabel('Altitude (m)')

    plt.title('Elevation Change for Path {}'.format(num))

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)

paths = [pathv1, pathv2, pathv3,pathv4,pathv5]
subplots = [ax1, ax2, ax3, ax4, ax5]

for i in range(len(paths)):
    path = paths[i]
    path.adjustAlts()
    path = path.getLine()
    # x axis values = coordinate values
    x = []
    for num in np.arange(0, len(path)/10, 1/10):
        x.append(num)
    # y axis values = altitude values
    y = path.values()
    
    max_alt_list = [max_alt] * len(y)

    if i > 2:
        subplots[i].set_xlabel('Distance (km)')
    subplots[i].set_ylabel('Altitude (m)')
    subplots[i].set_title('Path {}'.format(i+1))
    subplots[i].plot(x, y)

    # plot max alt
    subplots[i].plot(x, max_alt_list, linestyle='dashed')



fig.suptitle('Elevation Change')

# plotAltChange(pathv1, 1, max_alt)
# plotAltChange(pathv2, 2, max_alt)
# plotAltChange(pathv3, 3, max_alt)
# plotAltChange(pathv4, 4, max_alt)
# plotAltChange(pathv5, 5, max_alt)

plt.show()
