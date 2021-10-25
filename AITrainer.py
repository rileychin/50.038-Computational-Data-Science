import cv2 
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture('videsos/IMG_5905.MOV')
img = cv2.imread('riley.jpg')
detector = pm.poseDetector()

while True:
    success, img = cap.read()
    # img = cv2.imread('riley.jpg')
    # img = cv2.resize(img,(720,720))
    img = detector.findPose(img,False)

    lmList = detector.findPosition(img,False)
    #print(lmList)

    if len(lmList) != 0:
        detector.findAngle(img,12,14,16)
        detector.findAngle(img,11,13,15)


    cv2.imshow('Image',img)
    cv2.waitKey(1)



## TODO: plot the angle/frame of the video