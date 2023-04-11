from osgeo import gdal, osr
from pathlib import Path
import sys

"""
Here we transform the coordinates from lon/lat form to pixel 
coordinates (x/y values) which can be used to access a point in the file.

We store any files which have already been mapped in a python dict.
"""

class MapCoordinates:
    _files_opened = {}

    def __init__(self, fname):
        self._fname = "../ireland/" + fname
        self._ct = None
        self._fileinfo = []

        self.__checkFile()

    def getFileName(self):
        return self._fname
        
    def getFileInfo(self):
        return self._fileinfo
    
    def getCTransformation(self):
        return self._ct

    def __checkFile(self):
        if self._fname in self._files_opened:
            file = self._files_opened[self._fname]
            self._ct = file.getCTransformation()
            self._fileinfo = file.getFileInfo()
        else:
            self.__mapSpatialReference()
            self._files_opened[self._fname] = self

    def __mapSpatialReference(self):
        path = Path(self._fname)

        if path.is_file():
            src = gdal.Open(self._fname)
            gp = src.GetProjection()
            
            self._fileinfo.append(src.GetGeoTransform())
            self._fileinfo.extend([src.RasterXSize, src.RasterYSize])
            self._fileinfo.append(src.ReadAsArray())

            # this is the files srs
            file_sr = osr.SpatialReference()
            file_sr.ImportFromWkt(gp)

            # this is the target srs we want to map from
            geo_sr = osr.SpatialReference()
            geo_sr.ImportFromEPSG(4326)

            # this line ensures the axes match the format required
            # e.g. EPSG4326 (WGS84) uses lat as x axis and lon as y
            # returns (2, -1, 3) 
            #   -> 2 means first axis of CRS maps to second of our data
            #   -> -1 second axis of CRS maps to first axis, with values negated
            #   -> 3 means third axis of CRS to thrid axis
            # this will store that information for the projection
            geo_sr.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

            self._ct = osr.CoordinateTransformation(geo_sr, file_sr)
        
        else:
            sys.exit("No solution found")