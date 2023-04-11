import haversine as hs
from Altitude import *

start = (51.68224740443309, -9.446598226237537)
end = (53.37731900994556, -6.234298920712984)
distance = hs.haversine(start, end)

separate = 0.1

# we will measure the altitude every 100m from start to finish
# so to find the new coords we must divide distance by .1
new_dist = distance/separate

# we will then subtract start latitude from end latitude
# and repeat for longitude
lat_dist = start[0] - end[0]
lon_dist = start[1] - end[1]

# then divide these by new distance to get number we must add
lat_sum = lat_dist / new_dist
lon_sum = lon_dist / new_dist

lat, lon = start[0], start[1]

# now start a loop to find altitude at each point
elevation = []
if lat < end[0]:
    while lat < end[0]:
        alt = Altitude((lat, lon))
        elevation.append(alt.getAltitude())
        lat -= lat_sum
        lon -= lon_sum
else:
    while lat > end[0]:
        alt = Altitude((lat, lon))
        elevation.append(alt.getAltitude())
        lat -= lat_sum
        lon -= lon_sum


alt = Altitude(end)
elevation.append(alt.getAltitude())
print()
print(max(elevation))
print()

#--------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

# x axis values = coordinate values
x = []
for i in np.arange(0, distance+separate, separate):
    x.append(i)

# y axis values = altitude values
y = elevation

# set figure size
plt.figure(figsize=(18, 4))

# plot points
plt.plot(x, y)

plt.xlabel('distance')
plt.ylabel('altitude')

plt.title('Elevation Change')

# show graph
plt.show()