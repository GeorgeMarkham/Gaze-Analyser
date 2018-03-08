import numpy as np
import http.client, requests, urllib, base64, json
import scipy.linalg as lin
import timeit
import cv2
from math import atan, sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#function to access the webcam and capture an image
def get_img_from_webcam():
    camera = cv2.VideoCapture(0) #Select the camera to use, 0=built in webcam
    return_val, camera_img = camera.read() #read an image from the camera and get a return value
    if(return_val):
        cv2.imwrite('me_test.png', camera_img) #Write captured image to file (for testing)
        return cv2.imencode('.jpg', camera_img)[1].tostring() # return the image as a string
    else:
        return None


#Function to do point projection on the data returned by MS Face API
def pointprojection(x,y):
    with np.load('calib_data.npz') as data:
        K = np.array(data['mtx'])

        sx = K[0][0]
        sy = K[1][1]
        cx = K[0][2]
        cy = K[1][2]
        x_ext = ((x-cx)/sx)
        y_ext = ((y-cy)/sy)

        coords = np.array([x_ext, y_ext, 1])
        coords = np.hstack(coords)
        return coords

def plot3daxis(x,y,z,x2,y2,z2):
    w = 20
    f = plt.figure()
    ax = f.gca(projection='3d')
    ax.quiver(0, 0, 0., x, y, z,color='red')
    ax.set_xlim(0,10);ax.set_ylim(0,10);ax.set_zlim(0,10)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim(-w,w);ax.set_ylim(-w,w);ax.set_zlim(-w,w)
    ax.quiver(0, 0, 0., x2, y2, z2,color='blue')
    ax.set_xlim(0,10);ax.set_ylim(0,10);ax.set_zlim(0,10)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim(-w,w);ax.set_ylim(-w,w);ax.set_zlim(-w,w)
    plt.show()

def calculate_z(face_area):
    z = (-5262*face_area) + 16489.333333
    return z

#Set subscription key and base end point
SUBSCRIPTION_KEY = '9a296c80c0524db2bec178d1ad0efb61'
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
    'returnFaceAttributes': 'headPose'
}
try:
    #start the timer
    #start = timeit.default_timer()
    
    #make the POST request using params and headers defined above
    #json is none as I'm not sending any json in the request body, all data being sent is throught the data parameter
    res = requests.request('POST', ENDPOINT + '/detect', json=None, data=get_img_from_webcam(), headers=headers, params=params)
    
    #stop the timer
    #stop = timeit.default_timer()

    #parse the json
    parsed_res = json.loads(res.text)
    if(len(parsed_res) > 0):
        pupil_left_x = parsed_res[0]['faceLandmarks']['pupilLeft']['x']
        pupil_left_y = parsed_res[0]['faceLandmarks']['pupilLeft']['y']

        pupil_right_x = parsed_res[0]['faceLandmarks']['pupilRight']['x']
        pupil_right_y = parsed_res[0]['faceLandmarks']['pupilRight']['y']

        left_pupil_coords = pointprojection(x=pupil_left_x, y=pupil_left_y)
        right_pupil_coords = pointprojection(x=pupil_right_x, y=pupil_right_y)

        print(left_pupil_coords)
        print(right_pupil_coords)
except Exception as e:
    print(e)