from time import sleep
from constants import FOOD_SERVO_ANGLE_OPEN as open_angle
from constants import FOOD_SERVO_ANGLE_CLOSED as closed_angle
from constants import FOOD_SERVO_NUMBER as servo_number


# Bowl is refilled w/ one food ratio -> abt. 1.5 seconds
def refill_food_bowl():
    set_servo_angle(open_angle)
    sleep(1.5)
    set_servo_angle(closed_angle)