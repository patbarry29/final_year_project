from circle_path_v1 import *
from circle_path_v2 import *
# from copy_coords import write_to_clipboard
from find_peaks import *
from follow_edge import *
from pathfinding import *
import time

'''
Compare all algorithms
'''

def pathSmoothing(path, fly_alt):
    i=0
    while i<path.getLength()-2:
        pt1 = path.getPoint(i)
        pt2 = path.getPoint(i+1)
        pt3 = path.getPoint(i+2)
        test_line = Line(pt1, pt3, 20)
        if test_line.getMaxAlt() < fly_alt:
            del path.getLine()[pt2]
        else:
            i += 1
    
    waypts = list(path.getLine().keys())
    path = Line(0, 0)
    for i in range(len(waypts)-1):
        line = Line(waypts[i], waypts[i+1])
        path.addLine(line)

    return path

def runRandom(start=(52.552282, -9.091245), end=(52.382904, -8.815093)):
    '''
        Runs each algorithm on a set of random start and end points
    '''
    # get 2 random points <= 'range' km away from each other
    # range_in_kms = 30
    # try:
    #     start, end = getTwoPoints(range_in_kms)
    # except:
    #     print('fail')
    #     start = (52.552282, -9.091245)
    #     end = (52.382904, -8.815093)
    # start = (52.552282, -9.091245)
    # end = (52.382904, -8.815093)
    
    straight_line = Line(start, end)
    start_alt = Altitude(start).getAltitude()
    
    fly_alt = start_alt + 80

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
    print()
    # ---------------PRINT SOME INFORMATION--------------- #


    # ---------------Method 1 - Circle Algorithm--------------- #
    inc = 1
    st1 = time.time()
    try:
        pathv1 = circleAlgV1(peaks, straight_line.getLine(), inc, max_alt)
        pathv1 = pathSmoothing(pathv1, fly_alt)
        print("Solution found for V1")
    except:
        pathv1 = Line(start, end)
        print("No solution found for V1")
    et1 = time.time()
    ex_time1 = round(et1-st1,2)
    maxv1 = pathv1.getMaxAlt()
    # ---------------Method 1 - Circle Algorithm--------------- #


    # ---------------Method 2 - Circle Algorithm with Waypoints--------------- #
    st2 = time.time()
    try:
        pathv2 = circleAlgV2(peaks, straight_line.getLine(), inc, max_alt)
        pathv2 = pathSmoothing(pathv2, fly_alt)
        print("Solution found for V2")
    except:
        pathv2 = Line(start, end)
        print("No solution found for V2")
    et2 = time.time()
    ex_time2 = round(et2-st2, 2)
    maxv2 = pathv2.getMaxAlt()
    # ---------------Method 2 - Circle Algorithm with Waypoints--------------- #

    
    # ---------------Method 3 - Follow Edge--------------- #
    st3 = time.time()
    try:
        step_dist = 100
        pathv3 = runFollowEdge(start, end, start_alt, straight_line, step_dist)
        pathv3 = pathSmoothing(pathv3, fly_alt)
        print("Solution found for V3")
    except:
        pathv3 = Line(start, end)
        print("No solution found for V3")
    et3 = time.time()
    ex_time3 = round(et3-st3, 2)
    maxv3 = pathv3.getMaxAlt()
    # ---------------Method 3 - Follow Edge--------------- #


    # ---------------Method 4 - Greedy--------------- #
    step_dist = 50
    width = 300
    graph = AreaMap(start, end, width, max_alt, step_dist)
    st4 = time.time()
    try:
        waypts = greedy(graph, start, end)
        pathv4 = cleanPath(waypts, fly_alt, start, end, True)
        print("Solution found for V4")
    except:
        pathv4 = Line(start, end)
        print("No solution found for V4")
    et4 = time.time()
    ex_time4 = round(et4-st4, 2)
    maxv4 = pathv4.getMaxAlt()
    # ---------------Method 4 - Greedy--------------- #


    # ---------------Method 5 - A*--------------- #
    st5 = time.time()
    pathv5 = 0
    if maxv4 <= max_alt+1:
        waypts = a_star(graph, fly_alt, start, end)
        pathv5 = cleanPath(waypts, fly_alt, start, end, True)
        print("Solution found for V5")
    else:
        pathv5 = Line(start, end)
        print("No solution found for V5")
    et5 = time.time()
    ex_time5 = round(et5-st5, 2)
    maxv5 = pathv5.getMaxAlt()
    # ---------------Method 5 - A*--------------- #

    # # ---------------Method 6 - Bisect Obstacles--------------- #
    # try:
    #     pathv6 = bisectObstacles(straight_line, max_alt, start,end)
    #     print("Solution found for V6")
    # except:
    #     pathv6 = Line(start, end)
    #     print("No solution found for V6")
    # # ---------------Method 6 - Bisect--------------- #


    # ---------------RETRIEVE RESULTS--------------- #
    print()

    paths = [straight_line,pathv1,pathv2,pathv3,pathv4,pathv5]

    avgs = []
    dists = []
    ratios = []
    energies = []
    for path in paths:
        avgs.append(path.getAverageAlt())
        dist = path.getTotalDistance()
        dists.append(dist)
        ratios.append(round(dist/dist_flown, 2))
        energies.append(path.getEnergyConsumption(fly_alt))

    exec_times = [0, ex_time1, ex_time2, ex_time3, ex_time4, ex_time5]
    maxs = [max_straight, maxv1, maxv2, maxv3, maxv4, maxv5]
    
    speed = 80 # km/h
    time_taken = []
    for dist in dists:
        t = dist/speed
        t = t*60
        time_taken.append(round(t, 2))

    # ---------------WRITE RESULTS TO FILE--------------- #
    # writeFile(dist_flown, ratios, energies, exec_times, time_taken)

    # ---------------PRINT RESULTS--------------- #
    print("\t\t\t", "Straight", "Circles\t", "Circles Waypts", "Follow Edge", "Greedy", "\tA*", "\tA*2", sep='\t')
    print("Execution time (s)", end='\t\t')
    for elem in exec_times:
        print(elem, end='\t\t')
    print()
    print()
    print("Distance flown (km)", end='\t\t')
    for elem in dists:
          print(elem, end='\t\t')
    print()
    print("Extra dist flown ratio", end='\t\t')
    for elem in ratios:
          print(elem, end='\t\t')
    print()
    print("Time taken (mins)", end='\t\t')
    for elem in time_taken:
          print(elem, end='\t\t')
    print()
    print()
    print("Number of turns\t", end='\t\t')
    for elem in energies:
          print(elem[3], end='\t\t')
    print()
    print("Avg angle of turn (°)", end='\t\t')
    for elem in energies:
          print(elem[6], end='\t\t')
    print()
    print()
    print("Max height (m)\t", end='\t\t')
    for elem in maxs:
          print(elem, end='\t\t')
    print()
    print("Average height (m)", end='\t\t')
    for elem in avgs:
          print(elem, end='\t\t')
    print()
    print("Max alt violation (m)", end='\t\t')
    for elem in energies:
          print(elem[7], end='\t\t')
    print()
    print("Metres spent ascending", end='\t\t')
    for elem in energies:
          print(elem[4], end='\t\t')
    print()
    print("Metres spent descending", end='\t\t')
    for elem in energies:
          print(elem[5], end='\t\t')
    print()
    print()
    print("Energy used (mAh)", end='\t\t')
    for elem in energies:
          print(elem[2], end='\t\t')
    print()

    return (start, end)


def writeFile(dist, ratios, energies, exec_times, time_taken):
    '''
        Write values to file.
    '''
    f = open('comp_table.txt', 'r')
    file_matrix = []
    i =0
    for line in f:
        line = line.strip().split(', ')
        if i == 0:
            line[0] = int(line[0])
            line[1] = float(line[1])
        elif i > 1:
            for i in range(1, len(line)):
                if line[i].isdigit():
                    line[i] = int(line[i])
                else:
                    line[i] = float(line[i])
        file_matrix.append(line)
        i += 1

    output = ''
    for i in range(len(file_matrix)):
        line = file_matrix[i]
        if i == 0:
            line[0] += 1
            line[1] += dist
        elif i>1:
            line[1] += energies[i-2][7]
            line[2] += exec_times[i-2]
            line[3] += ratios[i-2]
            line[4] += energies[i-2][3]
            line[5] += energies[i-2][6]
            line[6] += energies[i-2][4]
            line[7] += energies[i-2][5]
            line[8] += energies[i-2][2]
            line[9] += time_taken[i-2]
            line[3] = round(line[3], 2)
            line[8] = round(line[8], 2)
            line[8] = round(line[8], 2)

        file_matrix[i] = str(file_matrix[i]).replace('[', '')
        file_matrix[i] = str(file_matrix[i]).replace(']', '')
        file_matrix[i] = str(file_matrix[i]).replace('\'', '')
        output += file_matrix[i] + '\n'

    f.close()
    f = open('comp_table.txt', 'w')
    f.write(output)


def resetFile():
    '''
        Reset values in file.
    '''
    f = open('comp_table.txt', 'r')
    file_matrix = []
    i=0
    for line in f:
        line = line.strip().split(', ')
        file_matrix.append(line)
        i += 1

    output = ''
    for i in range(len(file_matrix)):
        line = file_matrix[i]
        if i == 0:
            line[0] = 0
            line[1] = 0
        elif i>1:
            for j in range(9):
                line[j+1] = 0

        file_matrix[i] = str(file_matrix[i]).replace('[', '')
        file_matrix[i] = str(file_matrix[i]).replace(']', '')
        file_matrix[i] = str(file_matrix[i]).replace('\'', '')
        output += file_matrix[i] + '\n'

    f.close()

    f = open('comp_table.txt', 'w')

    f.write(output)

def avgFile():
    '''
        Get average of values in file
    '''
    f = open('comp_table.txt', 'r')
    file_matrix = []
    i = 0
    for line in f:
        line = line.strip().split(', ')
        if i == 0:
            line[0] = int(line[0])
        elif i > 1:
            for i in range(1, len(line)):
                if line[i].isdigit():
                    line[i] = int(line[i])
                else:
                    line[i] = float(line[i])
        file_matrix.append(line)
        i += 1

    output = ''
    for i in range(len(file_matrix)):
        line = file_matrix[i]
        if i>1:
            for j in range(9):
                line[j+1] /= (int(file_matrix[0][0])*10)
                line[j+1] = round(line[j+1], 2)

        file_matrix[i] = str(file_matrix[i]).replace('[', '')
        file_matrix[i] = str(file_matrix[i]).replace(']', '')
        file_matrix[i] = str(file_matrix[i]).replace('\'', '')
        output += file_matrix[i] + '\n'

    f.close()
    f = open('comp_table.txt', 'w')
    f.write(output)


runRandom()

# points_list = [((54.927087, -6.530282), (54.855993, -6.425568)), ((52.911964, -9.023531), (53.170627, -8.943006)), ((51.989371, -9.403429), (51.896119, -9.461825)), ((54.40728, -7.096105), (54.559341, -6.911664)), ((54.404866, -6.972018), (54.538685, -7.170628)), ((51.73721, -8.827323), (51.908036, -8.603584)), ((53.897466, -9.405069), (53.886912, -8.998475)), ((54.928227, -7.816211), (55.038591, -7.892343)), ((51.950958, -9.715331), (52.161878, -9.526101)), ((53.553909, -9.26062), (53.446836, -9.640073)), ((54.060549, -6.464065), (54.246143, -6.690572)), ((52.741256, -8.033562), (52.537217, -8.011447)), ((52.697123, -6.3135), (52.844671, -6.515446)), ((54.951008, -6.802663), (54.884136, -7.13983)), ((52.317515, -8.577266), (52.274962, -8.294538)), ((53.940507, -7.010889), (53.96491, -7.446323)), ((52.486604, -9.231006), (52.337832, -8.935073)), ((54.182363, -5.937541), (54.440345, -5.95225)), ((54.949177, -6.839965), (54.869358, -6.692774)), ((52.199353, -9.403514), (52.393483, -9.176927)), ((51.816882, -9.529142), (52.000645, -9.334986)), ((54.98721, -8.189151), (55.007843, -8.134483)), ((55.002049, -7.282134), (54.947532, -7.561273)), ((54.528762, -7.052626), (54.711532, -7.306284)), ((52.875505, -7.16885), (52.969383, -7.141404))]
# for pt in points_list:
#     runRandom(pt[0], pt[1])


# resetFile()
# avgFile()