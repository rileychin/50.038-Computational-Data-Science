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
        
        lmList = detector.findPosition(img,False)
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
    return r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip


# def clean(l1, l2, l3, l4, l5, l6):
#     # right = (max(l1)>max(l2))
#     # left = (max(l2)>max(l1))
#     # if right:
#     pop = []
#     l1new=[]
#     l2new=[]
#     l3new=[]
#     l4new=[]
#     l5new=[]
#     l6new=[]
#     for i in range(len(l1)):
#         if l1[i] < 160:
#             l1new.append(l1[i])
#             l2new.append(l2[i])
#             l3new.append(l3[i])
#             l4new.append(l4[i])
#             l5new.append(l5[i])
#             l6new.append(l6[i])
#     return l1new, l2new ,l3new,l4new,l5new,l6new



# Play all the videos to get angles
for file in onlyfiles:
    print(file)
    cap = cv2.VideoCapture(f'videos/{file}')
    r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip = play_video(cap)
    # r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip = clean(r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip)
    all_angles_list.append([r_arm, l_arm, r_armpit, l_armpit, r_hip, l_hip])



# for i in range(len(all_angles_list)):
#     for j in range(6):
#         print(len(all_angles_list[i][j]))

# def plot_graph(right_angle_list,left_angle_list):
#     right_angle_array = np.array(right_angle_list)
#     left_angle_array = np.array(left_angle_list)
#     x_array = np.arange(start=0, stop=right_angle_array.size)
#     plt.scatter(np.arange(start=0, stop=right_angle_array.size),right_angle_array,c='r',label='right arm')
#     plt.scatter(np.arange(start=0, stop=left_angle_array.size),left_angle_array,c='b',label='left arm')
#     plt.xlabel("Frames")
#     plt.ylabel("Angle")
#     plt.legend()
#     plt.show()

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