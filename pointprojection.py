import numpy as np
import scipy.linalg as lin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import atan, pi
import http.client, requests, urllib, base64, json
import cv2

def get_img_from_webcam():
    camera = cv2.VideoCapture(0) #Select the camera to use, 0=built in webcam
    return_val, camera_img = camera.read() #read an image from the camera and get a return value
    if(return_val):
        cv2.imwrite('me_test.png', camera_img) #Write captured image to file (for testing)
        return cv2.imencode('.jpg', camera_img)[1].tostring() # return the image as a string
    else:
        return None


def calculate_eye_center(eye_left_top, eye_left_bottom, eye_left_outer, eye_left_inner):
    eye_center_1_x = ((eye_left_inner['x']-eye_left_outer['x'])/2)
    eye_center_2_x = ((eye_left_bottom['x']-eye_left_top['x'])/2)

    eye_center_1_y = ((eye_left_inner['y']-eye_left_outer['y'])/2)
    eye_center_2_y = ((eye_left_bottom['y']-eye_left_top['y'])/2)

    eye_center_1_x = eye_left_outer['x'] + eye_center_1_x
    eye_center_2_x = eye_left_top['x'] + eye_center_2_x

    eye_center_1_y = eye_left_outer['y'] + eye_center_1_y
    eye_center_2_y = eye_left_bottom['y'] + eye_center_2_y

    center = (((eye_center_1_x+eye_center_2_x)/2), ((eye_center_1_y+eye_center_2_y)/2))
    print(center)
    return center

def calculate_angle(center, pupil_left):
    center_x, center_y = center
    pupil_left_x, pupil_left_y = pupil_left

    angle = atan( (center_x-pupil_left_x) / (center_x-pupil_left_x) )
    return angle

def calculate_z(area, slope, intercept):
    z = slope*area + intercept
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
    res = requests.request('POST', ENDPOINT + '/detect', json=None, data=get_img_from_webcam(), headers=headers, params=params)
    
    #stop the timer
    #stop = timeit.default_timer()

    #parse the json
    parsed_res = json.loads(res.text)
    if(len(parsed_res) > 0):

        face_rect_width = parsed_res[0]['faceRectangle']['width']
        face_rect_height = parsed_res[0]['faceRectangle']['height']

        face_area = face_rect_height*face_rect_width

        pupil_left_x = parsed_res[0]['faceLandmarks']['pupilLeft']['x']
        pupil_left_y = parsed_res[0]['faceLandmarks']['pupilLeft']['y']

        eye_left_top = parsed_res[0]['faceLandmarks']['eyeLeftTop']
        eye_left_bottom = parsed_res[0]['faceLandmarks']['eyeLeftBottom']
        eye_left_outer = parsed_res[0]['faceLandmarks']['eyeLeftOuter']
        eye_left_inner = parsed_res[0]['faceLandmarks']['eyeLeftInner']

        eye_left_center = calculate_eye_center(eye_left_top, eye_left_bottom, eye_left_outer, eye_left_inner)

        pupil_right_x = parsed_res[0]['faceLandmarks']['pupilRight']['x']
        pupil_right_y = parsed_res[0]['faceLandmarks']['pupilRight']['y']
        
        #yaw already in degrees
        yaw = parsed_res[0]['faceAttributes']['headPose']['yaw']

        print('\nyaw: ', yaw)


        # Do the point projection #
        with np.load('calib_data.npz') as data:
            with np.load('predict_z_vals.npz') as predict_z_vals:

                slope = predict_z_vals['slope']
                intercept = predict_z_vals['intercept'] + 1

                print('intercept:', intercept)

                K = np.array(data['mtx'])
                #K = [[ 282.363047,      0.,          166.21515189],[   0.,          280.10715905,  108.05494375],[   0.,            0.,            1.        ]]
                rvecs = np.array(data['rvecs'])
                R = cv2.Rodrigues(rvecs)

                sx = K[0][0]
                sy = K[1][1]
                cx = K[0][2]
                cy = K[1][2]
                cz = K[2][2]
                
                x = pupil_left_x
                y = pupil_left_y

                eyeball_depth = 23.4
                eyeball_height = 23.7

                X_w = ((x-cx)/sx)
                Y_w = ((y-cy)/sy)
                Z_w = calculate_z(face_area, slope, intercept)

                center_x, center_y = eye_left_center

                center_x_w = ((center_x-cx)/sx)
                center_y_w = ((center_y-cx)/sx)



                center = (center_x_w, center_y_w, Z_w)
                pupil_left_coords = (X_w, Y_w, Z_w)

                Eye_left_cx = center_x_w
                Eye_left_cy = center_y_w

                proj_eye_left_x = ((X_w-Eye_left_cx)/sx)
                proj_eye_left_y = ((Y_w-Eye_left_cy)/sy)

                print('proj_eye_left_x: ', proj_eye_left_x)
                print('proj_eye_left_y: ', proj_eye_left_y)
                print('Z_w:' , Z_w)

                angle_x = atan( (Eye_left_cx-proj_eye_left_x) / (eyeball_depth/2) )
                print('angle_x *: ', angle_x)
                angle_x = angle_x * (180/pi)
                print('angle_x: ', angle_x)

                angle_y = atan( (Eye_left_cy-proj_eye_left_y) / (eyeball_height/2) )
                print('angle_y *: ', angle_y)
                angle_y = angle_y * (180/pi)
                print('angle_y: ', angle_y)

                gaze_angle_x = angle_x + yaw

                print(gaze_angle_x)



except Exception as e:
    print(e)
