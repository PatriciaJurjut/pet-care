from time import sleep
from datetime import datetime
from datetime import timedelta
from constants import FOOD_SERVO_ANGLE_OPEN as open_angle
from constants import FOOD_SERVO_ANGLE_CLOSED as closed_angle
from constants import FOOD_SERVO_NUMBER as servo_number
from constants import FOOD_STANDARD_CYCLES_NUMBER as standard_cycles_number
from constants import FOOD_COMPLETE_REFILL_TIME as seconds_for_complete_refill
from constants import FOOD_QUICK_TREAT_TIME as seconds_for_treat
from constants import FOOD_STANDARD_CYCLE_LENGTH as standard_cycle_length
from servo import set_servo_angle
from db_connection import update_DB_feeding_parameters
from db_connection import get_last_feeding_time
from db_connection import get_feeding_cycles_number
from db_connection import get_feeding_cycle_length
from db_connection import get_manual_feeding_field

cycles_number = standard_cycles_number
cycle_length_minutes = standard_cycle_length # default mode: feeding occurs every 5 hours = 300 mins
completed_cycles = 0

last_feeding_time = datetime.min # TODO: get it from DB
upcoming_feeding_time = datetime.min


def feeding_service():
    current_time = datetime.now()
    init_DB_variables()
    print(upcoming_feeding_time)
    if is_manual_feeding_performed():
        refill_bowl_for_treat()
        
    elif is_feeding_time_now:
        refill_bowl_completely()

def init_DB_variables():
    global cycle_length_minutes
    global cycles_number
    global last_feeding_time
    cycles_number = get_feeding_cycles_number()
    cycle_length_minutes = get_feeding_cycle_length()
    print(cycle_length_minutes)
    last_feeding_time = get_last_feeding_time()

# Bowl is refilled for a treat (small portion) -> abt. 0.5 seconds
def refill_bowl_for_treat():
    set_servo_angle(open_angle, servo_number)
    sleep(seconds_for_treat)
    set_servo_angle(closed_angle, servo_number)

# Bowl is refilled w/ one food ratio -> abt. 1.5 seconds
def refill_bowl_completely():
    set_servo_angle(open_angle, servo_number)
    sleep(seconds_for_complete_refill)
    set_servo_angle(closed_angle, servo_number)
    update_feeding_parameters()
    
def update_feeding_parameters():
    global upcoming_feeding_time
    global last_feeding_time
    last_feeding_time = datetime.now() # TODO: update in DB
    upcoming_feeding_time = last_feeding_time + timedelta(minutes=cycle_length_minutes)
    update_DB_feeding_parameters(last_feeding_time)
    upcoming_feeding_time = last_feeding_time + timedelta(cycle_length_minutes)
    
def is_feeding_time_now():
    return current_time >= upcoming_feeding_time

def is_manual_feeding_performed():
    return get_manual_feeding_field()
    
