from manualControl import *
from automaticControl import *
from camera import *
from enum import Enum

camera = Camera()


class State(Enum):
    MANUAL = 0
    FIND = 1
    CENTER = 2
    DRIVE = 3


def handleManual():
    camera.get_keypoints()
    manual_movement()


def handleFind():
    if camera.find_best_ball(camera.get_keypoints()) is not None:
        state = State.DRIVE
        switcher.get(state)()
    else:
        print("finding")
        find_ball()


def handleCenter():
    center_ball(camera.find_best_ball(camera.get_keypoints()))


def handleDrive():
    follow_ball(camera.find_best_ball(camera.get_keypoints()))


switcher = {
    State.MANUAL: handleManual,
    State.FIND: handleFind,
    State.CENTER: handleCenter,
    State.DRIVE: handleDrive
}

manualControlEnabled = True

while True:

    manualControlEnabled = control_state_manual(manualControlEnabled)
    if manualControlEnabled:
        state = State.MANUAL
    else:
        state = State.FIND

    switcher.get(state)()

    print(state)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

camera.quit_camera()
