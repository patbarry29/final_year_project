from MapCoordinates import *
import sys

'''
Retrieve altitude of given point
'''

class Altitude:
    def __init__(self, coords):
        self._fname = "ALPSMLC30_N051W011_DSM.tif"
        self._coords = coords
        self._altitude = None
        self._src = MapCoordinates(self._fname)

        self.__mapCoords()

    def getCoords(self):
        return self._coords

    def getAltitude(self):
        return self._altitude

    def getFileName(self):
        return self._fname

    def __mapCoords(self):
        # create variables
        ct = self._src.getCTransformation()
        fileinfo = self._src.getFileInfo()
        gt = fileinfo[0]
        width, height = fileinfo[1], fileinfo[2]
        ds = fileinfo[3] # dataset with info for each coord

        # map_x will store the required x axis for projection
        # map_y does the same
        # in our case, it switches lat to map_y and vice versa
        map_x, map_y, z = ct.TransformPoint(self._coords[0], self._coords[1])

        # now we must invert the transformation so it goes 
        # lon/lat coords -> pixel coords
        gt_inv = gdal.InvGeoTransform(gt)
        pixel_x, pixel_y = gdal.ApplyGeoTransform(gt_inv, map_x, map_y)

        pixel_x, pixel_y = round(pixel_x), round(pixel_y)

        if pixel_x in range(0, width) and pixel_y in range(0, height):
            self._altitude = ds[pixel_y, pixel_x]
        else:
            # x and y indicate if the coordinates are left/right or 
            #   up/down of the current file
            x = 0
            y = 0
            if pixel_x < 0:
                x = 1
            elif pixel_x >= width:
                x = -1
            if pixel_y < 0:
                y = 1
            elif pixel_y >= height:
                y = -1
            self.__findNextFile(x, y)


    def __findNextFile(self, x, y):
        '''
            Function to find the file where the coordinates are located.
            
            Files are named like this:
            "ALPSMLC30_N0" + latitude value + "W0" + longitude value+ "_DSM.tif"
            
            So to find the correct file, we just need to add/subtract 1 to the 
            lat/lon values until we locate the coordinates.
        '''
        prefix = self._fname[:12]
        num1 = self._fname[12:14]
        midfix = self._fname[14:16]
        num2 = self._fname[16:18]
        suffix = self._fname[18:]
        
        num2 = str(int(num2) + x)
        num1 = str(int(num1) + y)

        if len(num1) < 2:
            num1 = "0" + num1
        if len(num2) < 2:
            num2 = "0" + num2
        
        self._fname = prefix + num1 + midfix + num2 + suffix
        try:
            self._src = MapCoordinates(self._fname)
            self.__mapCoords()
        except:
            # sys.exit("No solution found")
            return