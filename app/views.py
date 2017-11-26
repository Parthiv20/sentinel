# from app import app


import subprocess
import json
import os
import xml.etree.ElementTree as etree
import random
import time

from osgeo import ogr
from osgeo import osr
from flask import Flask, request, render_template, session, flash, redirect, url_for, jsonify
from celery import Celery


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
    # for i in range(1, 25):
    #     time.sleep(1)
    #     message1 = 'time count less than 10 seconds'
    #     message2 = 'time count less than 20 seconds'
    #     message3 = 'final time count'

    #     if i < 10:
    #         self.update_state(state='PROGRESS',
    #                           meta={'current': i, 'total': 25,
    #                                  'status': message1})
    #     elif i < 20:
    #         self.update_state(state='PROGRESS',
    #                           meta={'current': i, 'total': 25,
    #                                  'status': message2})
    #     else:
    #         self.update_state(state='PROGRESS',
    #                           meta={'current': i, 'total': 25,
    #                                  'status': message3})
    
    # TODO: optimise this step later
    f = open('sp_subset.txt', 'r')
    img_list = f.read().splitlines()

    print(img_list)

    gdalbuildvrt = subprocess.check_output(["which", "gdalbuildvrt"])[:-1].decode("utf-8")

    self.update_state(state='PROGRESS', meta={'current': 'step1', 'total': 'stpes6', 'status': 'This first step shortlisting images'})
    time.sleep(10)

    self.update_state(state='PROGRESS', meta={'current': 'step2', 'total': 'stpes6', 'status': 'This second step merging all bands for image'})

    subprocess.call([gdalbuildvrt, "-resolution", "user", "-tr", "60", "60", "-separate", "allbands.vrt", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B01.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B02.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B03.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B04.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B05.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B06.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B07.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B08.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B8A.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B09.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B10.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B11.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B12.jp2"])     
    time.sleep(5)

    self.update_state(state='PROGRESS', meta={'current': 'step3', 'total': 'stpes6', 'status': 'This third step sun angle image creation'})

    subprocess.call(["fmask_sentinel2makeAnglesImage.py", "-i", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/MTD_TL.xml", "-o", "angles.img"])
    time.sleep(5)

    self.update_state(state='PROGRESS', meta={'current': 'step4', 'total': 'stpes6', 'status': 'This fourth step cloud image creation its longer step'})

    subprocess.call(["fmask_sentinel2Stacked.py", "-a", "allbands.vrt", "-z", "angles.img", "-o", "cloud.img"])

    gdalinfo = subprocess.check_output(["which", "gdalinfo"])[:-1].decode("utf-8")

    img_info = json.loads(subprocess.check_output([gdalinfo, "-json", "cloud.img"]).decode("utf-8"))

    img_pixles = img_info["size"][0]*img_info["size"][1]

    cloud_pixels = img_info["rat"]["row"][2]["f"][0]

    cloud_percent = str((cloud_pixels/img_pixles)*100)

    self.update_state(state='PROGRESS', meta={'current': 'step5', 'total': 'stpes6', 'status': 'This fifth step cloud cover percentage: '+cloud_percent})
    time.sleep(10)

    return {'current': 'step6', 'total': 'steps6', 'status': 'PROCESSED', 'result': 'All Steps are finished successfully'}




@app.route('/longtask', methods=['POST'])
def longtask():
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
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
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

    # in_poly.Transform(transform)

    
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
    
    # TODO:spatila subset, optimise sp_subset as global array
    sp_subset = []
    for img_dir in tmp_subset:
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
            out_multi_poly.AddGeometry(img_poly)


    # converting to GeoJSON
    
    out_geojson = out_multi_poly.ExportToJson()

    # writing sp_subset arry to file so we can access in longterm task function. 
    # TODO: optimise this step later
    thefile = open('sp_subset.txt', 'w')

    for img in sp_subset:
        thefile.write("%s\n" % img)             
        
    return out_geojson

if __name__ == '__main__':
    app.run(debug=True)
