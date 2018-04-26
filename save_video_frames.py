import sys
import numpy as np
import cv2

video_file = sys.argv[1]

if video_file == 0:
    video_file = int(video_file)

cap = cv2.VideoCapture(video_file)

vid_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

for i in range(vid_length):
    ret, frame = cap.read()

    frame = cv2.flip(frame,1)
    cv2.imshow("Img", frame)
    cv2.imwrite(str(i) + ".jpg", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()