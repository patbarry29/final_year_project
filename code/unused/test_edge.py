from follow_edge import *
from copy_coords import *
import time

def runFollowEdge(start, end, start_alt, straight_line, step_dist): 
    # st = time.time()
    max_alt = 120
    i = 1
    # print()
    # print("On path {} at {} metres".format(i, start_alt+120))
    # print("Maximum altitude of the UAV: {}m".format(start_alt+max_alt))
    path = getPath(start, end, start_alt+max_alt, straight_line, step_dist)
    max_alt -= 60

    paths = {path: path.getMaxAlt()}
    try:
        while path.getMaxAlt() > start_alt+120 and max_alt >= 0:
            # print("Path maximum is ", path.getMaxAlt())
            # i+=1
            # print("On path {} at {} metres".format(i, start_alt+max_alt))
            path = getPath(start, end, start_alt+max_alt, straight_line, step_dist)
            max_alt -= 60
            paths[path] = path.getMaxAlt()
    except:
        print("Algorithm interrupted")
    
    # paths[path] = path.getMaxAlt()
    # print()
    # print()
    # print("Maximum:\t", start_alt+120)
    # print("Straight:\t", straight_line.getMaxAlt())
    min_path = min(paths.items(), key=lambda x: x[1])
    path = min_path[0]
    min_path = min(paths.items(), key=lambda x: x[1])
    path = min_path[0]

    return path
    # et = time.time()

    # print(et-st)


def getPath(start, end, max_alt, line, step_dist):
    edge_path = followEdge(start, end, line, max_alt, step_dist)

    return edge_path


if __name__ == '__main__':
    range_in_kms = 20
    step_dist = 50
    # try:
    #     start, end = getTwoPoints(range_in_kms)
    # except:
    #     print('NOT RANDOM\n\n')
    #     start= (52.652448, -7.446219) # NOT WORK
    #     end= (52.65948, -8.545809)
    # # start= (52.429367, -9.317902) # NOT WORK
    # # end= (52.296735, -9.136351)
    # # start= (53.600975, -9.901837) # NOT WORK, VERY HARD
    # # end= (53.703304, -9.653155)
    # # start= (55.066292, -8.152927) # NOT WORK
    # # end= (54.983136, -8.027814)
    # # start= (54.28975, -7.980695) # NOT WORK
    # # end= (54.257052, -7.806686)
    # # start= (53.569554, -9.490858) # NOT WORK
    # # end= (53.594508, -9.705984)
    # # start= (53.539344, -9.678252) # NOT WORK
    # # end= (53.400684, -10.042603)
    # # start= (52.380765, -8.32299) # NOT WORK
    # # end= (52.301254, -8.118864)

    # # start= (55.043063, -6.77983) # WORKS
    # # end= (55.000384, -7.004581)
    # # start= (52.731114, -7.608729)# WORKS
    # # end= (52.73384, -7.405407)
    # # start= (54.287751, -7.594472) # WORKS
    # # end= (54.391446, -7.457022)
    # # start= (52.8838411, -8.5146466) # WORKS
    # # end= (53.0204914, -8.4933211)
    # # start= (51.9078787, -8.9924612) # WORK
    # # end= (51.768131, -8.9780161)
    # # start= (52.180058, -7.99371) # WORKS
    # # end= (52.325791, -7.999908)


    # print("start=", start)
    # print("end=", end)

    # start_alt = Altitude(start).getAltitude()
    # max_alt = 120

    # straight_line = Line(start, end, step_dist)

    # runFollowEdge(start, end, start_alt, straight_line, step_dist)


    # print()
    # print("drone max\t",max_alt)

    # print("Straight max\t",straight_line.getMaxAlt())

    # print("edge max\t",max_alt)