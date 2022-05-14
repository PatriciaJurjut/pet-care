from time import sleep
from datetime import datetime
from datetime import timedelta
from constants import FOOD_SERVO_ANGLE_OPEN as open_angle
from constants import FOOD_SERVO_ANGLE_CLOSED as closed_angle
from constants import FOOD_SERVO_NUMBER as servo_number
from servo import set_servo_angle

last_feeding_time = datetime.min
cycle_length_minutes = 300 # default mode: feeding occurs every 5 hours = 300 mins
upcoming_feeding_time = datetime.min


def feeding_service():
    current_time = datetime.now()
    print(upcoming_feeding_time)
    if current_time >= upcoming_feeding_time:
        refill_food_bowl()


# Bowl is refilled w/ one food ratio -> abt. 1.5 seconds
def refill_food_bowl():
    set_servo_angle(open_angle, servo_number)
    sleep(1.5)
    set_servo_angle(closed_angle, servo_number)
    update_feeding_parameters()
    
def update_feeding_parameters():
    global upcoming_feeding_time, last_feeding_time
    last_feeding_time = datetime.now()
    upcoming_feeding_time = last_feeding_time + timedelta(cycle_length_minutes)
    
