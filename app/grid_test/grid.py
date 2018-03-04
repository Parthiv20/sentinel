import os
import subprocess
import gdal
import numpy as np
import itertools
import json
import random

ds = gdal.Open('allbands.vrt')

x = ds.RasterXSize

y = ds.RasterYSize

print(x,y)

ds = None

x_arr = np.linspace(0, x, 5, endpoint=False).tolist()
y_arr = np.linspace(0, y, 5, endpoint=False).tolist()

print(x_arr)
print(y_arr)

xy_cartesian = list(itertools.product(x_arr, y_arr))

print(len(xy_cartesian))

# for i in xy_cartesian:
#     print(i)

x_step = x/5
y_step = y/5


cloud_pixels = 0


j=0
random.shuffle(xy_cartesian)
for i in xy_cartesian:
    print(i)
    j += 1
    print(j)
    
    print(i[0], i[1], x_step, y_step)
    
    subprocess.call(['gdal_translate', '-srcwin', str(i[0]), str(i[1]), str(x_step), str(y_step), 'allbands.vrt', 'rast'+str(j)+'.tif' ])
    subprocess.call(['fmask_sentinel2Stacked.py', '-a', 'rast'+str(j)+'.tif', '-z', 'angles.img', '-o', 'cloud'+str(j)+'.jpg'])
    subprocess.call(['rm', 'rast'+str(j)+'.tif'])
    img_info = json.loads(subprocess.check_output(['gdalinfo', "-json", 'cloud'+str(j)+'.jpg']).decode("utf-8"))
    grid_cloud_pixels = img_info["rat"]["row"][2]["f"][0]
    cloud_pixels += grid_cloud_pixels
    subprocess.call(['rm', 'cloud'+str(j)+'.jpg.aux.xml'])





img_info = json.loads(subprocess.check_output(['gdalinfo', "-json", "cloud.img"]).decode("utf-8"))
img_pixles = img_info["size"][0]*img_info["size"][1]
big_cloud_pixels = img_info["rat"]["row"][2]["f"][0]



print("grid imgae pixels and cloud cover percentage")
print(cloud_pixels)

cloud_percent = str((cloud_pixels/img_pixles)*100)
print(cloud_percent)


print("big image pixels and cloud cover percentage")
print(big_cloud_pixels)
cloud_percent = str((big_cloud_pixels/img_pixles)*100)
print(cloud_percent)
