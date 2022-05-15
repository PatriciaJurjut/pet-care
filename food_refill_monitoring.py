from time import sleep
from datetime import datetime
from datetime import timedelta
from constants import FOOD_SERVO_ANGLE_OPEN as open_angle
from constants import FOOD_SERVO_ANGLE_CLOSED as closed_angle
from constants import FOOD_SERVO_NUMBER as servo_number
from servo import set_servo_angle
from db_connection import update_DB_feeding_parameters
from db_connection import get_last_feeding_time
from db_connection import get_feeding_cycles_number
from db_connection import get_feeding_cycle_length

last_feeding_time = datetime.min # TODO: get it from DB
cycles_number = 3
cycle_length_minutes = 300 # default mode: feeding occurs every 5 hours = 300 mins
upcoming_feeding_time = datetime.min


def feeding_service():
    init_DB_variables()
    current_time = datetime.now()
    print(upcoming_feeding_time)
    if current_time >= upcoming_feeding_time:
        refill_food_bowl()

def init_DB_variables():
    global cycle_length_minutes
    global cycles_number
    global last_feeding_time
    cycles_number = get_feeding_cycles_number()
    cycle_length_minutes = get_feeding_cycle_length()
    print(cycle_length_minutes)
    last_feeding_time = get_last_feeding_time()

# Bowl is refilled w/ one food ratio -> abt. 1.5 seconds
def refill_food_bowl():
    set_servo_angle(open_angle, servo_number)
    sleep(1.5)
    set_servo_angle(closed_angle, servo_number)
    update_feeding_parameters()
    
def update_feeding_parameters():
    global upcoming_feeding_time, last_feeding_time
    last_feeding_time = datetime.now() # TODO: update in DB
    upcoming_feeding_time = last_feeding_time + timedelta(minutes=cycle_length_minutes)
    update_DB_feeding_parameters(last_feeding_time)
    
