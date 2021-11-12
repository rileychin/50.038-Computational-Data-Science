import cv2 
import numpy as np
import time
import PoseModule as pm
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import pandas as pd
import statistics


path = "./videos"
goodpath = "./videos/goodtrain"
badpath = "./videos/badtrain"
badtestpath = "./test/badtest"
goodtestpath = "./test/goodtest"
img = cv2.imread('riley.jpg')
detector = pm.poseDetector()
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
onlygoodfiles = [f for f in listdir(goodpath) if isfile(join(goodpath,f))]
onlybadfiles = [f for f in listdir(badpath) if isfile(join(badpath,f))]
badtestfiles = [f for f in listdir(badtestpath) if isfile(join(badtestpath,f))]
goodtestfiles = [f for f in listdir(goodtestpath) if isfile(join(goodtestpath,f))]

def addAngle(p1, p2, p3):
    item = round(detector.findAngle(img,p1,p2,p3), 2)
    if item:
        return(item)
    else:
        return(0)

def play_video(cap):
    r_arm = []
    l_arm = []
    r_armpit = []
    l_armpit = []
    r_hip = []
    l_hip = []
    while True:
        success, img = cap.read()
        # img = cv2.imread('riley.jpg')
        # img = cv2.resize(img,(720,720))
        if img is None:
            break
                
        img = detector.findPose(img,False)
        
        lmList = detector.findPosition(img,False) #coordinates
        #print(lmList)
        if len(lmList) != 0:
            r_arm.append(round(detector.findAngle(img,12,14,16), 2))
            l_arm.append(round(detector.findAngle(img,11,13,15), 2))
            r_armpit.append(round(detector.findAngle(img,14, 12, 24), 2))
            l_armpit.append(round(detector.findAngle(img,13, 11, 23), 2))
            r_hip.append(round(detector.findAngle(img,12, 24, 26), 2))
            l_hip.append(round(detector.findAngle(img,11, 23, 25), 2))

        cv2.imshow('Image',img)
        cv2.waitKey(1)
    return r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip #length of each of these list = number of frames in video

def get_mean(input_list):
    return statistics.mean(input_list)

def get_variance(input_list):
    return statistics.variance(input_list)


def main():
    file_list = []
    r_arm_mean = []
    r_arm_variance = []
    l_arm_mean = []
    l_arm_variance = []
    r_armpit_mean = []
    r_armpit_variance = []
    l_armpit_mean = []
    l_armpit_variance = []
    r_hip_mean = []
    r_hip_variance = []
    l_hip_mean = []
    l_hip_variance = []
    classification = []
    # Play all the videos to get angles
    # Play all the bad examples to get data
    for file in onlybadfiles:          #for every file, run play_video, get r_arm etc etc
        print(file)
        cap = cv2.VideoCapture(f'videos/badtrain/{file}')
        r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip = play_video(cap) #calls play_video, gets result, for 1 video

        file_list.append(file)
        r_arm_mean.append(get_mean(r_arm))
        r_arm_variance.append(get_variance(r_arm))
        l_arm_mean.append(get_mean(l_arm))
        l_arm_variance.append(get_variance(l_arm))
        r_armpit_mean.append(get_mean(r_armpit))
        r_armpit_variance.append(get_variance(r_armpit))
        l_armpit_mean.append(get_mean(l_armpit))
        l_armpit_variance.append(get_variance(l_armpit))
        r_hip_mean.append(get_mean(r_hip))
        r_hip_variance.append(get_variance(r_hip))
        l_hip_mean.append(get_mean(l_hip))
        l_hip_variance.append(get_variance(l_hip))
        classification.append(0)

    # Play all the good examples to get data
    for file in onlygoodfiles:          #for every file, run play_video, get r_arm etc etc
        print(file)
        cap = cv2.VideoCapture(f'videos/goodtrain/{file}')
        r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip = play_video(cap) #calls play_video, gets result, for 1 video

        file_list.append(file)
        r_arm_mean.append(get_mean(r_arm))
        r_arm_variance.append(get_variance(r_arm))
        l_arm_mean.append(get_mean(l_arm))
        l_arm_variance.append(get_variance(l_arm))
        r_armpit_mean.append(get_mean(r_armpit))
        r_armpit_variance.append(get_variance(r_armpit))
        l_armpit_mean.append(get_mean(l_armpit))
        l_armpit_variance.append(get_variance(l_armpit))
        r_hip_mean.append(get_mean(r_hip))
        r_hip_variance.append(get_variance(r_hip))
        l_hip_mean.append(get_mean(l_hip))
        l_hip_variance.append(get_variance(l_hip))
        classification.append(1)

    data = {'file': file_list, 
    'r_arm_mean':r_arm_mean,'r_arm_variance':r_arm_variance,
    'l_arm_mean':l_arm_mean, 'l_arm_variance':l_arm_variance,
    'r_armpit_mean':r_armpit_mean,'r_armpit_variance':r_armpit_variance,
    'l_armpit_mean':l_armpit_mean,'l_armpit_variance':l_armpit_variance,
    'r_hip_mean':r_hip_mean,'r_hip_variance':r_hip_variance,
    'l_hip_mean':l_hip_mean,'l_hip_variance':l_hip_variance,
    'class': classification}
    
    dataFrame = pd.DataFrame(data)
    print(dataFrame)
    dataFrame.to_csv("csv/mean_variance.csv",index=False)

    file_list = []
    r_arm_mean = []
    r_arm_variance = []
    l_arm_mean = []
    l_arm_variance = []
    r_armpit_mean = []
    r_armpit_variance = []
    l_armpit_mean = []
    l_armpit_variance = []
    r_hip_mean = []
    r_hip_variance = []
    l_hip_mean = []
    l_hip_variance = []
    classification = []

    # Play all test videos to get data
    for file in badtestfiles:          #for every file, run play_video, get r_arm etc etc
        print(file)
        cap = cv2.VideoCapture(f'test/badtest/{file}')
        r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip = play_video(cap) #calls play_video, gets result, for 1 video

        file_list.append(file)
        r_arm_mean.append(get_mean(r_arm))
        r_arm_variance.append(get_variance(r_arm))
        l_arm_mean.append(get_mean(l_arm))
        l_arm_variance.append(get_variance(l_arm))
        r_armpit_mean.append(get_mean(r_armpit))
        r_armpit_variance.append(get_variance(r_armpit))
        l_armpit_mean.append(get_mean(l_armpit))
        l_armpit_variance.append(get_variance(l_armpit))
        r_hip_mean.append(get_mean(r_hip))
        r_hip_variance.append(get_variance(r_hip))
        l_hip_mean.append(get_mean(l_hip))
        l_hip_variance.append(get_variance(l_hip))
        classification.append(0)

    for file in goodtestfiles:          #for every file, run play_video, get r_arm etc etc
        print(file)
        cap = cv2.VideoCapture(f'test/goodtest/{file}')
        r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip = play_video(cap) #calls play_video, gets result, for 1 video

        file_list.append(file)
        r_arm_mean.append(get_mean(r_arm))
        r_arm_variance.append(get_variance(r_arm))
        l_arm_mean.append(get_mean(l_arm))
        l_arm_variance.append(get_variance(l_arm))
        r_armpit_mean.append(get_mean(r_armpit))
        r_armpit_variance.append(get_variance(r_armpit))
        l_armpit_mean.append(get_mean(l_armpit))
        l_armpit_variance.append(get_variance(l_armpit))
        r_hip_mean.append(get_mean(r_hip))
        r_hip_variance.append(get_variance(r_hip))
        l_hip_mean.append(get_mean(l_hip))
        l_hip_variance.append(get_variance(l_hip))
        classification.append(1)

    test_data = {'file': file_list, 
    'r_arm_mean':r_arm_mean,'r_arm_variance':r_arm_variance,
    'l_arm_mean':l_arm_mean, 'l_arm_variance':l_arm_variance,
    'r_armpit_mean':r_armpit_mean,'r_armpit_variance':r_armpit_variance,
    'l_armpit_mean':l_armpit_mean,'l_armpit_variance':l_armpit_variance,
    'r_hip_mean':r_hip_mean,'r_hip_variance':r_hip_variance,
    'l_hip_mean':l_hip_mean,'l_hip_variance':l_hip_variance,
    'class': classification}
    
    dataFrame = pd.DataFrame(test_data)
    print(dataFrame)
    dataFrame.to_csv("csv/mean_variance_test.csv",index=False)

if __name__ == "__main__":
    main()