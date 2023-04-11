from find_peaks import *
from crow_flies_v2 import *
from Circle import *

# get altitudes from start to end
# start = (51.65550157494285, -9.461801748197177)
start = (51.838353847600885, -10.156763362936477)
end = (53.37731900994556, -6.234298920712984)
straight_line = getStraightLine(start, end)

# find all points above max altitude
max_alt = 400
peaks = findPeaks(straight_line, max_alt)

# draw circles
circles = [[],[]]
empty_vals = []
for peak, radius in peaks.items():
    if radius > 0:
        c = Circle(peak, straight_line)
        h0,h1 = c.getCircle(radius)

        circles[0].append(h0)
        circles[1].append(h1)
    else:
        empty_vals.append(peak)

for key in empty_vals:
    del peaks[key]




def recursive(point1, point2, i, circle, point_num, circle_num, leniency=0, half2=False):
    # if circle_num>1:
    #     print(circle_num)
    line = getStraightLine(point1, point2)
    max_alt_on_line = max(list(line.values()))

    # if line is below max altitude, save and move to next peak
    if max_alt_on_line < max_alt+leniency:
        new_checkpoints[point_num] = point2
        print(circle_num)
        if circle_num<len(peaks)-1:
            to_remove = list(circle)[:i+1]
            for key in to_remove:
                del circle[key]

            next_circle = circles_copy[0][circle_num+1]
            recursive(point2, new_checkpoints[point_num+1], 0, next_circle, point_num+1, circle_num+1, leniency)
        else:
            print('here now ')
        #     recursive(end, point2, 0, circle, point_num+1, circle_num, leniency)


    else:
        # else, try next point in circle
        if i<len(circle)-1:
            recursive(point1, list(circle)[i+1], i+1, circle, point_num, circle_num, leniency, half2=half2)

        # else, try next half of circle
        elif i==len(circle)-1 and not half2:
            i = 0
            circle = circles_copy[1][circle_num]
            recursive(point1, list(circle)[i+1], i+1, circle, point_num, circle_num, leniency, half2=True)

        # else, go back to previous circle
        elif circle_num>0:
            p1 = new_checkpoints[point_num-2]
            # restore circle to original state before going back
            # print(len(circles_copy[0][circle_num]), len(circles[0][circle_num]))
            # circles_copy[0][circle_num] = circles[0][circle_num]
            # circles_copy[1][circle_num] = circles[1][circle_num]
            # print(len(circles_copy[0][circle_num]))
            
            try:
                prev_circle = circles_copy[0][circle_num-1]
                recursive(p1, list(prev_circle)[0], 0, prev_circle, point_num-1, circle_num-1, leniency)
            except IndexError:
                print(new_checkpoints)



if len(peaks) > 0:
    new_checkpoints = [start] + [0]*len(peaks) + [end]
    for c in circles[0]:
        i = circles[0].index(c)
        new_checkpoints[i+1] = list(c)[0]

    circles_copy = [[],[]]
    for h in range(2):
        for c in range(len((circles[h]))):
            circles_copy[h].append(circles[h][c])
    circle = circles_copy[0][0]
    
    recursive(start, list(circle)[0], 0, circle, point_num=1, circle_num=0, leniency=10)

    # print(list(peaks.keys())[1], half1_list[1])
    print(new_checkpoints)


    for i in range(len(new_checkpoints)-1):
        line = getStraightLine(new_checkpoints[i], new_checkpoints[i+1])
        print(max(list(line.values())), new_checkpoints[i],new_checkpoints[i+1])