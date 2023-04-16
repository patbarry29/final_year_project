import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from scipy.interpolate import griddata

from bisect_obstacles import bisectObstacles
from circle_path_v1 import circleAlgV1
from circle_path_v2 import circleAlgV2
from find_peaks import findPeaks
from follow_edge import runFollowEdge
from pathfinding import *

'''
Code sourced from "https://github.com/13ff6/Topography_Map_Madagascar/blob/main/Mad_Regional_Map.py"
Plots paths retrieved from all algorithms on a coloured contour map.
'''

def makeFigure(path, col, num):
    '''
        Plot path with colour col on terrain background.
    '''
    cmap = plt.get_cmap('terrain')

    fig,ax = plt.subplots()

    tl = 5 # tick length
    tw = 1 # tick width
    lw = 3 # line width

    # make scatter plot with terrain information
    plt.scatter(x,y,1,z,cmap=cut_terrain_map)
    # make a colorbar as a legend
    cbar = plt.colorbar(label='Elevation above sea level (m)')
    cbar.ax.tick_params(size=3,width=1)
    cbar.ax.tick_params(which='major',direction='in',bottom=True, top=True, left=False, right=True,length=tl*2,width=tw+1,color='black')
    cbar.outline.set_linewidth(lw)

    plt.xlabel('Longitude (°)')
    plt.ylabel('Latitude (°)')

    # enforce x and y axis to be equal
    plt.gca().set_aspect('equal')
    plt.xlim(min(lon), max(lon))
    plt.ylim(min(lat), max(lat))
    plt.gca().invert_yaxis()
    plt.yticks(np.linspace(min(lat), max(lat), 6))

    ax.tick_params(colors='black')
    ax.spines['top'].set_linewidth(lw)
    ax.spines['bottom'].set_linewidth(lw)
    ax.spines['right'].set_linewidth(lw)
    ax.spines['left'].set_linewidth(lw)

    ax.tick_params(which='major',direction='in',bottom=True, top=True, left=True, right=True,length=tl*2,width=tw+1,color='black')
    ax.minorticks_on()
    ax.tick_params(which='minor',direction='in',bottom=True, top=True, left=True, right=True,length=tl+1.5,width=tw,color='black')
    
    # get x and y coords for path
    x1 = [pt[1] for pt in path.getLine()]
    y1 = [pt[0] for pt in path.getLine()]

    # plot path
    plt.plot(x1,y1, color=col)

    fig.suptitle('Contour Map for {} path below {}m'.format(algs[num], max_alt), fontsize=16)

    # plot start and end point of path
    path_start = path.getPoint(0)
    path_end = path.getPoint(-1)

    plt.plot(path_start[1],path_start[0], 'co')
    plt.text(path_start[1],path_start[0],'Start', color='black', ha='center')

    plt.plot(path_end[1],path_end[0], 'co')
    plt.text(path_end[1],path_end[0],'End', color='black', ha='center')

    fig.set_size_inches(5.2,5.5, forward=True)

    return fig, ax



range_in_kms = 30
try:
    start, end = getTwoPoints(range_in_kms)
except:
    start = (52.375697, -6.476178)
    end = (52.458768, -6.823477)

# start = (52.552282, -9.091245)
# end = (52.382904, -8.815093)
# start = (52.15479648262347, -10.269537344917408) # dingle to tralee
# end = (52.29349252772312, -9.708420947018718)

print("start =", start)
print("end =", end)
print()


straight_line = Line(start, end)
start_alt = Altitude(start).getAltitude()
max_alt = start_alt+120
step_dist = 100
width = 100

peaks = findPeaks(straight_line.getLine(), max_alt)
graph = AreaMap(start, end, width, max_alt, step_dist)

# ---------------Method 1 - Circle Algorithm--------------- #
inc = 1
try:
    pathv1 = circleAlgV1(peaks, straight_line.getLine(), inc, max_alt)
    print("Solution found for V1")
except:
    pathv1 = Line(start, end)
    print("No solution found for V1")
# ---------------Method 1 - Circle Algorithm--------------- #

# ---------------Method 2 - Circle Algorithm with Waypoints--------------- #
try:
    pathv2 = circleAlgV2(peaks, straight_line.getLine(), inc, max_alt)
    print("Solution found for V2")
except:
    pathv2 = Line(start, end)
    print("No solution found for V2")
# ---------------Method 2 - Circle Algorithm with Waypoints--------------- #

# ---------------Method 3 - Follow Edge--------------- #
try:
    step_dist = 100
    pathv3 = runFollowEdge(start, end, start_alt, straight_line, step_dist)
    print("Solution found for V3")
except:
    pathv3 = Line(start, end)
    print("No solution found for V3")
# ---------------Method 3 - Follow Edge--------------- #

# ---------------Method 4 - Greedy--------------- #
try:
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
# ---------------Method 5 - A*--------------- #


# # ---------------Method 6 - Bisect Obstacles--------------- #
# try:
#     pathv6 = bisectObstacles(straight_line, max_alt, start,end)
#     print("Solution found for V6")
# except:
#     pathv6 = Line(start, end)
#     print("No solution found for V6")
# # ---------------Method 6 - Bisect--------------- #


algs = ['Circles', 'Circles w/ Waypts', 'Follow Edge', 'Greedy', 'A*']

print(algs[0], pathv1.getMaxAlt(), sep=':\t\t')
print(algs[1], pathv2.getMaxAlt(), sep=':\t')
print(algs[2], pathv3.getMaxAlt(), sep=':\t\t')
print(algs[3], pathv4.getMaxAlt(), sep=':\t\t\t')
print(algs[4], pathv5.getMaxAlt(), sep=':\t\t\t')
# print(pathv6.getMaxAlt())

graph1 = graph.getMap()

# create dataset where each element is [lat,lon,alt]
ds = [[pt[0], pt[1], line[pt]] for line in graph1 for pt in line]
ds = np.asarray(ds)
lat = ds[:, 0]
lon = ds[:, 1]
alt = ds[:, 2]

num_pts = step_dist**3

# Combine the lower and upper range of the terrain colormap with a gap in the middle
# to let the coastline appear more prominently.
colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 56))
colors_land = plt.cm.terrain(np.linspace(0.25, 1, 200))

# combine them and build a new colormap
colors = colors_land
if min(alt) < 0: # if water present in map, must combine undersea and land
    colors = np.vstack((colors_undersea, colors_land))
cut_terrain_map = matplotlib.colors.LinearSegmentedColormap.from_list('cut_terrain', colors)


[x,y] = np.meshgrid(np.linspace(float(min(lon)), float(max(lon)), int(np.sqrt(num_pts))), np.linspace(float(min(lat)), float(max(lat)), int(np.sqrt(num_pts))))
z = griddata((lon, lat), alt, (x, y), method='linear')
x = np.matrix.flatten(x) # Gridded longitude
y = np.matrix.flatten(y) # Gridded latitude
z = np.matrix.flatten(z) # Gridded elevation
z_max = np.nanmax(z)

z[z<=0.] = z_max*-0.28302 # make all underwater points the same value
z[z>max_alt] = z_max  # make all points that are obstacles the same value

fig1, ax = makeFigure(pathv1, 'red', 0)

fig2, ax = makeFigure(pathv2, 'black',1)

fig3, ax = makeFigure(pathv3, 'green',2)

fig4, ax = makeFigure(pathv4, 'blue',3)

fig5, ax = makeFigure(pathv5, 'purple',4)

# fig6, ax = makeFigure(pathv6, 'white')

print()



plt.show()
