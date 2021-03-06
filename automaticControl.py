from motionControl import *


def find_ball():
    move_robot_XY(0, 0, 5, 0)


def center_ball(point):
    print(point)
    if point is not None:
        maxSpeedR = 30
        ballErrorR = point[0] - 424
        normalizedBallErrorR = ballErrorR / 848
        rotationSpeed = normalizedBallErrorR * maxSpeedR
        move_robot_XY(0, 0, -rotationSpeed, 0)


def follow_ball(point):
    print(point)
    if point is not None:
        maxSpeedR = 30
        ballErrorR = point[0] - 424
        normalizedBallErrorR = ballErrorR / 848
        rotationSpeed = normalizedBallErrorR * maxSpeedR
        maxSpeedF = 50
        ballErrorF = point[2] - 300
        normalizedBallErrorF = ballErrorF / 1000
        movementSpeed = normalizedBallErrorF * maxSpeedF
        move_robot_XY(0, -movementSpeed, -rotationSpeed, 0)
