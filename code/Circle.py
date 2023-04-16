from Altitude import *
from math import cos, sin, radians, degrees

'''
Draw circles around centre
'''

class Circle:
    def __init__(self, centre):
        self._centre = centre

    def getCircle(self, radius, inc=10, angle=0):
        '''
            Return a circle dict with:
                key=centre, val=list of points on the circle
        '''
        half1 = {}
        half2 = {}
        max_angle = 180+angle
        while angle != max_angle:
            # calculate 2 point coords, one going in one direction around
            # the circle, the other in the other direction
            pt1 = self.__calcCoords(radius, angle)
            pt2 = self.__calcCoords(radius, 180+angle)
            # store in dict
            half1[pt1] = Altitude(pt1).getAltitude()
            half2[pt2] = Altitude(pt2).getAltitude()
            angle += inc
        
        return half1, half2

    def __calcCoords(self, r, a):
        # must convert the angle from degrees to radians
        a = radians(a)
        # formula to calculate the coords of any point on a circle
        # given centre, radius, and angle
        x = self._centre[0] + (r * cos(a))
        y = self._centre[1] + (r * sin(a))
        return (x,y)
    
    def drawCircles(self, dict, inc=10):
        '''
        Draw circles with 360/inc points.
        '''
        c = {}
        for peak, radius in dict.items():
            h1,h2 = self.getCircle(radius, inc)

            c[peak] = h1
            c[peak].update(h2)

        return c
