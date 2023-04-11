from find_peaks import *
from crow_flies_v2 import *
from Circle import *
import haversine as hs
import time
from random_points import *

# get the start time
st = time.time()

# get altitudes from start to end
locations = ["Waterville", "Bantry", "Cork", "Dublin", "Longford", "Roscommon", "Athlone"]
coordinates = [(51.838353847600885, -10.156763362936477),
                (51.679318843246996, -9.451819063072634),
                (51.9121179892824, -8.476718670933947),
                (53.37731900994556, -6.234298920712984),
                (53.72581065734818, -7.792177930254111),
                (53.63852441535096, -8.204503237649801),
                (53.43955211234059, -7.924606329493087)]
# start =  coordinates[0] # waterville
# start = coordinates[1] # bantry
# end = coordinates[2] # cork
# end = coordinates[3] # dublin
start = coordinates[4] # longford
end = coordinates[5] # roscommon
end = coordinates[6] # Athlone

# start, end = getTwoPoints(15)

straight_line = getStraightLine(start, end)

# find all points above max altitude
max_alt = 85
peaks = findPeaks(straight_line, max_alt)

def drawCircles(inc=10):
    c = {}
    empty_vals = []
    for peak, radius in peaks.items():
        if radius > 0:
            circle = Circle(peak, straight_line)
            h0,h1 = circle.getCircle(radius, inc)

            c[peak] = h0
            c[peak].update(h1)
        else:
            empty_vals.append(peak)

    for key in empty_vals:
        del peaks[key]
    
    return c

def checkCircles():
    too_high = False
    for c in range(len(circles)):
        circle = circles[list(circles)[c]]
        max_on_circle = max(list(circle.values()))

        if max_on_circle > max_alt:
            peaks_key = list(peaks)[c]
            peaks[peaks_key] = peaks[peaks_key]*1.05
            too_high = True
    return too_high

inc = 1
circles = drawCircles(inc)
max_alt_on_path = max(list(straight_line.values()))
too_high = checkCircles()
while too_high:
    circles = drawCircles(inc)
    too_high = checkCircles()
# print(peaks)


points = [start]
num_steps = int(180/inc)
for c in circles:
    circle = circles[c]
    closest_point = (0,0)

    for p in circle:
        distance = math.dist(p, start)
        min_dist = math.dist(closest_point, start)
        
        if distance < min_dist:
            closest_point = p
    
   
    circle = list(circle)
    i = circle.index(closest_point)
    semi_circle = circle[i:] + circle[:i+1]
    semi_circle = semi_circle[:num_steps]
    points += semi_circle


i = 1
while i < len(points):
    j = 1
    c1 = points[i:i+num_steps]
    d1_start = math.dist(start,c1[0])
    d1_end = math.dist(end,c1[-1])
    while j < len(points):
        c2 = points[j:j+num_steps]
        d2_start = math.dist(start,c2[0])
        d2_end = math.dist(end,c2[-1])

        # print(i, j,d1_end,d2_end)

        if d1_start>d2_start and i<j:
            # print(1)
            points = points[:i] + points[i+num_steps:]
            i = i-num_steps
            break

        if d1_end<d2_end and i<j:
            # print(2)
            points = points[:j] + points[j+num_steps:]

        # print()
        j += num_steps

    i += num_steps


points.append(end)

circle_path = {}
circle_dist = 0

for point in range(len(points)-1):
    # print(points[point][0],points[point][1], sep=', ')
    line = getStraightLine(points[point], points[point+1])
    circle_dist += hs.haversine(points[point], points[point+1])
    circle_path.update(line)
    print(max(list(line.values())))

# print(points[-1][0],points[-1][1], sep=', ')
# print("max height", max(list(straight_line.values())))

# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st


print()
straight_dist = hs.haversine(start,end)
up_over_dist = straight_dist * 1000
for p in peaks:
    peak_alt = Altitude(p).getAltitude()
    up_over_dist += ((peak_alt+10) - max_alt)*2
up_over_dist /= 1000



# print("Start: {}".format(locations[coordinates.index(start)]))
# print("End: {}".format(locations[coordinates.index(end)]))
print("Start: {}".format(start))
print("End: {}".format(end))

print("Max altitude of drone: {}m".format(max_alt))
print("Straight line distance: {}km".format(round(straight_dist,2)))
print("Number of obstacles on path: {}".format(len(circles)))
print("\nPath 1 = going up and over; Path 2 = going around using circles\n")

print("-----------Path 1----------")
print("Distance flown: \t{}km".format(round(up_over_dist,2)))
max_alt_up_over = max(list(straight_line.values()))
print("Max altitude flown: \t{}m".format(max_alt_up_over))
height_up = max_alt_up_over+10-max_alt
height_down = max_alt_up_over+10-max_alt
print("Altitude change up: \t{}m".format(height_up))
print("Altitude change down: \t{}m".format(height_down))
extra_dist = round(up_over_dist-straight_dist, 2)
print("Extra distance flown: \t{}km".format(extra_dist))

print()

print("-----------Path 2----------")
print("Distance flown: \t{}km".format(round(circle_dist,2)))
print("Max altitude flown: \t{}m".format(max(list(circle_path.values()))))
extra_dist = round(circle_dist-straight_dist, 2)
print("Extra distance flown: \t{}km".format(extra_dist))

print()

print("Number of points on circle used: {}".format(360/inc))
print('Execution time: {} secs'.format(elapsed_time))

print()
# print(len(points))