import serial
import struct
import math

s = serial.Serial("/dev/ttyACM0", baudrate=115200)

WHEEL_ANGLES = [math.radians(angle) for angle in [-120, 0, 120]]


def calculate_speed(wheel_angle, moving_direction, speed, angular_speed):
    return int(round(math.cos(moving_direction + wheel_angle) * speed + angular_speed))


def move_robot(moving_direction=0, speed=0, angular_speed=0, thrower_speed=0, failsafe=0):
    speed1, speed2, speed3 = [calculate_speed(angle, moving_direction, speed, angular_speed) for angle in
                              WHEEL_ANGLES]
    send_data = struct.pack("<hhhHBH", speed1, speed2, speed3, thrower_speed, failsafe, 0xAAAA)
    s.write(send_data)


def move_robot_XY(speed_x=0, speed_y=0, angular_speed=0, thrower_speed=0, failsafe=0):
    moving_direction = math.atan2(speed_y, speed_x)
    speed = math.hypot(speed_x, speed_y)
    move_robot(moving_direction, speed, angular_speed, thrower_speed, failsafe=failsafe)
