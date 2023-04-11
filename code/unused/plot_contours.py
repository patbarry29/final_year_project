import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
from Altitude import Altitude
from AreaMap import AreaMap
from Line import Line
from circle_path_v1 import circleAlgV1
from circle_path_v2 import circleAlgV2
from find_peaks import findPeaks
from follow_edge import runFollowEdge
from pathfinding import *

range_in_kms = 40
start, end = getTwoPoints(range_in_kms)
start= (54.287751, -7.594472) # WORKS
end= (54.391446, -7.457022)

straight_line = Line(start, end)
start_alt = Altitude(start).getAltitude()
max_alt = start_alt+120
step_dist = 100
width = 300

peaks = findPeaks(straight_line.getLine(), max_alt)

graph = AreaMap(start, end, width, max_alt, step_dist)


# # ---------------Method 1 - Circle Algorithm--------------- #
# inc = 1
# try:
#     pathv1 = circleAlgV1(peaks, straight_line.getLine(), inc, max_alt)
#     print("Solution found for V1")
# except:
#     pathv1 = Line(start, end)
#     print("No solution found for V1")
# # ---------------Method 1 - Circle Algorithm--------------- #

# # ---------------Method 2 - Circle Algorithm with Waypoints--------------- #
# try:
#     pathv2 = circleAlgV2(peaks, straight_line.getLine(), inc, max_alt)
#     print("Solution found for V2")
# except:
#     pathv2 = Line(start, end)
#     print("No solution found for V2")
# # ---------------Method 2 - Circle Algorithm with Waypoints--------------- #

# # ---------------Method 3 - Follow Edge--------------- #
# try:
#     step_dist = 100
#     pathv3 = runFollowEdge(start, end, start_alt, straight_line, step_dist)
#     print("Solution found for V3")
# except:
#     pathv3 = Line(start, end)
#     print("No solution found for V3")
# # ---------------Method 3 - Follow Edge--------------- #

# # ---------------Method 4 - Greedy--------------- #
# try:
#     # width = 300
#     fly_alt = start_alt + 80
#     graph = AreaMap(start, end, width, max_alt, step_dist)
#     waypts = greedy(graph, start, end)
#     pathv4 = cleanPath(waypts, fly_alt, start, end, True)
#     print("Solution found for V4")
# except:
#     pathv4 = Line(start, end)
#     print("No solution found for V4")
# maxv4 = pathv4.getMaxAlt()
# # ---------------Method 4 - Greedy--------------- #


# # ---------------Method 5 - A*--------------- #
# pathv5 = 0
# if maxv4 <= max_alt+1:
#     waypts = a_star(graph, fly_alt, start, end)
#     pathv5 = cleanPath(waypts, fly_alt, start, end, True)
#     print("Solution found for V5")
# else:
#     pathv5 = Line(start, end)
#     print("No solution found for V5")
# # ---------------Method 5 - A*--------------- #

graph1 = graph.getMap()

df = [[pt[0], pt[1], line[pt]] for line in graph1 for pt in line]
df =np.asarray(df)
lat = df[:, 0]
lon = df[:, 1]
alt = df[:, 2]

num_pts = step_dist**3

[x,y] = np.meshgrid(np.linspace(float(min(lon)), float(max(lon)), int(np.sqrt(num_pts))), np.linspace(float(min(lat)), float(max(lat)), int(np.sqrt(num_pts))))
z = griddata((lon, lat), alt, (x, y), method='linear')
x = np.matrix.flatten(x) #Gridded longitude
y = np.matrix.flatten(y) #Gridded latitude
z = np.matrix.flatten(z) #Gridded elevation

# plt.figure(figsize=(10,10))

plt.scatter(x,y,1,z,cmap='terrain')
plt.colorbar(label='Elevation above sea level [m]')
plt.xlabel('Longitude [°]')
plt.ylabel('Latitude [°]')

# x1 = [pt[1] for pt in pathv1.getLine()]
# y1 = [pt[0] for pt in pathv1.getLine()]

# x2 = [pt[1] for pt in pathv2.getLine()]
# y2 = [pt[0] for pt in pathv2.getLine()]

# x3 = [pt[1] for pt in pathv3.getLine()]
# y3 = [pt[0] for pt in pathv3.getLine()]

# x4 = [pt[1] for pt in pathv4.getLine()]
# y4 = [pt[0] for pt in pathv4.getLine()]

# x5 = [pt[1] for pt in pathv5.getLine()]
# y5 = [pt[0] for pt in pathv5.getLine()]

# plt.plot(x1,y1, color='red')
# plt.plot(x2,y2, color='white')
# plt.plot(x3,y3, color='black')
# plt.plot(x4,y4, color='green')
# plt.plot(x5,y5, color='yellow')

plt.gca().set_aspect('equal')

plt.show()