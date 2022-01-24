from camera import *
from manualControl import *
from automaticControl import *
from enum import Enum

camera = Camera()


class State(Enum):
    MANUAL = 0
    FIND = 1
    DRIVE = 2
    AIM = 3
    THROW = 4


def handleManual():
    manual_movement()


def handleFind():
    center_ball(camera.find_best_ball(camera.get_keypoints()))
    print("camera")


def handleDrive():
    follow_ball(camera.find_best_ball(camera.get_keypoints()))


switcher = {
    State.MANUAL: handleManual,
    State.FIND: handleFind,
    State.DRIVE: handleDrive
}

manualControlEnabled = False
state = State.MANUAL

while True:

    manualControlEnabled = control_state_manual(manualControlEnabled)
    if manualControlEnabled:
        state = State.MANUAL
        print("manual")
    else:
        state = state.FIND
        print("find")

    switcher.get(state)()

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

camera.quit_camera()
