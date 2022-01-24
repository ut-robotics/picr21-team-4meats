from camera import *
from manualControl import *
from automaticControl import *

initialize_camera()
controlState = False
prevControlState = False

while True:

    controlState = control_state_manual(prevControlState)
    if controlState:
        manual_movement()
    prevControlState = controlState

    if not controlState:
        # center_ball(find_best_ball(get_keypoints()))
        follow_ball(find_best_ball(get_keypoints()))

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

quit_camera()
