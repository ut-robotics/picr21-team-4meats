import pyrealsense2 as rs
import numpy as np
import cv2
from time import *
import os

pipeline = rs.pipeline()
config = rs.config()
colorizer = rs.colorizer()
colorizer.set_option(rs.option.visual_preset, 2)

cam_res_width = 848
cam_res_height = 480
cam_fps = 60

# config.enable_stream(rs.stream.depth, cam_res_width, cam_res_height, rs.format.z16, cam_fps)
config.enable_stream(rs.stream.color, cam_res_width, cam_res_height, rs.format.bgr8, cam_fps)

pipeline_profile = pipeline.start(config)

device = pipeline.get_active_profile().get_device().query_sensors()[1]
device.set_option(rs.option.enable_auto_exposure, 0)
device.set_option(rs.option.enable_auto_white_balance, 0)
device.set_option(rs.option.exposure, 100.0)
device.set_option(rs.option.white_balance, 50.0)

while True:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    if not color_frame:
        continue
    color_image = np.asanyarray(color_frame.get_data())
    outimage = color_image.copy()
    cv2.imshow('cap', outimage)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

print('closing program')
pipeline.stop()
cv2.destroyAllWindows()
