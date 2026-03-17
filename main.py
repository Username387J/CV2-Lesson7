import cv2
import numpy as np
import time


video=cv2.VideoCapture(0)
#wait function
time.sleep(1)

background=0
# number o fram counts
count=0

#capturing background frame
for i in range (60):
    return_val,background=video.read()
    if return_val == False:
        #restart for i in range loop
        continue
background=np.flip(background,axis=1)

#Capturing video for Output
while(video.isOpened()):
    return_val,image=video.read()
    if return_val == False:
        break
    count=count+1
    image=np.flip(image,axis=1)
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    #mask1
    lower_red=np.array([100,40,40])
    upper_red=np.array([100,255,255])

    mask1=cv2.inRange(hsv,lower_red,upper_red)

    #mask2
    lower_red=np.array([155,40,40])
    upper_red=np.array([150,255,255])

    mask2=cv2.inRange(hsv,lower_red,upper_red)
    mask1=mask1+mask2

    #defining the raw image

    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2)
    mask1=cv2.dilate(mask1,np.ones((3,3),np.uint8),iterations=1)
    mask2=cv2.bitwise_not(mask1)
    
    #masking process
    res1=cv2.bitwise_and(background,background,mask=mask1)
    res2=cv2.bitwise_and(image,image,mask=mask2)
    finalOutput=cv2.addWeighted(res1,1,res2,1,0)
    cv2.imshow("Invisible Man",finalOutput)

    k=cv2.waitKey(10)

    if k==27:
        break

    

