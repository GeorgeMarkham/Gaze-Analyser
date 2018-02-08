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
def pointprojection(left_pupil_x, left_pupil_y, right_pupil_x, right_pupil_y):
    with np.load('calib_data.npz') as data:
        mtx = np.array(data['mtx'])
        dist = np.array(data['dist'])
        rvecs = np.array(data['rvecs'])
        tvecs = np.array(data['tvecs'])

        R = np.eye(3)
        T = np.array([[0],[1],[0]])

        P = mtx.dot(np.hstack((R,T)))
        
        x_left = np.array([left_pupil_x,left_pupil_y,1])
        X_left = np.dot(lin.pinv(P), x_left)
        X_left = X_left / X_left[3]

        XX_left  = X_left[:]
        XX_left[1] = X_left[2]
        XX_left[2] = X_left[1]
        x_coord_left = XX_left[:3][0]
        y_coord_left = XX_left[:3][1]
        z_coord_left = XX_left[:3][2]

        #gaze_angle_left = atan((y_coord_left/x_coord_left))

        hyp_left = sqrt( ( (x_coord_left*x_coord_left) + (y_coord_left*y_coord_left) + (z_coord_left*z_coord_left) ) )
        print("\n\n\nhyp_left = \n", hyp_left)

        #print("\n\n\nθ (left) = \n", gaze_angle_left)
        print('\nx_coord_left = \n', x_coord_left, '\ny_coord_left = \n', y_coord_left, '\nz_coord_left = \n', z_coord_left)

        x_right = np.array([right_pupil_x,right_pupil_y,1])
        X_right = np.dot(lin.pinv(P), x_right)
        X_right = X_right / X_right[3]

        XX_right  = X_right[:]
        XX_right[1] = X_right[2]
        XX_right[2] = X_right[1]
        x_coord_right = XX_right[:3][0]
        y_coord_right = XX_right[:3][1]
        z_coord_right = XX_right[:3][2]

        #gaze_angle_right = atan((y_coord_right/x_coord_right))
        #print("\n\n\nθ (right) = \n", gaze_angle_right)

        hyp_right = sqrt( ( (x_coord_right*x_coord_right) + (y_coord_right*y_coord_right) + (z_coord_right*z_coord_right) ) )
        print("\n\n\nhyp_right = \n", hyp_right)
        print('\nx_coord_right = \n', x_coord_right, '\ny_coord_right = \n', y_coord_right, '\nz_coord_right = \n', z_coord_right)

        plot3daxis(x_coord_left, y_coord_left, z_coord_left, x_coord_right, y_coord_right, z_coord_right)
        #plot3daxis(x_coord_left, y_coord_left, z_coord_left)

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

        pointprojection(left_pupil_x = pupil_left_x, left_pupil_y = pupil_left_y, right_pupil_x = pupil_right_x, right_pupil_y = pupil_right_y)


except Exception as e:
    print(e)