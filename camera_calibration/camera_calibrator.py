import numpy as np
import cv2
import json


doSomething = True
# termination criteria from opencv example code: 
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

objpoints = []
imgpoints = []

#gray_img = []

#Get an image
camera = cv2.VideoCapture(0) #Select the camera to use, 0=built in webcam
return_val, camera_img = camera.read()
camera_img = cv2.flip(camera_img, 1)

gray_img = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)
ret_val, corners = cv2.findChessboardCorners(gray_img, (9,6), None)

if ret_val == True:
    objpoints.append(objp)
    chessboard_corners = cv2.cornerSubPix(gray_img, corners, (11,11), (-1,-1), criteria)
    imgpoints.append(chessboard_corners)
    output_img = cv2.drawChessboardCorners(camera_img, (9,6), chessboard_corners, ret_val)
    
    print("Press Enter to save the calibration data or Esc to exit without saving")

    while(True):
        cv2.imshow('Chessboard', output_img)
        if cv2.waitKey(1) == 13:
            break
        elif cv2.waitKey(1) == 27:
            doSomething = False
            break
        #END IF
    #END WHILE
    if doSomething == True:        
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray_img.shape[::-1], None, None)
        #Create a JSON object
        calibration_data = {}
        calibration_data['mtx'] = mtx.tolist()
        calibration_data['dist'] = dist.tolist()

        #Filename to save object to
        filename = 'camera_calibration_data.json'

        #Save JSON object to file
        with open(filename, 'w') as output_file:
            json.dump(calibration_data, output_file)
            print('Calibration saved to ' + filename)
        #END WITH
    #END IF
#END IF  


cv2.destroyAllWindows()  


#Load JSON
with open(filename, 'r') as camera_calibration_file:
    camera_calibration_file_data = json.load(camera_calibration_file)
    camera_mtx = np.array(camera_calibration_file_data['mtx'])
    camera_dist = np.array(camera_calibration_file_data['dist'])
    print(camera_mtx)