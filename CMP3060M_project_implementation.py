#An implementation of the algorithm outlined in "A Study Of Non-Invasive Gaze Detection Methods" by George Markham, 2018

#Import libraries
import numpy as np
import cv2
import scipy.linalg as lin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import tan, atan, pi, radians
import http.client, requests, urllib, base64, json
from sys import argv


#Helper functions
def get_img_from_file(file_name):
    img = cv2.imread(file_name)
    img = cv2.flip(img, 1)
    return cv2.imencode('.jpg', img)[1].tostring() # return the image as a string

def get_img_from_webcam(cam_num):
    camera = cv2.VideoCapture(int(cam_num)) #Select the camera to use, 0=built in webcam
    return_val, camera_img = camera.read() #read an image from the camera and get a return value
    if(return_val):
        camera_img = cv2.flip(camera_img, 1)
        return cv2.imencode('.jpg', camera_img)[1].tostring() # return the image as a string
    else:
        return None

def parse_res(res):

    #Return dictionary
    parsed_res = json.loads(res.text)
    if(len(parsed_res) > 0):
        face_rect_width = parsed_res[0]['faceRectangle']['width']
        face_rect_height = parsed_res[0]['faceRectangle']['height']

        face_area = face_rect_height*face_rect_width

        yaw = parsed_res[0]['faceAttributes']['headPose']['yaw']

        pupil_left_x = parsed_res[0]['faceLandmarks']['pupilLeft']['x']
        pupil_left_y = parsed_res[0]['faceLandmarks']['pupilLeft']['y']

        eye_left_top = parsed_res[0]['faceLandmarks']['eyeLeftTop']
        eye_left_bottom = parsed_res[0]['faceLandmarks']['eyeLeftBottom']
        eye_left_outer = parsed_res[0]['faceLandmarks']['eyeLeftOuter']
        eye_left_inner = parsed_res[0]['faceLandmarks']['eyeLeftInner']

        eye_left_center = calculate_eye_center(eye_left_top, eye_left_bottom, eye_left_outer, eye_left_inner)

        eye_right_top = parsed_res[0]['faceLandmarks']['eyeRightTop']
        eye_right_bottom = parsed_res[0]['faceLandmarks']['eyeRightBottom']
        eye_right_outer = parsed_res[0]['faceLandmarks']['eyeRightOuter']
        eye_right_inner = parsed_res[0]['faceLandmarks']['eyeRightInner']

        eye_right_center = calculate_eye_center(eye_right_top, eye_right_bottom, eye_right_outer, eye_right_inner)
        
        pupil_right_x = parsed_res[0]['faceLandmarks']['pupilRight']['x']
        pupil_right_y = parsed_res[0]['faceLandmarks']['pupilRight']['y']

        facial_landmarks = {}
        facial_landmarks['face_area'] = face_area
        facial_landmarks['pupil_left_x'] = pupil_left_x
        facial_landmarks['pupil_left_y'] = pupil_left_y
        facial_landmarks['pupil_right_x'] = pupil_right_x
        facial_landmarks['pupil_right_y'] = pupil_right_y
        facial_landmarks['eye_left_center'] = eye_left_center
        facial_landmarks['eye_right_center'] = eye_right_center
        facial_landmarks['yaw'] = yaw

        return facial_landmarks

    return {}

def calculate_angle(center, pupil):
    eyeball_depth = 23.4
    angle = atan( (center-pupil) / (eyeball_depth/2) )

    return angle * (180/pi)

def calculate_z(area):
    predict_z_vals = np.load('predict_z_vals.npz')
    slope = predict_z_vals['slope']
    intercept = predict_z_vals['intercept']
    z = slope*area + intercept
    return z

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
    return center

def get_metric(facial_landmarks):
    #Get the camera calibration data
    K = np.array(np.load('calib_data.npz')['mtx'])

    sx = K[0][0]
    sy = K[1][1]
    cx = K[0][2]
    cy = K[1][2]
    cz = K[2][2]

    facial_landmarks_metric = {}
    facial_landmarks_metric['face_area'] = facial_landmarks['face_area']
    facial_landmarks_metric['pupil_left_x'] = ((facial_landmarks['pupil_left_x']-cx)/sx)
    facial_landmarks_metric['pupil_left_y'] = ((facial_landmarks['pupil_left_y']-cy)/sy)
    facial_landmarks_metric['pupil_right_x'] = ((facial_landmarks['pupil_right_x']-cx)/sx) 
    facial_landmarks_metric['pupil_right_y'] = ((facial_landmarks['pupil_right_y']-cy)/sy) 
    facial_landmarks_metric['eye_left_center'] = ((facial_landmarks['eye_left_center'][0]-cx)/sx) 
    facial_landmarks_metric['eye_right_center'] = ((facial_landmarks['eye_right_center'][0]-cx)/sx) 
    facial_landmarks_metric['yaw'] = facial_landmarks['yaw']
    return facial_landmarks_metric

def calculate_point(gaze_angle, z, origin):
    offset = z * (tan(radians(gaze_angle)))
    return origin + offset


#Set subscription key and base end point
# SUBSCRIPTION_KEY = 'YOUR API KEY'
# ENDPOINT = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/'

SUBSCRIPTION_KEY = 'SUBSCRIPTION_KEY'
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

predict_z = np.load('calib_data.npz')

if len(argv) > 3: #Means z is passed as an argument
    if argv[3] == 'z': 
        z_val = float(argv[4])


if argv[1] == 'i' :
    #Use an image file
    img_file = argv[2]
    res = requests.request('POST', ENDPOINT + '/detect', json=None, data=get_img_from_file(img_file), headers=headers, params=params)
    parsed_response = parse_res(res)

    parsed_response = parse_res(res)
    if len(parsed_response) > 0:
        metric_landmarks = get_metric(parsed_response)
        gaze_angle = metric_landmarks['yaw'] + (( calculate_angle(metric_landmarks['eye_left_center'], metric_landmarks['pupil_left_x']) + calculate_angle(metric_landmarks['eye_right_center'], metric_landmarks['pupil_left_x']) )/2)
        
        if(z_val == 0):
            z_val = calculate_z(metric_landmarks['face_area'])
        
        point = calculate_point(gaze_angle, z_val, ( (metric_landmarks['eye_left_center'] + metric_landmarks['eye_right_center'])/2 ) )
        print(point)
    else:
        print("Couldn't find any faces")

elif argv[1] == 'c':
    #Get image from webcam
    cam = argv[2]
    res = requests.request('POST', ENDPOINT + '/detect', json=None, data=get_img_from_webcam(int(cam)), headers=headers, params=params)
    parsed_response = parse_res(res)
    if len(parsed_response) > 0:
        metric_landmarks = get_metric(parsed_response)

        if(z_val == 0):
            z_val = calculate_z(metric_landmarks['face_area'])

        gaze_angle = metric_landmarks['yaw'] + (( calculate_angle(metric_landmarks['eye_left_center'], metric_landmarks['pupil_left_x']) + calculate_angle(metric_landmarks['eye_right_center'], metric_landmarks['pupil_left_x']) )/2)
        point = calculate_point(gaze_angle, z_val, ( (metric_landmarks['eye_left_center'] + metric_landmarks['eye_right_center'])/2 ) )
        print(point)
    else:
        print("Couldn't find any faces")

elif argv[1] == 'h':
    print("\n\tHelp:")
    print("\tUse i followed by an image file to use an image on your computer")
    print("\tUse c followed by the number that corresponds to the camera you want to use (use 0 for the default system webcam)\n")
else:
    print(argv)
    print("Please specify an image source, use the h argument if you need help")