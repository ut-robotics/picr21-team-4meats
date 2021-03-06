import os
import pyrealsense2
import cv2
import numpy
import time
import functools


class Camera():
    def __init__(self):
        self.n = True
        self.clk1 = 0.0
        self.clk2 = 0.0

        self.oldSelectedPoint = [0, 0, 0]
        self.selectedPoint = [0, 0, 0]

        blobparams = cv2.SimpleBlobDetector_Params()
        blobparams.filterByArea = True
        blobparams.minArea = 100
        blobparams.maxArea = 20000
        blobparams.filterByCircularity = False
        blobparams.minDistBetweenBlobs = 100
        blobparams.filterByInertia = False
        blobparams.filterByConvexity = False

        self.detector = cv2.SimpleBlobDetector_create(blobparams)

        cam_width = 848
        cam_height = 480
        cam_fps = 60

        self.pipeline = pyrealsense2.pipeline()
        config = pyrealsense2.config()
        config.enable_stream(pyrealsense2.stream.depth, cam_width, cam_height, pyrealsense2.format.z16, cam_fps)
        config.enable_stream(pyrealsense2.stream.color, cam_width, cam_height, pyrealsense2.format.bgr8, cam_fps)
        self.pipeline.start(config)

        device = self.pipeline.get_active_profile().get_device().query_sensors()[1]
        device.set_option(pyrealsense2.option.enable_auto_exposure, 0)
        device.set_option(pyrealsense2.option.enable_auto_white_balance, 0)
        device.set_option(pyrealsense2.option.exposure, 100.0)
        device.set_option(pyrealsense2.option.white_balance, 100.0)

        align_to = pyrealsense2.stream.color
        self.align = pyrealsense2.align(align_to)

        self.trackbar_names = ['lH', 'lS', 'lV', 'hH', 'hS', 'hV', "Kernel size", "Sigma"]
        self.trackbar_limits = [255, 255, 255, 255, 255, 255, 50, 200]
        cv2.namedWindow("Trackbars")
        self.trackbars = self.getTrackbarValues()

        for index, name in enumerate(self.trackbar_names):
            cv2.createTrackbar(name, "Trackbars", self.trackbars[index], self.trackbar_limits[index],
                               functools.partial(self.updateTrackbar, index))

    def get_keypoints(self):
        if self.n:
            self.n = False
            self.clk1 = time.time()

        elif not self.n:
            self.n = True
            self.clk2 = time.time()

        dif = self.clk2 - self.clk1

        if dif < 0:
            dif *= -1

        fps = round(1 / dif)

        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not color_frame or depth_frame:
            pass
        color_image = numpy.asanyarray(color_frame.get_data())
        input = color_image.copy()
        hsv = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)

        lowerLimits = numpy.array(self.trackbars[0:3])
        upperLimits = numpy.array(self.trackbars[3:6])
        x = self.trackbars[6]

        if x % 2 == 0:
            x += 1

        kernel = numpy.ones((x, x), numpy.uint8)
        blur = cv2.GaussianBlur(hsv, (x, x), self.trackbars[7])

        thresholded = cv2.bitwise_not(cv2.inRange(blur, lowerLimits, upperLimits))

        output = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)
        keypoints = self.detector.detect(output)
        output = cv2.drawKeypoints(output, keypoints, numpy.array([]), (0, 0, 255),
                                   cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        points = []

        if len(keypoints) != 0:
            for elem in keypoints:
                point_depth = int(depth_frame.get_distance(round(elem.pt[0]), round(elem.pt[1])) * 1000)
                cv2.putText(output, str(round(elem.pt[0])) + " " + str(round(elem.pt[1])),
                            (round(elem.pt[0]), round(elem.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                cv2.putText(output, str(point_depth),
                            (round(elem.pt[0]), round(elem.pt[1]) - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

                points.append([round(elem.pt[0]), round(elem.pt[1]), point_depth])

        cv2.putText(input, str(fps), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Unprocessed', input)
        cv2.imshow('Processed', output)

        return points

    def quit_camera(self):
        print('closing program')
        self.pipeline.stop()
        cv2.destroyAllWindows()
        self.saveTrackbarValues(self.trackbars)

    def getTrackbarValues(self, path="./trackbar_defaults.txt"):
        trackbarValues = [15, 14, 58, 89, 163, 164, 3, 0]
        if os.path.isfile(path):
            try:
                with open(path) as file:
                    trackbarValues = []
                    for line in file:
                        trackbarValues.append(int(line.strip()))
            except:
                pass

        return trackbarValues

    def saveTrackbarValues(self, values, path="./trackbar_defaults.txt"):
        with open(path, "w+") as file:
            for value in values:
                file.write(str(value) + '\n')

    def updateTrackbar(self, index, value):
        self.trackbars[index] = value

    def find_best_ball(self, keypoints):

        if len(keypoints) != 0:
            keypoints = sorted(keypoints, key=lambda x: x[2])
            for point in keypoints:
                if point[2] != 0:
                    self.selectedPoint = point
                    break

            print(self.selectedPoint)
            print(self.oldSelectedPoint)
            print(keypoints)
            self.oldSelectedPoint = self.selectedPoint
            return self.selectedPoint
