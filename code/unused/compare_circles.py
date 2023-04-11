from circle_path_v1 import *
from circle_path_v2 import *
from find_peaks import *
from follow_edge import *
import time

# get 2 random points <= 60km away from each other
range_in_kms = 60
start, end = getTwoPoints(range_in_kms)
# print("start =", start)
# print("end =", end)

locations = ["Waterville", "Bantry", "Cork", "Dublin", "Longford", "Roscommon", "Athlone"]
coordinates = [(51.838353847600885, -10.156763362936477),
                (51.679318843246996, -9.451819063072634),
                (51.9121179892824, -8.476718670933947),
                (53.37731900994556, -6.234298920712984),
                (53.72581065734818, -7.792177930254111),
                (53.63852441535096, -8.204503237649801),
                (53.43955211234059, -7.924606329493087)]
start =  coordinates[0] # waterville
start = coordinates[1] # bantry
end = coordinates[2] # cork
# # end = coordinates[3] # dublin

# start= (55.043063, -6.77983) # WORKS
# end= (55.000384, -7.004581)
# start= (52.731114, -7.608729)# WORKS
# end= (52.73384, -7.405407)
# # start= (54.287751, -7.594472) # WORKS
# # end= (54.391446, -7.457022)
# start= (52.8838411, -8.5146466) # WORKS
# end= (53.0204914, -8.4933211)
# start= (51.9078787, -8.9924612) # WORK
# end= (51.768131, -8.9780161)
# start= (52.180058, -7.99371) # WORKS
# end= (52.325791, -7.999908)


straight_line = Line(start, end)
start_alt = Altitude(start).getAltitude()

# find all points above max altitude
max_alt = start_alt+120
peaks = findPeaks(straight_line.getLine(), max_alt)

inc = 1
# get the start time
st1 = time.time()
try:
    pathv1 = circleAlgV1(peaks, straight_line.getLine(), inc, max_alt)
except:
    pathv1 = Line(start, end)
    print("No solution found for V1")
et1 = time.time()
ex_time1 = et1-st1

st2 = time.time()
try:
    pathv2 = circleAlgV2(peaks, straight_line.getLine(), inc, max_alt)
except:
    pathv2 = Line(start, end)
    print("No solution found for V2")
et2 = time.time()
ex_time2 = et2-st2


max_straight = straight_line.getMaxAlt()

maxv1 = pathv1.getMaxAlt()
maxv2 = pathv2.getMaxAlt()

# print(max_alt)
# print(max_straight, maxv1, maxv2)
# print()
# print(ex_time1, ex_time2)

# print(len(pathv1), len(pathv2))


print()
print("start =", start)
print("end =", end)

print()

print("Distance between points\t\t", round(haversine(start, end), 2))

print("Drone max height\t\t",max_alt)
print("Max height as crow flies\t", max_straight)
print("# of obstacles\t\t\t", len(peaks))
print("Max height of v1\t\t", maxv1)
print("Max height of v2\t\t", maxv2)

print()

print("Execution time method 1:", ex_time1)
print("Execution time method 2:", ex_time2)