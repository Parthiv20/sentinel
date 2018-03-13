# from app import app


import subprocess
import json
import os
import xml.etree.ElementTree as etree
import random
import time
import copy
import itertools
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats

from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from flask import Flask, request, render_template, session, flash, redirect, url_for, jsonify
from celery import Celery
from flask import session
from subprocess import Popen, PIPE, CalledProcessError
from geojson import Polygon


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'


# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(bind=True)
def long_task(self):

    with open("in_dict.txt") as f:
        in_dict = json.load(f)

    in_bbox ='{"type": "Polygon", "coordinates":'+str(in_dict['bbox'])+'}'

    sensor = in_dict['satellite']

    self.update_state(state="PROGRESS", meta={"extent": in_bbox, "type": "vector" })

    gdalbuildvrt = subprocess.check_output(["which", "gdalbuildvrt"])[:-1].decode("utf-8")

    gdal_translate = subprocess.check_output(["which", "gdal_translate"])[:-1].decode("utf-8")

    gdalinfo = subprocess.check_output(["which", "gdalinfo"])[:-1].decode("utf-8")

    data_path = "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data"

    f = open("sp_subset.txt", "r")
    sp_subset = f.readlines()


    # This we use in final result image
    image_dates = []
    cloud_percent = []


    for img in sp_subset:        

        date = img[11:15]+"-"+img[15:17]+"-"+img[17:19]
        
        image_dates.append(date)
        
        img_xml_tree = etree.parse(data_path+os.path.sep+sensor+os.path.sep+img[:-1]+os.path.sep+"MTD_MSIL1C.xml")
        img_xml_root = img_xml_tree.getroot()

        band_list = img_xml_root[0][0][11][0][0]

        band_path = data_path+os.path.sep+sensor+os.path.sep+img[:-1]+os.path.sep


        sun_angle_path = (band_list[0].text).rsplit(os.path.sep, 2)[0]

        subprocess.call([gdalbuildvrt, "-resolution", "user", "-tr", "60", "60", "-separate", img[:-6]+"_allbands.vrt", band_path+band_list[0].text+".jp2", band_path+band_list[1].text+".jp2", band_path+band_list[2].text+".jp2", band_path+band_list[3].text+".jp2", band_path+band_list[4].text+".jp2", band_path+band_list[5].text+".jp2", band_path+band_list[6].text+".jp2", band_path+band_list[7].text+".jp2", band_path+band_list[8].text+".jp2", band_path+band_list[9].text+".jp2", band_path+band_list[10].text+".jp2", band_path+band_list[11].text+".jp2", band_path+band_list[12].text+".jp2"])

        subprocess.call(["fmask_sentinel2makeAnglesImage.py", "-i", band_path+sun_angle_path+os.path.sep+"MTD_TL.xml", "-o", img[:-6]+"_angles.img"])


        subprocess.call([gdalbuildvrt, "-resolution", "user", "-tr", "60", "60", "-separate", img[:-6]+"_rgb.vrt", band_path+band_list[1].text+".jp2", band_path+band_list[2].text+".jp2", band_path+band_list[3].text+".jp2"])

        subprocess.call([gdal_translate, "-of", "JPEG", "-ot", "Byte", "-scale", img[:-6]+"_rgb.vrt", img[:-6]+"_rgb.jpg"])

        img_info = json.loads(subprocess.check_output([gdalinfo, "-json", img[:-6]+"_rgb.vrt"]).decode("utf-8"))

        img_size = img_info['size']

        # # creating projection
        img_srs = osr.SpatialReference()
        img_srs.ImportFromEPSG(4326)

        out_srs = osr.SpatialReference()
        out_srs.ImportFromEPSG(int(in_dict["srs"].rsplit(":")[1]))

        transform = osr.CoordinateTransformation(img_srs, out_srs)  
        
        # getting image extent and transforming to 3857
        grid_extent = img_info['wgs84Extent']['coordinates'][0]
        grid_extent_x = [item[0] for item in grid_extent]
        grid_extent_y = [item[1] for item in grid_extent]
        grid_x_min = min(grid_extent_x)
        grid_y_min = min(grid_extent_y)
        grid_x_max = max(grid_extent_x)
        grid_y_max = max(grid_extent_y)
        
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(grid_x_min, grid_y_min)
        point.Transform(transform)
        grid_x_min = point.GetX()
        grid_y_min = point.GetY()
        point.AddPoint(grid_x_max, grid_y_max)
        point.Transform(transform)
        grid_x_max = point.GetX()
        grid_y_max = point.GetY()
        grid_extent = [grid_x_min, grid_y_min, grid_x_max, grid_y_max]

        self.update_state(state='PROGRESS', meta={'type': 'raster', 'extent': grid_extent, 'name':img[:-6]+'_rgb.jpg', 'image_size': img_size })
        
        # small grid processing

        ds = gdal.Open(img[:-6]+"_allbands.vrt")

        x = ds.RasterXSize
        y = ds.RasterYSize

        # used to calculate cloud percent
        img_pixels = x*y

        ds = None

        # # TODO:update here for user specified grid size
        x_arr = np.linspace(0, x, 3, endpoint=False).tolist()
        y_arr = np.linspace(0, y, 3, endpoint=False).tolist()

        xy_cartesian = list(itertools.product(x_arr, y_arr))

        # # TODO:update here for user specified grid size
        x_step = x/3
        y_step = y/3

        cloud_pixels = 0
        j=0
        # to process grids randomly
        random.shuffle(xy_cartesian)

        for i in xy_cartesian:
            j += 1
            subprocess.call([gdal_translate, "-srcwin", str(i[0]), str(i[1]), str(x_step), str(y_step), img[:-6]+"_allbands.vrt", img[:-6]+"_rast"+str(j)+".tif" ])
            subprocess.call(["fmask_sentinel2Stacked.py", "-a", img[:-6]+"_rast"+str(j)+".tif", "-z", img[:-6]+"_angles.img", "-o", img[:-6]+"_cloud"+str(j)+".img"])
            
            subprocess.call([gdal_translate, "-of", "JPEG", "-ot", "Byte", "-expand", "rgb", "-scale", img[:-6]+"_cloud"+str(j)+".img", img[:-6]+"_cloud"+str(j)+".jpg"])
            
            img_info = json.loads(subprocess.check_output([gdalinfo, "-json", img[:-6]+"_cloud"+str(j)+".img"]).decode("utf-8"))
            
            grid_size = img_info['size']
            
            grid_cloud_pixels = img_info["rat"]["row"][2]["f"][0]
            grid_extent = img_info['wgs84Extent']['coordinates'][0]
            grid_extent_x = [item[0] for item in grid_extent]
            grid_extent_y = [item[1] for item in grid_extent]
            grid_x_min = min(grid_extent_x)
            grid_y_min = min(grid_extent_y)
            grid_x_max = max(grid_extent_x)
            grid_y_max = max(grid_extent_y)
            
            # trasnforming extent to EPSG:3857 transfrom is coming from above
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(grid_x_min, grid_y_min)
            point.Transform(transform)
            grid_x_min = point.GetX()
            grid_y_min = point.GetY()
            point.AddPoint(grid_x_max, grid_y_max)
            point.Transform(transform)
            grid_x_max = point.GetX()
            grid_y_max = point.GetY()
            grid_extent = [grid_x_min, grid_y_min, grid_x_max, grid_y_max]
            cloud_pixels += grid_cloud_pixels
            
            self.update_state(state='PROGRESS', meta={'type': 'raster', 'extent':grid_extent, 'name': img[:-6]+"_cloud"+str(j)+'.jpg', 'image_size': grid_size })
        
        img_cloud_percent = cloud_pixels/img_pixels

        cloud_percent.append(img_cloud_percent)

    # Creating final result image.
    # image_dates coming from above.
    # image_dates.append("2018-01-01")
    # image_dates.append("2018-02-02")
    # image_dates.append("2018-03-03")

    y_pos = np.arange(len(image_dates))
    
    # cloud_percent.append(40)
    # cloud_percent.append(15)
    # cloud_percent.append(50)
 
    barlist = plt.bar(y_pos, cloud_percent, align='center', alpha=0.5)

    for i in barlist:
        if i.get_height() >=25:
            i.set_color('r')
        else:
            i.set_color('g')
        
    plt.xticks(y_pos, image_dates, rotation=45)
    plt.ylabel('% of cloud cover')
    plt.xlabel('Image acquition dates')
    plt.title('Sentinel 2A images cloud cover')
    x = stats.mean(cloud_percent)
    y = stats.median(cloud_percent)
    a = stats.stdev(cloud_percent)
    b = stats.variance(cloud_percent)

    cloud_stats="""    mean     :"""+format(x, '.2f')+"""
    median  :"""+format(y, '.2f')+"""
    stdev     :"""+format(a, '.2f')+"""
    variance:"""+format(b, '.2f')+""" """


    plt.axhline(y=25, color='b', linestyle='-')

    plt.text(len(cloud_percent),(max(cloud_percent))*0.4,cloud_stats, fontsize=20)
 
    plt.savefig('cloud.png', bbox_inches="tight")

    subprocess.call(["convert", "bar_chart.png", "cloud.jpg"])
       
    time.sleep(2)

    subprocess.call("rm *.vrt *.tif *.jpg *.xml *.img *.txt", shell=True)

    # udatate status content
    return {'current': 'bleek', 'total': 'steps6', 'status': 'PROCESSED', 'result': 'All Steps are finished successfully'}




@app.route('/longtask', methods=['POST'])
def longtask():
    with open('in_bbox.txt', 'w') as outfile:
        json.dump(request.json, outfile)
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'extent': task.info.get('extent', ''),
            'type': task.info.get('type', ''),
            'name': task.info.get('name', ''),
            'image_size' : task.info.get('image_size', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


@app.route('/')
def route():
    return "bleek"

@app.route('/index', methods=['GET'])
def index():
    return "Hello, World!"

# TODO: discuss about route should be with parameters or with out.
# The format of route is kind of analysis/algorithm/name of the satellite data/
@app.route('/cloud-cover/fmask/sentinel2', methods=['POST'])
def cloud_cover():    
    print(request.path)

    with open('in_dict.txt', 'w') as outfile:
        json.dump(request.json, outfile)

    input_dict = json.loads(request.data.decode())

    bbox = input_dict["bbox"]
    # getting integer part from epsd code.
    in_srs_code = int(input_dict["srs"].split(":")[1])  

    # Create ring
    ring = ogr.Geometry(ogr.wkbLinearRing)

    for point in bbox[0]:
        ring.AddPoint(point[0], point[1])

    # Create polygon
    in_poly = ogr.Geometry(ogr.wkbPolygon)
    in_poly.AddGeometry(ring) 
    
    # creating projection
    in_srs = osr.SpatialReference()
    in_srs.ImportFromEPSG(in_srs_code)

    out_srs = osr.SpatialReference()
    out_srs.ImportFromEPSG(4326)

    transform = osr.CoordinateTransformation(in_srs, out_srs)

    in_poly.AssignSpatialReference(in_srs)

    # TODO: optimiese this step wheather to transform input bbox or all shortlisted image bboxs.
    #in_poly.Transform(transform)

    
    # multi polygon for output
    out_multi_poly = ogr.Geometry(ogr.wkbMultiPolygon)

    out_multi_poly.AddGeometry(in_poly)
        
    # shortlisting images in give time and spatila extend.

    time_range = input_dict["date_range"]
    satellite = input_dict["satellite"]
    time_range = range(int(time_range[0].replace("-", "")), int(time_range[1].replace("-", "") ))
    

    data_dir = "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data"+os.sep+satellite


    # Temporal subset
    tmp_subset = []
    for img_dir in os.listdir(data_dir):
        date_img_dir = int(img_dir.split("_")[2].split("T")[0])
        if date_img_dir in time_range:
            tmp_subset.append(img_dir)

    # TODO:spatial subset, optimise sp_subset as global array
    sp_subset = []
    for img_dir in tmp_subset:
        
        #TODO: img extent is read from xml then we can exclude images with dark part. which is not possible if we use gdalinfo.
        img_xml_tree = etree.parse(data_dir+os.sep+img_dir+os.sep+'INSPIRE.xml')
        img_xml_root = img_xml_tree.getroot()
        # extracting image boundary polygon from xml
        img_bbox_char = img_xml_root[9][0][1][0].text.split(" ")

        # removing last element as it is empty string
        img_bbox_char.pop()
        # converting list to iter for pairwaise iteration
        img_bbox_char = iter(img_bbox_char)

        img_bbox = []
        # open layers takes in different order for x,y
        for x in img_bbox_char:
            img_bbox.append([float(next(img_bbox_char)), float(x)])
    

        # Create ring
        ring = ogr.Geometry(ogr.wkbLinearRing)

        for point in img_bbox:
            ring.AddPoint(point[0], point[1])

        # Create polygon
        img_poly = ogr.Geometry(ogr.wkbPolygon)
        img_poly.AddGeometry(ring) 

        # creating projection
        img_srs = osr.SpatialReference()
        img_srs.ImportFromEPSG(4326)

        img_poly.AssignSpatialReference(img_srs)

        transform = osr.CoordinateTransformation(img_srs, in_srs)

        img_poly.Transform(transform)


        if in_poly.Intersects(img_poly):
            sp_subset.append(img_dir)
            

    # writing sp_subset arry to file so we can access it in longterm task function. 
    # TODO: optimise this step later
    thefile = open('sp_subset.txt', 'w')

    for img in sp_subset:
        thefile.write("%s\n" % img)            
       
    task = long_task.apply_async()
    
    return jsonify({}), 202, {'Location': url_for('taskstatus',task_id=task.id)}

if __name__ == '__main__':
    app.run(debug=True)
