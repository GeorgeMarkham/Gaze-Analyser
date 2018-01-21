
#Get a new image after 2.5 secs
#print("Press tab to take a new picture!")
#while(True):
#    cv2.imshow('Calibration image', cv2.drawChessboardCorners(camera_img, (9,6), chessboard_corners, ret_val))
#    if cv2.waitKey(1) == 9:
#        return_val, camera_img = camera.read()
#        camera_img_new = cv2.flip(camera_img, 1)
#        
#        height, width = camera_img_new.shape[:2]
#        optimal_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))
#        dst = cv2.undistort(camera_img_new, mtx, dist, None, optimal_camera_matrix)
#        x,y,w,h = roi
#        dst = dst[y:y+h, x:x+w]
#        #cv2.imshow('calibresult',dst)
#    if cv2.waitKey(1) == 27:
#        break
#cv2.destroyAllWindows()