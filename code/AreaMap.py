from Line import *

'''
Class to retrieve grid of surrounding area for use in greedy and A* algorithms.
'''

class AreaMap:
    def __init__(self, start, end, width, max_alt, step_dist=100):
        self._start = start
        self._end = end
        self._width = width
        self._max_alt = max_alt
        self._step_dist = step_dist
        self._line = Line(self._start, self._end, self._step_dist)

        self._left_side = self.buildSide(left=True)
        self._right_side = self.buildSide(left=False)
        self._matrix = self.buildMatrix()
        # if width < 30:
        #     self._obs_map = self.buildObsMap()

    def getStepDist(self):
        return self._step_dist
    
    def getStart(self):
        return self._start
    
    def getWidth(self):
        return len(self._matrix[0])
    
    def getMaxAlt(self):
        return self._line.getMaxAlt()
    
    def getMaxAltDrone(self):
        return self._max_alt
    
    def getObsMap(self):
        return self._obs_map

    def getSide(self, left):
        if left:
            return self._left_side
        else:
            return self._right_side
        
    def getDist2Points(self, p1, p2):
        dist = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
        return dist

    def getIndex(self, point):
        i1 = 0
        i2 = 0
        for line in self._matrix:
            if point in line:
                i1 = self._matrix.index(line)
                i2 = list(line).index(point)
        return i1, i2
    
    def getPoint(self, i1, i2):
        line = self._matrix[i1]
        items = line.items()
        point = list(items)[i2]
        return point
    
    def getMap(self):
        return self._matrix
    
    
    def buildSide(self, left):
        '''
            Retrieve grid to one side of the central line.
        '''
        side = []
        x_slope, y_slope = self._line.getSlopes()
        for point in self._line.getLine():
            side.append(self.drawPerpLine(point, left, x_slope, y_slope))
        return side

    def buildMatrix(self):
        '''
            Join the 2 grids, left and right, and combine into 1.
        '''
        matrix = []
        for i in range(len(self._left_side)):
            r = self._right_side[i]
            r = dict(reversed(r.items()))
            l = self._left_side[i]
            r.update(l)
            matrix.append(r)
        return matrix
    
    def drawPerpLine(self, point, left, x_slope, y_slope):
        '''
            Draw a line perpendicular to the given slopes:
                x_slope and y_slope
        '''
        lat = point[0]
        lon = point[1]
        perp_line = {}
        
        if left:
            y_slope = -1 * y_slope
        else:
            x_slope = -1 * x_slope
        
        for i in range(self._width):
            if i==0 and left:
                perp_line = {}
            else:
                perp_line[(lat,lon)] = Altitude((lat, lon)).getAltitude()
            
            lat += (y_slope)
            lon += (x_slope)
        
        return perp_line
    

    def buildObsMap(self):
        '''
            Alternative method to store graph for A*.
            Build a map of all the obstacles, and then create adjacency 
            list for each point, inc. start and end points.
        '''
        obstacle_map = {self._start:[], self._end:[]}
        for line in self._matrix:
            for point, val in line.items():
                if val == 'obs':
                    obs = []
                    obs_i1, obs_i2 = self.getIndex(point)
                    obs.append(self.getPoint(max(0, obs_i1-1), obs_i2))
                    obs.append(self.getPoint(obs_i1, max(0, obs_i2-1)))
                    if obs_i1 < len(self._matrix)-1:
                        obs.append(self.getPoint(obs_i1+1, obs_i2))
                    if obs_i2 < self._width-1:
                        obs.append(self.getPoint(obs_i1, obs_i2+1))
                    
                    i = 0
                    while i < len(obstacle_map):
                        p1 = list(obstacle_map.keys())[i]
                        adj_list = list(obstacle_map.values())[i]
                        for p2 in obs:
                            if p2[1] != 'obs':
                                obstacle_map[p2[0]] = []
                                obs_on_path = Line(p1, p2[0], 20).getMaxAlt()
                                if p2[0] in adj_list:
                                    obstacle_map[p2[0]].append(p1)
                                elif obs_on_path < self._max_alt:
                                    obstacle_map[p2[0]].append(p1)
                                    adj_list.append(p2[0])
                        i += 1
        return obstacle_map