import haversine as hs
from Altitude import *
from energy_consumption import *

class Line:
    def __init__(self, start, end, step=100):
        self._start = start
        self._end = end
        self._step = step
        if start == end:
            # if start and end point are the same, only store start point
            if start != 0:
                alt1 = Altitude(start).getAltitude()
                self._alt_dict = {start: alt1}
            else:
                self._alt_dict = {}
            return
        
        # measure dist from start to end
        dist = self.measureDistance(start, end)
        step_dist = self.calcStepDistance(dist, step)
        self._inc_lat, self._inc_lon = self.extraCalcs(start, end, step_dist)
        # retrieve a dict storing (pt_coords: alt) 
        self._alt_dict = self.getAltitudes(start, end, self._inc_lat, self._inc_lon)


    def measureDistance(self, start, end):
        distance = hs.haversine(start, end)
        return distance

    def calcStepDistance(self, dist, step):
        # define how many kilometres to travel before measuring
        step = step/1000
        # we will measure the altitude (distance/step) times
        return dist / step


    def extraCalcs(self, start, end, step_dist):
        # we will then subtract start latitude from end latitude
        # and repeat for longitude to get distance
        lat_dist = start[0] - end[0]
        lon_dist = start[1] - end[1]

        # then divide by number of steps to calculate the number to be
        # added to each
        inc_lat = lat_dist / step_dist
        inc_lon = lon_dist / step_dist

        return inc_lat, inc_lon


    def getAltitudes(self, start, end, inc_lat, inc_lon):
        lat, lon = start[0], start[1]

        # now start a loop to find altitude at each step from start to end
        alt_dict = {}
        if lat < end[0]:
            while lat < end[0]:
                alt = Altitude((lat, lon))
                alt_dict[lat, lon] = alt.getAltitude()
                lat -= inc_lat
                lon -= inc_lon
        else:
            while lat > end[0]:
                alt = Altitude((lat, lon))
                alt_dict[lat, lon] = alt.getAltitude()
                lat -= inc_lat
                lon -= inc_lon

        alt = Altitude(end)
        alt_dict[end] = alt.getAltitude()
        return alt_dict


    def getLine(self):
        return self._alt_dict
    
    def getLength(self):
        return len(self._alt_dict)
    
    def getMaxAlt(self):
        # max alt on the line
        return max(list(self._alt_dict.values()))
    
    def getMaxAltDrone(self):
        return Altitude(self.getPoint(0)).getAltitude() + 120
    
    def getPoint(self, index):
        # returns ith point, i=index
        return list(self._alt_dict)[index]
    
    def getIndex(self, point):
        return list(self._alt_dict).index(point)
    
    # def getDistToLine(self, pt):
    #     '''
    #         used in bisect algorithm as a heuristic
    #     '''
    #     min_dist = 100
    #     for pt2 in self._alt_dict:
    #         dist = haversine(pt, pt2)
    #         min_dist = min(min_dist, dist)
    #     return min_dist
    
    def getSlopes(self):
        return self._inc_lat, self._inc_lon
    
    def getTotalDistance(self):
        # return distance from start to end measuring between each waypoint
        dist = 0
        for i in range(self.getLength()-1):
            dist += hs.haversine(self.getPoint(i), self.getPoint(i+1))
        return round(dist, 2)
    
    def getEnergyConsumption(self, fly_alt):
        '''
            returns energy consumption with factors including 
                height, turning angle and distance
        '''
        num_of_turns = -1
        total_ang = 0
        asc = 0
        desc = 0
        max_alt = self.getMaxAltDrone()
        energy_MJ, energy_kWh, energy_mAh = 0,0,0
        for i in range(len(self._alt_dict)-2):
            pt1 = self.getPoint(i)
            pt2 = self.getPoint(i+1)
            pt3 = self.getPoint(i+2)
            e_mj, e_kwh, e_mah = getEnergy(pt1, pt2)
            
            # check if a turn has been made
            ang = angle3pts(pt1, pt2, pt3)
            factor = 1
            if not math.isclose(ang,0):
                num_of_turns += 1
                total_ang += ang
                # range of factor = (1,50)
                # range of ang = (1,180)
                factor += ((ang**0.75)/100)
                # if ang < 2:
                #     factor += 0.3
            e_mj *= factor
            e_kwh *= factor
            e_mah *= factor

            # check if flying altitude breached
            pt1_alt = Altitude(pt1).getAltitude()
            pt2_alt = Altitude(pt2).getAltitude()
            factor = 1
            if pt2_alt > fly_alt:
                if pt2_alt > pt1_alt:
                    m_asc = pt2_alt-pt1_alt
                    asc += m_asc
                    factor += (0.3*m_asc) # 30% more power for ascent
                elif pt2_alt < pt1_alt:
                    desc += pt1_alt-pt2_alt
                    factor += 0.15 # 15% more for descent
            e_mj *= factor
            e_kwh *= factor
            e_mah *= factor

            # update total
            energy_MJ += e_mj
            energy_kWh += e_kwh
            energy_mAh += e_mah

        above_max = self.getMaxAlt()-max_alt
        if above_max > 0:
            above_max = 1
            energy_mAh *= 2
            
        avg_ang = total_ang
        if num_of_turns > 0:
            avg_ang = round(total_ang/num_of_turns, 1)
        
        return (energy_MJ, 
                round(energy_kWh, 1), 
                round(energy_mAh, 1), 
                num_of_turns, 
                asc+fly_alt, desc+fly_alt, 
                round(avg_ang, 2),
                max(0, above_max))
    
    def adjustAlts(self):
        # for use in plotting paths with contour maps
        fly_alt = self.getMaxAltDrone()-40
        for key, val in self._alt_dict.items():
            if val < fly_alt:
                self._alt_dict[key] = fly_alt
    
    def getAverageAlt(self):
        s = sum(self._alt_dict.values())
        avg = s / self.getLength()
        return round(avg,2)

    def addLine(self, line):
        # add one line to curent line
        self._alt_dict.update(line.getLine())
