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

def runRandom():
    '''
        Runs each algorithm on a set of random start and end points
    '''
    # get 2 random points <= 'range' km away from each other
    range_in_kms = 30
    try:
        start, end = getTwoPoints(range_in_kms)
    except:
        print('fail')
        start = (52.552282, -9.091245)
        end = (52.382904, -8.815093)
    
    straight_line = Line(start, end)
    start_alt = Altitude(start).getAltitude()

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
    fly_alt = start_alt + 80
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
    
    speed = 80 # km/h
    time_taken = []
    for dist in dists:
        t = dist/speed
        t = t*60
        time_taken.append(round(t, 2))

    # ---------------WRITE RESULTS TO FILE--------------- #
    # writeFile(dist_flown, ratios, energies, exec_times, time_taken)

    # ---------------PRINT RESULTS--------------- #
    print("\t\t\t", "Straight", "Circles\t", "Circles Waypts", "Follow Edge", "Greedy", "\tA*", sep='\t')
    print("Execution time (s)", 0, ex_time1, ex_time2, ex_time3, ex_time4, ex_time5, sep='\t\t')
    print()
    print("Distance flown (km)", dists[0], dists[1], dists[2], dists[3], dists[4], dists[5], sep='\t\t')
    print("Extra dist flown ratio", ratios[0], ratios[1], ratios[2], ratios[3], ratios[4], ratios[5], sep='\t\t')
    print("Time taken (mins)", time_taken[0], time_taken[1], time_taken[2], time_taken[3], time_taken[4], time_taken[5], sep='\t\t')
    print()
    print("Number of turns\t", energies[0][3], energies[1][3], energies[2][3], energies[3][3], energies[4][3], energies[5][3], sep='\t\t')
    print("Avg angle of turn (°)", energies[0][6], energies[1][6], energies[2][6], energies[3][6], energies[4][6], energies[5][6], sep='\t\t')
    print()
    print("Max height (m)\t", max_straight, maxv1, maxv2, maxv3, maxv4, maxv5, sep='\t\t')
    print("Average height (m)", avgs[0], avgs[1], avgs[2], avgs[3], avgs[4], avgs[5], sep='\t\t')
    print("Max alt violation (m)", energies[0][7], energies[1][7], energies[2][7], energies[3][7], energies[4][7], energies[5][7], sep='\t\t')
    print("Metres spent ascending", energies[0][4], energies[1][4], energies[2][4], energies[3][4], energies[4][4], energies[5][4], sep='\t\t')
    print("Metres spent descending", energies[0][5], energies[1][5], energies[2][5], energies[3][5], energies[4][5], energies[5][5], sep='\t\t')
    print()
    print("Energy used (mAh)", energies[0][2], energies[1][2], energies[2][2], energies[3][2], energies[4][2], energies[5][2], sep='\t\t')


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
            for j in range(8):
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
            for j in range(8):
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

# for i in range(10):
#     runRandom()

# resetFile()
# avgFile()