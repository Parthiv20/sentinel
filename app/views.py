from app import app


import subprocess
import json
import os
import xml.etree.ElementTree as etree

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
    # spatila subset
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

    # could_cover analysis
                    
        
    return out_geojson

