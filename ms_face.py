import numpy as np
import http.client, requests, urllib, base64, json
import timeit
import cv2

#function to access the webcam and capture an image
def get_img_from_webcam():
    camera = cv2.VideoCapture(0) #Select the camera to use, 0=built in webcam
    return_val, camera_img = camera.read() #read an image from the camera and get a return value
    if(return_val):
        cv2.imwrite('me_test.png', camera_img) #Write captured image to file (for testing)
        return cv2.imencode('.jpg', camera_img)[1].tostring() # return the image as a string
    else:
        return None

#Set subscription key and base end point
SUBSCRIPTION_KEY = '0f823364b6b140a1aa657fc73983357b'
ENDPOINT = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/'

#Set headers, octet-stream is to send an image to the api
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
}
#Tell the api what I want back from it
params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'emotion,headPose'
}
try:
    start = timeit.default_timer()
    #make the POST request using params and headers defined above
    #json is none as I'm not sending any json in the request body, all data being sent is throught the data parameter
    res = requests.request('POST', ENDPOINT + '/detect', json=None, data=get_img_from_webcam(), headers=headers, params=params)
    #parse the json
    stop = timeit.default_timer()
    #print(stop-start)
    parsed_res = json.loads(res.text)
    #dump json to the command line
    #print(json.dumps(parsed_res, sort_keys=True, indent=2))
    if(len(json.dumps(parsed_res, sort_keys=True, indent=2)) > 10):
        print(stop-start)
except Exception as e:
    print(e)