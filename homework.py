import cv2
import numpy as np
import time

# start webcam and wait one second
video = cv2.VideoCapture(0)
time.sleep(1)

background = 0
count = 0

# capture background 
for i in range(60):
    return_val, background = video.read()
    if return_val == False:
        continue
background = np.flip(background, axis=1)

# read camera frames
while(video.isOpened()):
    return_val, image = video.read()
    if return_val == False:
        break

    count = count + 1

    # mirror image across y axis because x axis is 0 and convert to HSV
    image = np.flip(image, axis=1)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # detect green color using HSV range (this is what becomes invisible)
    lower_red = np.array([35,40,40])
    upper_red = np.array([85,255,255])

    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask1 = mask1 + mask2

    
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3,3),np.uint8), iterations=1)

    # invert mask (everything that is NOT green)
    mask2 = cv2.bitwise_not(mask1)

    # replace green parts with background, keep rest normal
    res1 = cv2.bitwise_and(background, background, mask=mask1)
    res2 = cv2.bitwise_and(image, image, mask=mask2)

    # combine both to create invisibility effect
    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("Invisible Man", finalOutput)

    k = cv2.waitKey(10)
    if k == 27:
        break