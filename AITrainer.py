import cv2 
import numpy as np
import time
import PoseModule as pm
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

path = "./videos"
img = cv2.imread('riley.jpg')
detector = pm.poseDetector()


onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
print(onlyfiles)
all_angles_list = []

def play_video(cap,right_angle_list = [], left_angle_list = []):
    right_angle_list = []
    left_angle_list = []
    while True:
        success, img = cap.read()
        # img = cv2.imread('riley.jpg')
        # img = cv2.resize(img,(720,720))
        if img is None:
            break
                
        img = detector.findPose(img,False)
        
        lmList = detector.findPosition(img,False)
        #print(lmList)
        if len(lmList) != 0:
            right_angle = round(detector.findAngle(img,12,14,16), 2) #right arm
            left_angle = round(detector.findAngle(img,11,13,15), 2) #left arm
        
        right_angle_list.append(right_angle)
        left_angle_list.append(left_angle)


        cv2.imshow('Image',img)
        cv2.waitKey(1)


    return right_angle_list,left_angle_list

## TODO: plot the angle/frame of the video

# Play all the videos to get angles
for files in onlyfiles:
    print(files)
    cap = cv2.VideoCapture(f'videos/{files}')
    right_angles_list, left_angles_list = play_video(cap)
    all_angles_list.append(right_angles_list)
    all_angles_list.append(left_angles_list)
    
# Even numbers are 
for i in range(len(all_angles_list)):
    print(len(all_angles_list[i]))

def plot_graph(right_angle_list,left_angle_list):
    right_angle_array = np.array(right_angle_list)
    left_angle_array = np.array(left_angle_list)
    x_array = np.arange(start=0, stop=right_angle_array.size)
    plt.scatter(np.arange(start=0, stop=right_angle_array.size),right_angle_array,c='r',label='right arm')
    plt.scatter(np.arange(start=0, stop=left_angle_array.size),left_angle_array,c='b',label='left arm')
    plt.xlabel("Frames")
    plt.ylabel("Angle")
    plt.legend()
    plt.show()

def plot_all_graphs(all_angles_list):
    for i in range(1,len(all_angles_list),2):
        plt.subplot(2,len(all_angles_list),i)
        plt.scatter(np.arange(start=0, stop=len(all_angles_list[i-1])),np.array(all_angles_list[i-1]),c='r',label='right arm')
        plt.scatter(np.arange(start=0, stop=len(all_angles_list[i])),np.array(all_angles_list[i]),c='b',label='left arm')
        plt.xlabel('Frame')
        plt.ylabel('Angle')
        plt.legend()
    plt.show()


plot_graph(all_angles_list[2],all_angles_list[3])
plot_all_graphs(all_angles_list)