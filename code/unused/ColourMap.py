import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.colors
from Altitude import Altitude
from AreaMap import AreaMap
from Line import Line
from circle_path_v1 import circleAlgV1
from circle_path_v2 import circleAlgV2
from find_peaks import findPeaks
from follow_edge import runFollowEdge
from pathfinding import *


class FixPointNormalize(matplotlib.colors.Normalize):
    """ 
    Inspired by https://stackoverflow.com/questions/20144529/shifted-colorbar-matplotlib
    Subclassing Normalize to obtain a colormap with a fixpoint 
    somewhere in the middle of the colormap.
    This may be useful for a `terrain` map, to set the "sea level" 
    to a color in the blue/turquise range. 
    """
    def __init__(self, vmin=None, vmax=None, sealevel=0, col_val=0.21875, clip=False):
        # sealevel is the fix point of the colormap (in data units)
        self.sealevel = sealevel
        # col_val is the color value in the range [0,1] that should represent the sealevel.
        self.col_val = col_val
        matplotlib.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.sealevel, self.vmax], [0, self.col_val, 1]
        return np.ma.masked_array(np.interp(value, x, y))


range_in_kms = 20
start, end = getTwoPoints(range_in_kms)

# start = (52.552282, -9.091245) # BETTER SOLUTION
# end = (52.382904, -8.815093)
# start= (54.287751, -7.594472) # WORKS
# end= (54.391446, -7.457022)
# start = (53.621895, -9.481486)
# end = (53.763839, -9.4388)

print("start =", start)
print("end =", end)


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




# plt.close('all')

graph1 = graph.getMap()

df = [[pt[0], pt[1], line[pt]] for line in graph1 for pt in line]
df =np.asarray(df)
lat = df[:, 0]
lon = df[:, 1]
alt = df[:, 2]

num_pts = step_dist**3

# Combine the lower and upper range of the terrain colormap with a gap in the middle
# to let the coastline appear more prominently.
# inspired by https://stackoverflow.com/questions/31051488/combining-two-matplotlib-colormaps
colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 56))
colors_land = plt.cm.terrain(np.linspace(0.25, 1, 200))

# combine them and build a new colormap
colors = colors_land
if min(alt) < 0:
    colors = np.vstack((colors_undersea, colors_land))
cut_terrain_map = matplotlib.colors.LinearSegmentedColormap.from_list('cut_terrain', colors)

tl = 5
tw = 2
lw = 3
S = 30

[x,y] = np.meshgrid(np.linspace(float(min(lon)), float(max(lon)), int(np.sqrt(num_pts))), np.linspace(float(min(lat)), float(max(lat)), int(np.sqrt(num_pts))))
z = griddata((lon, lat), alt, (x, y), method='linear')
x = np.matrix.flatten(x) # Gridded longitude
y = np.matrix.flatten(y) # Gridded latitude
z = np.matrix.flatten(z) # Gridded elevation
z_max = np.nanmax(z)
z[z<0.] = z_max*-0.28302


cmap = plt.get_cmap('terrain')

fig,ax = plt.subplots()
plt.figure(figsize=(10, 9))

norm = FixPointNormalize(sealevel=0, vmin=np.nanmin(z), vmax=np.nanmax(z))

plt.scatter(x,y,1,z,cmap=cut_terrain_map)
cbar = plt.colorbar(label='Elevation above sea level [m]')
cbar.ax.tick_params(size=3,width=1)
cbar.ax.tick_params(which='major',direction='in',bottom=True, top=True, left=False, right=True,length=tl*2,width=tw+1,color='k')
cbar.outline.set_linewidth(lw)

plt.xlabel('Longitude [°]')
plt.ylabel('Latitude [°]')


plt.gca().set_aspect('equal')
plt.xlim(min(lon), max(lon))
plt.ylim(min(lat), max(lat))
plt.gca().invert_yaxis()
plt.yticks(np.linspace(min(lat), max(lat), 6))
np.linspace(-28,-10,19)
ax.set_yticks(np.linspace(min(lat), max(lat),19), minor=True)


ax.tick_params(colors='k')
ax.spines['top'].set_linewidth(lw)
ax.spines['bottom'].set_linewidth(lw)
ax.spines['right'].set_linewidth(lw)
ax.spines['left'].set_linewidth(lw)


ax.tick_params(which='major',direction='in',bottom=True, top=True, left=True, right=True,length=tl*2,width=tw+1,color='k')
ax.minorticks_on()
ax.tick_params(which='minor',direction='in',bottom=True, top=True, left=True, right=True,color='k',length=tl+1.5,width=tw)

plt.rcParams["font.family"] = "charter"
plt.rcParams.update({'font.size': S})
ax.set_yticks(np.linspace(min(lat), max(lat),19), minor=True)


x1 = [pt[1] for pt in pathv1.getLine()]
y1 = [pt[0] for pt in pathv1.getLine()]

x2 = [pt[1] for pt in pathv2.getLine()]
y2 = [pt[0] for pt in pathv2.getLine()]

x3 = [pt[1] for pt in pathv3.getLine()]
y3 = [pt[0] for pt in pathv3.getLine()]

x4 = [pt[1] for pt in pathv4.getLine()]
y4 = [pt[0] for pt in pathv4.getLine()]

x5 = [pt[1] for pt in pathv5.getLine()]
y5 = [pt[0] for pt in pathv5.getLine()]

# plt.plot(x1,y1, color='red')
plt.plot(x2,y2, color='white')
# plt.plot(x3,y3, color='black')
plt.plot(x4,y4, color='red')
plt.plot(x5,y5, color='black')

plt.title('Contour Map for paths below {}m'.format(max_alt), fontsize=26)

plt.show()
