import numpy as np
import base64
import cv2

#cv2.imwrite('test.png',frame)


camera = cv2.VideoCapture(0) #Select the camera to use, 0=built in webcam
return_val, camera_img = camera.read() #read an image from the camera and get a return value
if(return_val):
    #cv2.imwrite('test_img.png', camera_img)
    camera_img_gray = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)
    print(camera_img_gray.shape[0])
camera.release()

#np.set_printoptions(precision=3)
#print(base64.b64encode(camera_img))