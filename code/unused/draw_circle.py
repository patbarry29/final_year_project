from find_peaks import *
from crow_flies_v2 import *
from Circle import *

# get altitudes from start to end
start = (51.65550157494285, -9.461801748197177)
# start = (51.838353847600885, -10.156763362936477)
end = (53.37731900994556, -6.234298920712984)
straight_line = getStraightLine(start, end)

p1 = Altitude(start)

radius = .005
angle = 10
inc = 10

circle = Circle(start, straight_line)
positive, negative = circle.getCircle(radius, 90)

print(positive)
print(negative)

# -------------------------------------------------------------------------- #

# import matplotlib.pyplot as plt
# import numpy as np

# # x axis values = coordinate values
# x = [0]
# x1 = 0
# y = [p1.getAltitude()]
# for key, value in negative.items():
#     x1 += 10
#     x.append(x1)
#     y.append(value)
# print(x, y)


# # set figure size
# plt.figure(figsize=(15, 4))

# # plot points
# plt.plot(x, y)

# plt.xlabel('angle')
# plt.ylabel('altitude')

# plt.title('Elevation Change')

# # show graph
# plt.show()