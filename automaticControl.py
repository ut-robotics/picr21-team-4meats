from motionControl import *

oldSelectedPoint = [0, 0, 0]
selectedPoint = [0, 0, 0]
lostCounter = 0


def find_best_ball(keypoints):
    global oldSelectedPoint, selectedPoint, lostCounter
    if len(keypoints) == 0:
        move_robot_XY(0, 0, 10, 0)

    if len(keypoints) != 0:
        keypoints = sorted(keypoints, key=lambda x: x[2])
        for point in keypoints:
            if point[2] != 0:
                if abs(point[0] - oldSelectedPoint[0]) < 50 and abs(point[1] - oldSelectedPoint[1]) < 50 and \
                        oldSelectedPoint[0] != 0 and oldSelectedPoint[1] != 0:
                    selectedPoint = point
                    break
                elif (oldSelectedPoint[0] == 0 and oldSelectedPoint[1] == 0) or lostCounter >= 10:
                    lostCounter = 0
                    selectedPoint = point
                    break
                else:
                    lostCounter += 1

        print(lostCounter)
        oldSelectedPoint = selectedPoint
        return selectedPoint


def center_ball(point):
    print(point)
    if point is not None:
        maxSpeedR = 60
        ballErrorR = point[0] - 424
        normalizedBallErrorR = ballErrorR / 848
        rotationSpeed = normalizedBallErrorR * maxSpeedR
        move_robot_XY(0, 0, -rotationSpeed, 0)


def follow_ball(point):
    print(point)
    if point is not None:
        maxSpeedR = 60
        ballErrorR = point[0] - 424
        normalizedBallErrorR = ballErrorR / 848
        rotationSpeed = normalizedBallErrorR * maxSpeedR
        maxSpeedF = 60
        ballErrorF = point[2] - 370
        normalizedBallErrorF = ballErrorF / 1000
        movementSpeed = normalizedBallErrorF * maxSpeedF
        move_robot_XY(0, -movementSpeed, -rotationSpeed, 0)
