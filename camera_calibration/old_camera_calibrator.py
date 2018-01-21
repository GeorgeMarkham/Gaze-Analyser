import numpy as np
import cv2

# termination criteria from opencv example code: 
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

def get_chessboard_points(camera_img, chessboard_size): #returns imgpoints, objpoints
    
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    objpoints = []
    imgpoints = []

    gray_img = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray_img, chessboard_size, None)

    if ret == True:
        objpoints.append(objp)
        chessboard_corners = cv2.cornerSubPix(gray_img, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(chessboard_corners)

        return (imgpoints, objpoints)
    return (imgpoints, objpoints)



def get_camera_calibration(objpoints, imgpoints, gray_image): #returns ret, mtx, dist, rvecs, tvecs
    return cv2.calibrateCamera(objpoints, imgpoints, gray_image.shape[::-1], None, None)



def get_optimal_camera_matrix(matrix, distortion, img): #returns optimal_camera_matrix, roi (region of interest)
    height, width = img.shape[:2]
    optimal_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(matrix, distortion, (width, height), 1, (width, height))
    return (optimal_camera_matrix, roi)


def get_undistorted_image(img, matrix, distortion, optimal_camera_matrix, roi): #returns an image called dst
    dst = cv2.undistort(img, matrix, distortion, None, optimal_camera_matrix)

    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    return dst



#Get an image
camera = cv2.VideoCapture(0) #Select the camera to use, 0=built in webcam
return_val, camera_img = camera.read()
camera_img = cv2.flip(camera_img, 1)
camera_img_gray = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)

imgpoints, objpoints = get_chessboard_points(camera_img, (9,6))

if len(imgpoints) > 0 and len(objpoints) > 0:
    ret, matrix, distortion, rvecs, tvecs = get_camera_calibration(imgpoints, objpoints, camera_img_gray)
    optimal_camera_matrix, roi = get_optimal_camera_matrix(matrix, distortion, camera_img)
    
    #get new image
    cv2.waitKey(5000)
    return_val, camera_img_new = camera.read()
    camera_img_new = cv2.flip(camera_img, 1)

    undistorted_img = get_undistorted_image(camera_img_new, matrix, distortion, optimal_camera_matrix, roi)
    cv2.imshow(undistorted_img)