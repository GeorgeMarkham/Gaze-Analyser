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
SUBSCRIPTION_KEY = 'YOUR SUBSCRIPTION KEY'
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
    #start the timer
    start = timeit.default_timer()
    
    #make the POST request using params and headers defined above
    #json is none as I'm not sending any json in the request body, all data being sent is throught the data parameter
    res = requests.request('POST', ENDPOINT + '/detect', json=None, data=get_img_from_webcam(), headers=headers, params=params)
    
    #stop the timer
    stop = timeit.default_timer()

    head_rect_width = 0
    head_rect_left = 0
    pupil_left_x = 0
    pupil_right_x = 0

    #parse the json
    parsed_res = json.loads(res.text)
    if(len(parsed_res) > 0):
        head_rect_width = parsed_res[0]['faceRectangle']['width']
        head_rect_left = parsed_res[0]['faceRectangle']['left']
        pupil_left_x = parsed_res[0]['faceLandmarks']['pupilLeft']['x']
        pupil_right_x = parsed_res[0]['faceLandmarks']['pupilRight']['x']

        pupil_center = ((pupil_right_x-pupil_left_x)/2 + pupil_left_x)
        head_center = (head_rect_width/2) + head_rect_left
        

        gaze_pos = head_center - pupil_center
        print("Pupil_Center = " + str(pupil_center))
        print("Head_Center = " + str(head_center))
        print("Gaze Position = " + str(gaze_pos))

    #dump json to a file
    with open('face_coords.json', 'w') as file_out:
        file_out.write(json.dumps({"head_rect_width": head_rect_width, "head_rect_left": head_rect_left, "pupil_left_x": pupil_left_x, "pupil_right_x": pupil_right_x}, indent=2))
    #print(json.dumps(parsed_res, sort_keys=True, indent=2))

    #if(len(json.dumps(parsed_res, sort_keys=True, indent=2)) > 10):
    #    print(stop-start)
except Exception as e:
    print(e)