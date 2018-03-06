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
    # TODO: optimise this step later

    # f = open('sp_subset.txt', 'r')
    # img_list = f.read().splitlines()
    # f.close()
    # print(img_list)

    with open('data.txt') as f:
        in_dict = json.load(f)

    # print(in_dict)

    # poly2_extent = copy.deepcopy(in_dict['extent'])

    # del poly2_extent[0][3]
    # poly2_extent[0][2] = copy.deepcopy(in_dict['center'])

    # poly3_extent = copy.deepcopy(in_dict['extent'])

    # del poly3_extent[0][2]
    # poly3_extent[0][1] = copy.deepcopy(in_dict['center'])   

    # poly4_extent = copy.deepcopy(in_dict['extent'])
    
    # del poly4_extent[0][0]
    # del poly4_extent[0][-1]
    # poly4_extent[0][2] = copy.deepcopy(in_dict['center'])
    # poly4_extent[0].append(poly4_extent[0][0])


    # poly5_extent = copy.deepcopy(in_dict['extent'])
    
    # del poly5_extent[0][0]
    # del poly5_extent[0][-1]
    # del poly5_extent[0][0]
    # poly5_extent[0].append(in_dict['center'])
    # poly5_extent[0].append(poly5_extent[0][0])


    img_poly = '{ "type": "Polygon", "coordinates": [ [ [ 838405.962330951588228, 6862082.408005863428116, 0.0 ], [ 1017826.472330141579732, 6863729.436798275448382, 0.0 ], [ 1017481.162819475051947, 6685785.296250037848949, 0.0 ], [ 841943.274732842110097, 6684229.797995020635426, 0.0 ], [ 838405.962330951588228, 6862082.408005863428116, 0.0 ] ] ] }'

    poly1 = '{ "type": "Polygon", "coordinates":'+str(in_dict['extent'])+'}'

    # poly2 = '{ "type": "MultiPolygon", "coordinates":['+str(poly2_extent)+']}'

    # poly3 = '{ "type": "MultiPolygon", "coordinates":['+str(poly3_extent)+']}'

    # poly4 = '{ "type": "MultiPolygon", "coordinates":['+str(poly4_extent)+']}'

    # poly5 = '{ "type": "MultiPolygon", "coordinates":['+str(poly5_extent)+']}'


    self.update_state(state='PROGRESS', meta={'current': poly1, 'type': 'vector', 'status': 'This first step shortlisting images'})
    time.sleep(1)


    gdalbuildvrt = subprocess.check_output(["which", "gdalbuildvrt"])[:-1].decode("utf-8")

    gdal_translate = subprocess.check_output(["which", "gdal_translate"])[:-1].decode("utf-8")

    subprocess.call([gdalbuildvrt, "-resolution", "user", "-tr", "60", "60", "-separate", "rgb.vrt", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B02.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B03.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B04.jp2"])

    subprocess.call([gdal_translate, "-of", "JPEG", "-ot", "Byte", "-scale", "rgb.vrt", "rgb.jpg"])

    self.update_state(state='PROGRESS', meta={'current': 'raster', 'total': [838405.962, 6684208.676, 1017845.334, 6863745.147], 'status':'rgb.jpg' })
    time.sleep(1)

    # self.update_state(state='PROGRESS', meta={'current': poly2, 'total': 'stpes6', 'status': 'This second step merging all bands for image'})
    
    # #subprocess.call([gdalbuildvrt, "-resolution", "user", "-tr", "60", "60", "-separate", "allbands.vrt", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B01.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B02.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B03.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B04.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B05.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B06.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B07.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B08.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B8A.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B09.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B10.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B11.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B12.jp2"])     
    # #time.sleep(5)

    # self.update_state(state='PROGRESS', meta={'current': poly3, 'total': 'stpes6', 'status': 'This third step sun angle image creation'})

    # #subprocess.call(["fmask_sentinel2makeAnglesImage.py", "-i", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/MTD_TL.xml", "-o", "angles.img"])
    # #time.sleep(5)

    # self.update_state(state='PROGRESS', meta={'current': poly4, 'total': 'stpes6', 'status': 'This fourth step cloud image creation its longer step'})
    # #time.sleep(5)

    # subprocess.call(["fmask_sentinel2Stacked.py", "-a", "allbands.vrt", "-z", "angles.img", "-o", "cloud.img"])

    # gdalinfo = subprocess.check_output(["which", "gdalinfo"])[:-1].decode("utf-8")

    # img_info = json.loads(subprocess.check_output([gdalinfo, "-json", "cloud.img"]).decode("utf-8"))

    # img_pixles = img_info["size"][0]*img_info["size"][1]

    # cloud_pixels = img_info["rat"]["row"][2]["f"][0]

    # cloud_percent = str((cloud_pixels/img_pixles)*100)

    #self.update_state(state='PROGRESS', meta={'current': poly5, 'total': 'stpes6', 'status': 'This fifth step cloud cover percentage:'})
    #time.sleep(5)


    # tiles creation for the image
    img_xml_tree = etree.parse('/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/INSPIRE.xml')
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

    out_srs = osr.SpatialReference()
    out_srs.ImportFromEPSG(3857)

    img_poly.AssignSpatialReference(img_srs)

    transform = osr.CoordinateTransformation(img_srs, out_srs)

    img_poly.Transform(transform)

    img_geojson = img_poly.ExportToJson()

    # print(img_geojson)

    # with open('geoj', 'w')as f:
    #     f.write(img_geojson)

    #geojson grids creation as list

    a = list(range(838405,1017826,17942))

    b = list(range(6684229,6863729,17949))

    m = zip(a,a[1:])
    n = zip(b,b[1:])

    mn_cart = list(itertools.product(m,n))

    geoj_list = []

    for x in mn_cart:
        result = list(itertools.product([x[0][0],x[0][1]],[x[1][0],x[1][1]]))

        result[2], result[3] = result[3], result[2]

        result.append(result[0])


        gjson = Polygon([result])

        geoj_list.append(gjson)
    geoj_list.append(gjson)


    # test for small size updates
    i = 0
    crop_path = '/mnt/c/Users/pgulla/Desktop/thesis/openeo/crop_test/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA'
    
    #################################************************************backup for grid visuvalisation*******************************####################
    # # p = Popen(['inotifywait', '-m', '-r', '-e', 'create', './'], stdout=PIPE, bufsize=1, universal_newlines=True)
    # with Popen(['inotifywait', '-m', '-r', './'], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
    #     subprocess.Popen([gdalbuildvrt, "-resolution", "user", "-tr", "60", "60", "-separate", "allbands.vrt", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B01.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B02.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B03.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B04.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B05.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B06.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B07.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B08.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B8A.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B09.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B10.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B11.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B12.jp2"])     
    #     subprocess.Popen(["fmask_sentinel2makeAnglesImage.py", "-i", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/MTD_TL.xml", "-o", "angles.img"])
    #     subprocess.Popen(["fmask_sentinel2Stacked.py", "-a", "allbands.vrt", "-z", "angles.img", "-o", "cloud.img"])
    #     subprocess.Popen(["rm", "data.txt"])
    #     subprocess.Popen(["rm", "rgb.vrt"])
    #     for line in p.stdout:
    #         #print(str(i)+line, end='') # process line here
    #         self.update_state(state='PROGRESS', meta={'current': str(geoj_list.pop(random.randrange(len(geoj_list)))), 'type': 'vector', 'status': 'This is'+str(i)+'th step'})
    #         i +=1
    #         print(str(i)+line)
    #         time.sleep(0.800)
    #         if i == 101:
    #         # to get 100 grids add aditional 3 steps here
    #             break
    #   p.kill()
    #   subprocess.call([gdal_translate, "-of", "JPEG", "-ot", "Byte", "-expand", "rgb", "-scale", "cloud.img", "rgb.jpg"])
        
    #   self.update_state(state='PROGRESS', meta={'current': 'raster', 'type': 'raster', 'status': 'This is last step shortlisting images'})
    #   time.sleep(10)
    #################################************************************backup for grid visuvalisation*******************************####################

    subprocess.call([gdalbuildvrt, "-resolution", "user", "-tr", "60", "60", "-separate", "allbands.vrt", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B01.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B02.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B03.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B04.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B05.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B06.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B07.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B08.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B8A.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B09.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B10.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B11.jp2", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/IMG_DATA/T32UMC_20170619T103021_B12.jp2"])

    subprocess.call(["fmask_sentinel2makeAnglesImage.py", "-i", "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data/sentinel2/S2A_MSIL1C_20170619T103021_N0205_R108_T32UMC_20170619T103021.SAFE/GRANULE/L1C_T32UMC_A010401_20170619T103021/MTD_TL.xml", "-o", "angles.img"])

    ds = gdal.Open('allbands.vrt')

    x = ds.RasterXSize

    y = ds.RasterYSize

    ds = None

    # TODO:update here for user specified grid size
    x_arr = np.linspace(0, x, 2, endpoint=False).tolist()
    y_arr = np.linspace(0, y, 2, endpoint=False).tolist()

    xy_cartesian = list(itertools.product(x_arr, y_arr))

    # TODO:update here for user specified grid size
    x_step = x/2
    y_step = y/2

    cloud_pixels = 0

    j=0
    random.shuffle(xy_cartesian)
    for i in xy_cartesian:
        j += 1
        subprocess.call(['gdal_translate', '-srcwin', str(i[0]), str(i[1]), str(x_step), str(y_step), 'allbands.vrt', 'rast'+str(j)+'.tif' ])
        subprocess.call(['fmask_sentinel2Stacked.py', '-a', 'rast'+str(j)+'.tif', '-z', 'angles.img', '-o', 'cloud'+str(j)+'.img'])
        subprocess.call(['rm', 'rast'+str(j)+'.tif'])
        subprocess.call(['gdal_translate', '-of', 'JPEG', '-ot', 'Byte', '-expand', 'rgb', '-scale', 'cloud'+str(j)+'.img', 'cloud'+str(j)+'.jpg'])
        img_info = json.loads(subprocess.check_output(['gdalinfo', "-json", 'cloud'+str(j)+'.img']).decode("utf-8"))
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
        subprocess.call(['rm', 'cloud'+str(j)+'.jpg.aux.xml'])
        subprocess.call(['rm', 'cloud'+str(j)+'.img'])
        subprocess.call(['rm', 'cloud'+str(j)+'.img.aux.xml'])

        # TODO: update total to name.
        self.update_state(state='PROGRESS', meta={'current': 'raster', 'total':grid_extent, 'status': 'cloud'+str(j)+'.jpg' })
        time.sleep(10)

        
        # # Creating final result image.
        # objects = ('2017-05-05', '2017-06-05', '2017-07-05', '2017-08-05', '2017-09-05', '2017-10-05', '2017-11-05', '2017-12-05')
        # y_pos = np.arange(len(objects))
        # cloud_percent = [30, 10, 20, 16, 18, 50, 38, 28]
 
        # barlist = plt.bar(y_pos, cloud_percent, align='center', alpha=0.5)

        # for i in barlist:
        #     if i.get_height() >=25:
        #         i.set_color('r')
        #     else:
        #         i.set_color('g')
        
        
        # #     if i.get_height() > 25:
        # #         i.set_color('r')
        # # else:
        # #     i.set_color('g')

        # plt.xticks(y_pos, objects, rotation=45)
        # plt.ylabel('% of cloud cover')
        # plt.xlabel('Image acquition dates')
        # plt.title('Sentinel 2A images cloud cover')

        # x = stats.mean(cloud_percent)
        # y = stats.median(cloud_percent)
        # a = stats.stdev(cloud_percent)
        # b = stats.variance(cloud_percent)


        # # cloud_stats = """mean     :"""+format(x, '.2f')+"""
        # # median  :"""+format(y, '.2f')+"""
        # # stdev     :"""+format(a, '.2f')+"""
        # # variance:"""+format(b, '.2f')+""" """


        # cloud_stats = 'mean     :'+format(x, '.2f')+os.linesep+'median  :'+format(y, '.2f')+os.linesep+'stdev     :'+format(a, '.2f')+os.linesep+'variance:'+format(b, '.2f')


        # plt.axhline(y=25, color='b', linestyle='-')

        # plt.text(len(cloud_percent),(max(cloud_percent))*0.4,cloud_stats, fontsize=20)
 
        # plt.savefig('cloud.png', bbox_inches="tight")

        # #subprocess.call(["convert", "bar_chart.png", "cloud.jpg"])
       

    return {'current': img_geojson, 'total': 'steps6', 'status': 'PROCESSED', 'result': 'All Steps are finished successfully'}




@app.route('/longtask', methods=['POST'])
def longtask():
    with open('data.txt', 'w') as outfile:
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
    
    # TODO:spatial subset, optimise sp_subset as global array
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

    # writing sp_subset arry to file so we can access it in longterm task function. 
    # TODO: optimise this step later
    thefile = open('sp_subset.txt', 'w')

    for img in sp_subset:
        thefile.write("%s\n" % img)             
       
    return out_geojson

if __name__ == '__main__':
    app.run(debug=True)
