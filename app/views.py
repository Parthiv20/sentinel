from app import app
from flask import request
import subprocess
import json
import shapely
from shapely import geometry


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
    srs = input_dict["srs"]  
    print(bbox) 
    print(srs)
    user_box = geometry.box(bbox[0], bbox[1], bbox[2], bbox[3])
    print(type(user_box))

    return "testing the post request"
