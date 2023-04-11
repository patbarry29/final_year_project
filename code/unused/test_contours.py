from AreaMap import *
# from follow_edge import *

start = (54.317747, -5.930471) # to test algorithms on
end = (54.262201, -6.341939)

straight_line = Line(start, end)
max_alt = Altitude(start).getAltitude() + 120

# obstacles = getObstacles(straight_line.getLine(), max_alt)
# obs = obstacles[0]
# obs_shape = ContourMatrix(obs[0], obs[1], width, max_alt, step_dist)

step_dist = 50
width = 200
path = AreaMap(start, end, width, max_alt, step_dist)

alt_matrix = path.getMap()


point = 0
for line in alt_matrix:
    point = list(line)[width-1]
    point_alt = line[point]
    if  point_alt > max_alt:
        print(haversine(point, end))
        point2 = list(line)[width]
        print(haversine(point2, end))
        print()
        
