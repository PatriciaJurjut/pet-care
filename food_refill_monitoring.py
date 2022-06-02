import time
from time import sleep
from datetime import datetime
from datetime import timedelta
from constants import FOOD_SERVO_ANGLE_OPEN as OPEN_ANGLE
from constants import FOOD_SERVO_ANGLE_CLOSED as CLOSED_ANGLE
from constants import FOOD_SERVO_IDENTIFIER as SERVO_IDENTIFIER
from constants import FOOD_STANDARD_CYCLES_NUMBER as STANDARD_CYCLES_NUMBER
from constants import FOOD_COMPLETE_REFILL_TIME as SECONDS_FOR_COMPLETE_REFILL
from constants import FOOD_QUICK_TREAT_TIME as SECONDS_FOR_TREAT
from constants import FOOD_STANDARD_CYCLE_LENGTH as STANDARD_CYCLE_LENGTH
from servo import set_servo_angle
from db_connection import update_DB_feeding_parameters
from db_connection import get_last_feeding_time
from db_connection import get_feeding_cycles_number
from db_connection import get_feeding_cycle_length
from db_connection import get_manual_feeding_field

cycles_number = STANDARD_CYCLES_NUMBER
cycle_length_minutes = STANDARD_CYCLE_LENGTH  # default mode: feeding occurs every 5 hours = 300 mins
completed_cycles = 0

last_feeding_time: datetime  # TODO: get it from DB
upcoming_feeding_time = datetime.min


def ignore_first_call(fn):
    called = False

    def wrapper(*args, **kwargs):
        nonlocal called
        if called:
            return fn(*args, **kwargs)
        else:
            called = True
            return None

    return wrapper


def feeding_service():
    init_DB_variables()
    print(upcoming_feeding_time)
    if is_manual_feeding_performed():
        refill_bowl_for_treat()

    elif is_feeding_time_now():  # condition for cyclic feeding
        refill_bowl_completely()


def init_DB_variables():
    global cycle_length_minutes
    global cycles_number
    global last_feeding_time
    cycles_number = get_feeding_cycles_number()
    cycle_length_minutes = get_feeding_cycle_length()
    print(cycle_length_minutes)
    last_feeding_time = get_last_feeding_time()
    update_upcoming_feeding_time()
    print(last_feeding_time)


# Bowl is refilled for a treat (small portion) -> abt. 0.5 seconds
def refill_bowl_for_treat():
    set_servo_angle(OPEN_ANGLE, SERVO_IDENTIFIER)
    sleep(SECONDS_FOR_TREAT)
    set_servo_angle(CLOSED_ANGLE, SERVO_IDENTIFIER)


# Bowl is refilled w/ one food ratio -> abt. 1.5 seconds
def refill_bowl_completely():
    set_servo_angle(OPEN_ANGLE, SERVO_IDENTIFIER)
    sleep(SECONDS_FOR_COMPLETE_REFILL)
    set_servo_angle(CLOSED_ANGLE, SERVO_IDENTIFIER)
    update_feeding_parameters()


def update_feeding_parameters():
    global upcoming_feeding_time
    global last_feeding_time
    last_feeding_time = datetime.now()  # TODO: update in DB
    update_upcoming_feeding_time()
    update_DB_feeding_parameters(last_feeding_time)


def update_upcoming_feeding_time():
    global last_feeding_time
    global upcoming_feeding_time
    upcoming_feeding_time = last_feeding_time + timedelta(minutes=int(str(cycle_length_minutes)))


def is_feeding_time_now():
    current_time = datetime.now()
    return current_time >= upcoming_feeding_time != datetime.min


def is_manual_feeding_performed():
    return get_manual_feeding_field()
