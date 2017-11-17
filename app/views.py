from app import app


import subprocess
import json
import os

from osgeo import ogr
from osgeo import osr
from flask import request


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

    # Testing for GeoJSON
    out_geojson = in_poly.ExportToJson()
    
    # shortlisting images in give time and spatila extend.

    time_range = input_dict["date_range"]
    satellite = input_dict["satellite"]
    print(time_range[0].replace("-", ""), time_range[1].replace("-", "") )
    print(satellite)
    

    data_dir = "/mnt/c/Users/pgulla/Desktop/thesis/openeo/webapp/data"+os.sep+satellite

    # Temporal subset
    for img_dir in os.listdir(data_dir):
        print(img_dir)
        print(img_dir.split("_")[2].split("T")[0])
        print(type((img_dir.split("_")[2].split("T")[0])))

    return out_geojson


# [[[-1311047.9091473483, 8061966.247294111], [-1311047.9091473483, 4070118.8821290676], 
# [3189564.3162838295, 4070118.8821290676],
# [3189564.3162838295, 8061966.247294111], [-1311047.9091473483, 8061966.247294111]]]