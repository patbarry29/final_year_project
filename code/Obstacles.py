from Altitude import *

class Obstacles:
    def __init__(self, line, max_alt):
        self._line = line
        self._max_alt = max_alt

    def getObstacles(self):
        '''
        Assess line and return all obstacles on path, storing 
            [start,halfway,end] for each obstacle
        '''
        i = 0
        obstacles = []
        too_high = []
        for pt, altitude in self._line.getLine().items():
            point_index = self._line.getIndex(pt)
            if altitude >= self._max_alt and point_index != self._line.getLength()-1:
                if len(too_high) == 0 and point_index > 0:
                    # add start of obstacle
                    too_high.append(self._line.getPoint(point_index-1))
                # add pt within obstacle
                too_high.append(pt)
            
            elif len(too_high) > 0:
                if point_index < self._line.getLength()-2:
                    # add end of obstacle
                    too_high.append(self._line.getPoint(point_index+1))
                obstacles.append([])
                halfway = int((len(too_high)-1)/2)
                obstacles[i] = [too_high[0], too_high[halfway], too_high[-1]]
                i += 1
                too_high = []

        return obstacles