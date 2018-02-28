import os
import subprocess
import gdal
import numpy as np


ds = gdal.Open('allbands.vrt')

x = ds.RasterXSize

y = ds.RasterYSize

print(x,y)

ds = None

x_arr = np.linspace(0, x, 11).tolist()
y_arr = np.linspace(0, y, 11).tolist()

x_step = x_arr[1]
y_step = y_arr[1]

i=0
for a, b in zip(x_arr, y_arr):
    print(a, b)
    i += 1
    print(i)
    
    print(a, b, x_step, y_step)
    
    subprocess.call(['gdal_translate', '-srcwin', str(a), str(b), str(x_step), str(y_step), 'allbands.vrt', 'rast'+str(i)+'.tif' ])





