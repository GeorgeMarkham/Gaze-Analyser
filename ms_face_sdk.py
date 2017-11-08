import cognitive_face as CognitiveFace
import numpy as np
import base64
import cv2

def get_img_from_webcam():
    camera = cv2.VideoCapture(0) #Select the camera to use, 0=built in webcam
    return_val, camera_img = camera.read() #read an image from the camera and get a return value
    if(return_val):
        return base64.b64encode(camera_img)
    else:
        return None


#Variables holding account data
SUBSCRIPTION_KEY = '0f823364b6b140a1aa657fc73983357b'
ENDPOINT = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/'

#Apply account details to variables
CognitiveFace.Key.set(SUBSCRIPTION_KEY)
CognitiveFace.BaseUrl.set(ENDPOINT)

#img = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'

img = get_img_from_webcam()

#result = CognitiveFace.face.detect(img)
result = CognitiveFace.face.detect(img, landmarks=True)

print(result)
