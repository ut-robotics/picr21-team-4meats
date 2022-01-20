import os
import pyrealsense2
import cv2
import numpy
import time
import functools

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

cam_width = 848
cam_height = 480
cam_fps = 60

pipeline = pyrealsense2.pipeline()
config = pyrealsense2.config()
config.enable_stream(pyrealsense2.stream.color, cam_width, cam_height, pyrealsense2.format.bgr8, cam_fps)
pipeline_profile = pipeline.start(config)

device = pipeline.get_active_profile().get_device().query_sensors()[1]
device.set_option(pyrealsense2.option.enable_auto_exposure, 0)
device.set_option(pyrealsense2.option.enable_auto_white_balance, 0)
device.set_option(pyrealsense2.option.exposure, 100.0)
device.set_option(pyrealsense2.option.white_balance, 100.0)


def getTrackbarValues(path="./trackbar_defaults.txt"):
    trackbarValues = [125, 125, 125, 255, 255, 255, 5, 75]
    if os.path.isfile(path):
        try:
            file = open(path)
            trackbarValues = []
            for line in file:
                trackbarValues.append(int(line.strip()))
            file.close()
        except:
            pass
    return trackbarValues


def saveTrackbarValues(values, path="./trackbar_defaults.txt"):
    file = open(path, "w+")
    for value in values:
        file.write(str(value) + '\n')
    file.close()


def updateTrackbar(index, value):
    trackbars[index] = value


trackbar_names = ['lH', 'lS', 'lV', 'hH', 'hS', 'hV', "Kernel size", "Sigma"]
trackbar_limits = [255, 255, 255, 255, 255, 255, 50, 200]
cv2.namedWindow("Trackbars")
trackbars = getTrackbarValues()

for index, name in enumerate(trackbar_names):
    cv2.createTrackbar(name, "Trackbars", trackbars[index], trackbar_limits[index],
                       functools.partial(updateTrackbar, index))

while True:

    if n:
        n = False
        clk1 = time.time()

    elif not n:
        n = True
        clk2 = time.time()

    dif = clk2 - clk1

    if dif < 0:
        dif *= -1

    fps = round(1 / dif)

    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    if not color_frame:
        continue
    color_image = numpy.asanyarray(color_frame.get_data())
    input = color_image.copy()
    hsv = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)

    lowerLimits = numpy.array(trackbars[0:3])
    upperLimits = numpy.array(trackbars[3:6])
    x = trackbars[6]

    if x % 2 == 0:
        x += 1

    kernel = numpy.ones((x, x), numpy.uint8)
    blur = cv2.GaussianBlur(hsv, (x, x), trackbars[7])

    thresholded = cv2.bitwise_not(cv2.inRange(blur, lowerLimits, upperLimits))
    output = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)
    keypoints = detector.detect(output)
    output = cv2.drawKeypoints(output, keypoints, numpy.array([]), (0, 0, 255),
                               cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.putText(input, str(fps), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Unprocessed', input)
    cv2.imshow('Processed', output)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

print('closing program')
pipeline.stop()
cv2.destroyAllWindows()
saveTrackbarValues(trackbars)
