import numpy as np
from osgeo import gdal
from osgeo.gdalconst import *
from osgeo import gdal_array
import os

# you can find the GDAL library here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

ROOT_DIR = r'C:\Users\'
raster_path = 'dem.tif'

# open raster
raster = gdal.Open(os.path.join(ROOT_DIR, raster_path), GA_ReadOnly)

print type(raster)

# access raster attributes
gt = raster.GetGeoTransform()
attributes = {'origin: ': (gt[0], gt[3]),
              'cell_size': gt[1],
              'shape': (raster.RasterXSize, raster.RasterYSize),
              'driver': raster.GetDriver().LongName
              }

print attributes
# convert raster object to numpy array
array = gdal_array.DatasetReadAsArray(raster)

def get_raster_values(array):
    """
    # get unique values and counts for categorical raster
    :param array:
    :return: value_count_dict
    """
    unique = np.unique(array, return_counts=True)
    value_count_dict = dict(zip(unique[0], unique[1]))
    return value_count_dict
