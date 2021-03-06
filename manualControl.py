from motionControl import move_robot_XY
import pygame

pygame.init()
joysticks = []
clock = pygame.time.Clock()


def map(x, in_min, in_max, out_min, out_max, dead_min, dead_max):
    output = int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    if output not in range(dead_min, dead_max):
        return output
    else:
        return 0


for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    print("Detected joystick "), joysticks[-1].get_name(), "'"


def manual_movement():
    clock.tick(60)
    event = pygame.event.get()
    speed_x, speed_y, angular_speed = [map(joysticks[4].get_axis(i), -1, 1, -100, 100, -10, 10) for i in (0, 1, 3)]
    thrower_speed = map(joysticks[4].get_axis(6), 0, 1, 0, 2047, -2048, 10)
    print(str(speed_x) + " " + str(speed_y) + " " + str(angular_speed) + " " + str(thrower_speed))
    move_robot_XY(speed_x, speed_y, 0 - angular_speed, thrower_speed, failsafe=0)


def control_state_manual(prevState):
    event = pygame.event.get()
    if prevState == True and joysticks[4].get_button(0) == 1:
        return False
    elif prevState == False and joysticks[4].get_button(1) == 1:
        return True
    else:
        return prevState
