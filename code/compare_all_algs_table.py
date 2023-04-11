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
    st4 = time.time()
    try:
        step_dist = 50
        width = 300
        fly_alt = start_alt + 80
        graph = AreaMap(start, end, width, max_alt, step_dist)
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

    # ---------------RETRIEVE RESULTS--------------- #
    print()

    straight_avg = straight_line.getAverageAlt()
    avg_v1= pathv1.getAverageAlt()
    avg_v2= pathv2.getAverageAlt()
    avg_v3= pathv3.getAverageAlt()
    avg_v4= pathv4.getAverageAlt()
    avg_v5= pathv5.getAverageAlt()

    dist_v1 = pathv1.getTotalDistance()
    dist_v2 = pathv2.getTotalDistance()
    dist_v3 = pathv3.getTotalDistance()
    dist_v4 = pathv4.getTotalDistance()
    dist_v5 = pathv5.getTotalDistance()

    ratio_v1 = round(dist_v1/dist_flown, 2)
    ratio_v2 = round(dist_v2/dist_flown, 2)
    ratio_v3 = round(dist_v3/dist_flown, 2)
    ratio_v4 = round(dist_v4/dist_flown, 2)
    ratio_v5 = round(dist_v5/dist_flown, 2)
    ratios = [1,ratio_v1,ratio_v2,ratio_v3,ratio_v4,ratio_v5]

    energy_str = straight_line.getEnergyConsumption(fly_alt)
    energy1 = pathv1.getEnergyConsumption(fly_alt)
    energy2 = pathv2.getEnergyConsumption(fly_alt)
    energy3 = pathv3.getEnergyConsumption(fly_alt)
    energy4 = pathv4.getEnergyConsumption(fly_alt)
    energy5 = pathv5.getEnergyConsumption(fly_alt)
    energies = [energy_str,energy1,energy2,energy3,energy4,energy5]

    exec_times = [0, ex_time1, ex_time2, ex_time3, ex_time4, ex_time5]

    # ---------------WRITE RESULTS TO FILE--------------- #
    # writeFile(dist_flown, ratios, energies, exec_times)

    # ---------------PRINT RESULTS--------------- #
    print("\t\t\t", "Straight", "Circles\t", "Circles Waypts", "Follow Edge", "Greedy", "\tA*", sep='\t')
    print("Execution time (s)", 0, ex_time1, ex_time2, ex_time3, ex_time4, ex_time5, sep='\t\t')
    print()
    print("Distance flown (km)", dist_flown, dist_v1, dist_v2, dist_v3, dist_v4, dist_v5, sep='\t\t')
    print("Extra dist flown ratio", 1, ratio_v1, ratio_v2, ratio_v3, ratio_v4, ratio_v5, sep='\t\t')
    print()
    print("Number of turns\t", energy_str[3], energy1[3], energy2[3], energy3[3], energy4[3], energy5[3], sep='\t\t')
    print("Avg angle of turn (°)", energy_str[6], energy1[6], energy2[6], energy3[6], energy4[6], energy5[6], sep='\t\t')
    print()
    print("Max height (m)\t", max_straight, maxv1, maxv2, maxv3, maxv4, maxv5, sep='\t\t')
    print("Average height (m)", straight_avg, avg_v1, avg_v2, avg_v3, avg_v4, avg_v5, sep='\t\t')
    print("Max alt violation (m)", energy_str[7], energy1[7], energy2[7], energy3[7], energy4[7], energy5[7], sep='\t\t')
    print("Metres spent ascending", energy_str[4], energy1[4], energy2[4], energy3[4], energy4[4], energy5[4], sep='\t\t')
    print("Metres spent descending", energy_str[5], energy1[5], energy2[5], energy3[5], energy4[5], energy5[5], sep='\t\t')
    print()
    print("Energy used (mAh)", energy_str[2], energy1[2], energy2[2], energy3[2], energy4[2], energy5[2], sep='\t\t')


def writeFile(dist, ratios, energies, exec_times):
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
            line[3] = round(line[3], 2)
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
    i =0
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