from find_peaks import *
from up_and_over import *
from Circle import *
from draw_circles import *
from random_points import *
import time

def separateCircles():
    for c in circles:
        circle = circles[c]
        closest_point = (0,0)

        for p in circle:
            distance = math.dist(p, start)
            min_dist = math.dist(closest_point, start)

            if distance < min_dist:
                closest_point = p

        circle_l = list(circle)
        i = circle_l.index(closest_point)
        circle_l = circle_l[i:] + circle_l[:i+1]
        semi_circle1 = circle_l[:num_steps]
        semi_circle2 = [circle_l[0]] + circle_l[:num_steps+1:-1]

        semi_circle1_d = {}
        for p in semi_circle1:
            semi_circle1_d[p] = circle[p]
        
        semi_circle2_d = {}
        for p in semi_circle2:
            semi_circle2_d[p] = circle[p]

        try:
            max1 = max(semi_circle1_d.values())
            max2 = max(semi_circle2_d.values())
        except:
            sys.exit("no solution")
        
        if max1 < max2:
            circles[c] = semi_circle1_d
            
            # print(list(circles).index(c), max1, max2)
        else:
            # print(max1, max2)
            circles[c] = semi_circle2_d
            # print()


def checkCircles():
    too_high = False
    for c in range(len(circles)):
        circle = circles[list(circles)[c]]
        try:
            max_on_circle = max(list(circle.values()))
        except:
            sys.exit("no solution")

        if max_on_circle > max_alt:
            peaks_key = list(peaks)[c]
            peaks[peaks_key] = peaks[peaks_key]*1.05
            too_high = True
    return too_high


# get the start time
st = time.time()

r = int(input("Input drone range (in kms): "))
start, end = getTwoPoints(r)
# start = (55.338058, -7.330358)
# end = (54.5548, -7.253277)

straight_line = getStraightLine(start, end)
start_alt = Altitude(start).getAltitude()

# find all points above max altitude
max_alt = start_alt+120
peaks = findPeaks(straight_line, max_alt)


level = [10, 1, 0.1]
inc = level[int(input("More or less points used on the circle (1/2/3): "))-1]

num_steps = int(180/inc)
circles = drawCircles(peaks, straight_line, inc)
separateCircles()
too_high = checkCircles()
while too_high:
    circles = drawCircles(peaks, straight_line, inc)
    separateCircles()
    too_high = checkCircles()


points = [start]
for c in circles:
    circle = circles[c]
    for p in circle:
        points.append(p)

points.append(end)

circle_path = {}
print()
for point in range(len(points)-1):
    # print(points[point][0], points[point][1], sep=', ')
    line = getStraightLine(points[point], points[point+1])
    circle_path.update(line)
# print(end[0], end[1], sep=', ')

print()
print("start =", start)
print("end =", end)

print()

print("Drone max height\t\t",max_alt)
print("Max height as crow flies\t", max(list(straight_line.values())))
print("# of obstacles\t\t\t", len(peaks))
print("Max height of new path\t\t", max(list(circle_path.values())))
