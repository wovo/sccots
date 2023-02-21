# https://raspberrypi.stackexchange.com/questions/114035/picamera-and-ubuntu-20-04-arm64

import os
import cv2
import time

# open camera
if os.name == 'nt':
   cap = cv2.VideoCapture( 0 )
else:   
   cap = cv2.VideoCapture( "/dev/video0", cv2.CAP_V4L )

# set dimensions
cap.set( cv2.CAP_PROP_FRAME_WIDTH, 2560 )
cap.set( cv2.CAP_PROP_FRAME_HEIGHT, 1440 )

# take frame
n = 0
while True:
    ret, frame = cap.read()
    cv2.imwrite( "image.jpg", frame)
    n += 1
    print( "frame %d" % n )
    time.sleep( 1.0 )

# show in window
# doens't work within docker
if 0:
 while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

# release camera
cap.release()
