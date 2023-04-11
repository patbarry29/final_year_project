from circle_path_v1 import *
from circle_path_v2 import *
from copy_coords import write_to_clipboard
from find_peaks import *
from follow_edge import *
import time

# get 2 random points <= 60km away from each other
range_in_kms = 30
start, end = getTwoPoints(range_in_kms)
# print("start =", start)
# print("end =", end)

# locations = ["Waterville", "Bantry", "Cork", "Dublin", "Longford", "Roscommon", "Athlone"]
coordinates = [(51.838353847600885, -10.156763362936477),
                (51.679318843246996, -9.451819063072634),
                (51.9121179892824, -8.476718670933947),
                (53.37731900994556, -6.234298920712984),
                (53.72581065734818, -7.792177930254111),
                (53.63852441535096, -8.204503237649801),
                (53.43955211234059, -7.924606329493087)]
start =  coordinates[0] # waterville
# start = coordinates[1] # bantry
end = coordinates[2] # cork
end = coordinates[3] # dublin

# start= (55.043063, -6.77983) # WORKS
# end= (55.000384, -7.004581)
start= (52.731114, -7.608729)# WORKS
end= (52.73384, -7.405407)
# start= (54.287751, -7.594472) # WORKS
# end= (54.391446, -7.457022)
# start= (52.8838411, -8.5146466) # WORKS
# end= (53.0204914, -8.4933211)
# start= (51.9078787, -8.9924612) # WORK
# end= (51.768131, -8.9780161)
# start= (52.180058, -7.99371) # WORKS
# end= (52.325791, -7.999908)

# start = (52.056149, -9.050187)
# end = (51.842924, -8.850821)

# start= (52.399719, -7.956214)
# end= (52.152894, -8.01815)


straight_line = Line(start, end)
start_alt = Altitude(start).getAltitude()

# find all points above max altitude
max_alt = start_alt + 120
peaks = findPeaks(straight_line.getLine(), max_alt)

# ---------------PRINT SOME INFORMATION--------------- #

max_straight = straight_line.getMaxAlt()
print()
print("start =", start)
print("end =", end)

print()

print("Distance between points\t\t {}km".format(round(haversine(start, end), 2)))

print("Drone max height\t\t {}m".format(max_alt))
print("Max height as crow flies\t {}m".format(max_straight))
print("# of obstacles\t\t\t", len(peaks))

# ---------------PRINT SOME INFORMATION--------------- #

print()

# ---------------Method 1 - Circle Algorithm--------------- #
inc = 1
# get the start time
st1 = time.time()
try:
    pathv1 = circleAlgV1(peaks, straight_line.getLine(), inc, max_alt)
    
    print("Solution found for V1")
    et1 = time.time()

    ex_time1 = et1-st1
    maxv1 = pathv1.getMaxAlt()
    
    print("Max height of v1\t\t {}m".format(maxv1))
    print("Average height flown v1\t\t {}m".format(pathv1.getAverageAlt()))
    print("Distance flown v1\t\t {}km".format(pathv1.getTotalDistance()))
    print("Execution time v1: \t\t {}s".format(round(ex_time1, 2)))
except:
    pathv1 = Line(start, end)
    print("No solution found for V1")
# ---------------Method 1 - Circle Algorithm--------------- #

print()

# ---------------Method 2 - Circle Algorithm with Checkpoints--------------- #
st2 = time.time()
try:
    pathv2 = circleAlgV2(peaks, straight_line.getLine(), inc, max_alt)
    
    print("Solution found for V2")
    et2 = time.time()
    ex_time2 = et2-st2
    maxv2 = pathv2.getMaxAlt()
    
    print("Max height of v2\t\t {}m".format(maxv2))
    print("Average height flown v2\t\t {}m".format(pathv2.getAverageAlt()))
    print("Distance flown v2\t\t {}km".format(pathv2.getTotalDistance()))
    print("Execution time v2: \t\t {}s".format(round(ex_time2, 2)))
except:
    pathv2 = Line(start, end)
    print("No solution found for V2")

# ---------------Method 2 - Circle Algorithm with Checkpoints--------------- #

print()

# ---------------Method 3 - Follow Edge--------------- #
st3 = time.time()
try:
    step_dist = 50
    straight_line = Line(start, end, step_dist)
    pathv3 = runFollowEdge(start, end, start_alt, straight_line, step_dist)

    print("Solution found for V3")
    et3 = time.time()

    ex_time3 = et3-st3
    maxv3 = pathv3.getMaxAlt()

    print("Max height of v3\t\t {}m".format(maxv3))
    print("Average height flown v3\t\t {}m".format(pathv3.getAverageAlt()))
    print("Distance flown v3\t\t {}km".format(pathv3.getTotalDistance()))
    print("Execution time v3: \t\t {}s".format(round(ex_time3, 2)))
except:
    pathv3 = Line(start, end)
    print("No solution found for V3")
# ---------------Method 3 - Follow Edge--------------- #



output = ''
for p in pathv3.getLine():
    output += str(p[0]) + ', ' + str(p[1]) + '\n'
write_to_clipboard(output)