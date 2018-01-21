import numpy as np
import cv2
import json
import requests


filename = 'camera_calibration_data.json'

#Load JSON
with open(filename, 'r') as camera_calibration_file:
    camera_calibration_file_data = json.load(camera_calibration_file)
    camera_mtx = np.array(camera_calibration_file_data['mtx'])
    camera_dist = np.array(camera_calibration_file_data['dist'])

    post_obj = {}
    post_obj['mtx'] = camera_mtx.tolist()
    post_obj['dist'] = camera_dist.tolist()

    post_req = requests.post('http://localhost:8080/macbook_air_isight', data=json.dumps(post_obj), headers={'Content-Type': 'application/json'})
    print(post_req.status_code)
    print(post_obj)
    #print(camera_calibration_file_data['mtx'])
    #print(camera_calibration_file_data['dist'])