import numpy as np
import cv2

# termination criteria from opencv example code: 
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

def get_chessboard_points(camera_img, chessboard_size):
    
    gray_img = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray_img, chessboard_size, None)

    if ret == True:
        chessboard_corners = cv2.cornerSubPix(gray_img, corners, (11,11), (-1,-1), criteria)
        output_img = cv2.drawChessboardCorners(camera_img, chessboard_size, chessboard_corners, ret)
        return output_img
    return camera_img



while(True):
    camera = cv2.VideoCapture(0) #Select the camera to use, 0=built in webcam
    return_val, camera_img = camera.read()
    camera_img = cv2.flip(camera_img, 1)
    cv2.imshow('Calibration', get_chessboard_points(camera_img, (9,6)))
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()