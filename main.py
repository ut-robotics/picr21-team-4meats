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
    camera.get_keypoints()
    manual_movement()


def handleFind():
    center_ball(camera.find_best_ball(camera.get_keypoints()))


def handleDrive():
    follow_ball(camera.find_best_ball(camera.get_keypoints()))


switcher = {
    State.MANUAL: handleManual,
    State.FIND: handleFind,
    State.DRIVE: handleDrive
}

manualControlEnabled = True
state = State.MANUAL

while True:

    manualControlEnabled = control_state_manual(manualControlEnabled)
    if manualControlEnabled:
        state = State.MANUAL
    else:
        state = state.FIND

    switcher.get(state)()

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

camera.quit_camera()
