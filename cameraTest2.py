import numpy as np
import cv2
from time import *
import os

cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(4)

if not os.path.isfile("./trackbar_defaults.txt"):

    trackbar_value1 = 125
    trackbar_value2 = 125
    trackbar_value3 = 125
    trackbar_value4 = 255
    trackbar_value5 = 255
    trackbar_value6 = 255
    trackbar_value7 = 5
    trackbar_value8 = 75

else:
    try:
        file = open("trackbar_defaults.txt")
        trackbar_value1 = int(file.readline().strip())
        trackbar_value2 = int(file.readline().strip())
        trackbar_value3 = int(file.readline().strip())
        trackbar_value4 = int(file.readline().strip())
        trackbar_value5 = int(file.readline().strip())
        trackbar_value6 = int(file.readline().strip())
        trackbar_value7 = int(file.readline().strip())
        trackbar_value8 = int(file.readline().strip())
        file.close()
    except:
        trackbar_value1 = 125
        trackbar_value2 = 125
        trackbar_value3 = 125
        trackbar_value4 = 255
        trackbar_value5 = 255
        trackbar_value6 = 255
        trackbar_value7 = 5
        trackbar_value8 = 75

n = True
clk1 = 0.0
clk2 = 0.0

blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByArea = True
blobparams.minArea = 100
blobparams.maxArea = 20000
blobparams.filterByCircularity = False
blobparams.minDistBetweenBlobs = 200
blobparams.filterByInertia = False
blobparams.filterByConvexity = False

detector = cv2.SimpleBlobDetector_create(blobparams)


def updateValue1(new_value):
    global trackbar_value1
    trackbar_value1 = new_value
    return


def updateValue2(new_value):
    global trackbar_value2
    trackbar_value2 = new_value
    return


def updateValue3(new_value):
    global trackbar_value3
    trackbar_value3 = new_value
    return


def updateValue4(new_value):
    global trackbar_value4
    trackbar_value4 = new_value
    return


def updateValue5(new_value):
    global trackbar_value5
    trackbar_value5 = new_value
    return


def updateValue6(new_value):
    global trackbar_value6
    trackbar_value6 = new_value
    return


def updateValue7(new_value):
    global trackbar_value7
    trackbar_value7 = new_value
    return


def updateValue8(new_value):
    global trackbar_value8
    trackbar_value8 = new_value
    return


cv2.createTrackbar("lH", "Original", trackbar_value1, 255, updateValue1)
cv2.createTrackbar("lS", "Original", trackbar_value2, 255, updateValue2)
cv2.createTrackbar("lV", "Original", trackbar_value3, 255, updateValue3)
cv2.createTrackbar("hH", "Original", trackbar_value4, 255, updateValue4)
cv2.createTrackbar("hS", "Original", trackbar_value5, 255, updateValue5)
cv2.createTrackbar("hV", "Original", trackbar_value6, 255, updateValue6)
cv2.createTrackbar("Kernel size", "Original", trackbar_value7, 50, updateValue7)
cv2.createTrackbar("Sigma", "Original", trackbar_value8, 200, updateValue8)

while True:

    if n:
        n = False
        clk1 = time()

    elif not n:
        n = True
        clk2 = time()

    dif = clk2 - clk1

    if dif < 0:
        dif *= -1

    fps = round(1 / dif)

    ret, org = cap.read()
    r = [len(org) - 220, len(org) - 20, 0, len(org[0])]
    frame = org[r[0]:r[1], r[2]:r[3]]
    bgr = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lH = trackbar_value1
    lS = trackbar_value2
    lV = trackbar_value3
    hH = trackbar_value4
    hS = trackbar_value5
    hV = trackbar_value6
    lowerLimits = np.array([lH, lS, lV])
    upperLimits = np.array([hH, hS, hV])

    x = trackbar_value7

    if x % 2 == 0:
        x += 1

    kernel = np.ones((x, x), np.uint8)

    blur = cv2.GaussianBlur(bgr, (x, x), trackbar_value8)
    thresholded = cv2.bitwise_not(cv2.inRange(blur, lowerLimits, upperLimits))

    opening = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)

    keypoints = detector.detect(opening)
    frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.putText(frame, str(fps), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Processed', opening)
    cv2.imshow('Original', frame)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

print('closing program')
cap.release()
cv2.destroyAllWindows()

file = open("trackbar_defaults.txt", "w+")
file.write(str(trackbar_value1) + "\n" + str(trackbar_value2) + "\n" + str(trackbar_value3) + "\n" + str(
    trackbar_value4) + "\n" + str(trackbar_value5) + "\n" + str(trackbar_value6) + "\n" + str(
    trackbar_value7) + "\n" + str(trackbar_value8))
file.close()
