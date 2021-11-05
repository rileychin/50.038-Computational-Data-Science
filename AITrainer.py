import cv2 
import numpy as np
import time
import PoseModule as pm
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import pandas as pd

path = "./videos"
img = cv2.imread('riley.jpg')
detector = pm.poseDetector()
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

# r_arm = []
# l_arm = []
# r_armpit = []
# l_armpit = []
# r_hip = []
# l_hip = []
all_angles_list = []

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

# Play all the videos to get angles

for file in onlyfiles:          #for every file, run play_video, get r_arm etc etc
    print(file)
    cap = cv2.VideoCapture(f'videos/{file}')
    r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip = play_video(cap) #calls play_video, gets result, for 1 video
    # r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip = clean(r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip)
    all_angles_list.append([r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip]) #
    print (len(all_angles_list[0]))
    print (all_angles_list[0])

    all_angles_dic = {'r_arm': r_arm, 'l_arm' : l_arm, 'r_armpit': r_armpit ,'l_armpit':l_armpit , 'r_hip' : r_hip , 'l_hip' : l_hip}
    data = pd.DataFrame(all_angles_dic)
    data.to_csv("csv/" + file + ".csv")

def plot_all_graphs(all_angles_list):
    for i in range(len(all_angles_list)):
        plt.subplot(2, np.ceil(len(all_angles_list)/2) , i+1)
        plt.scatter(np.arange(start=0, stop=len(all_angles_list[i][0])),np.array(all_angles_list[i][0]),c='red',label='right arm')
        plt.scatter(np.arange(start=0, stop=len(all_angles_list[i][1])),np.array(all_angles_list[i][1]),c='blue',label='left arm')
        plt.scatter(np.arange(start=0, stop=len(all_angles_list[i][2])),np.array(all_angles_list[i][2]),c='green',label='right armpit')
        plt.scatter(np.arange(start=0, stop=len(all_angles_list[i][3])),np.array(all_angles_list[i][3]),c='yellow',label='left armpit')
        plt.scatter(np.arange(start=0, stop=len(all_angles_list[i][4])),np.array(all_angles_list[i][4]),c='purple',label='right hip')
        plt.scatter(np.arange(start=0, stop=len(all_angles_list[i][5])),np.array(all_angles_list[i][5]),c='brown',label='left hip')
        plt.title(onlyfiles[i])
        plt.xlabel('Frame')
        plt.ylabel('Angle')
        plt.legend()
    plt.show()

# plot_graph(all_angles_list[2],all_angles_list[3])
plot_all_graphs(all_angles_list)