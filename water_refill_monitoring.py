from time import sleep
import smbus
from datetime import datetime
from utils import current_time_milliseconds
from constants import WATER_I2C_ADDRESS as I2C_ADDRESS
from constants import WATER_SENSOR_ANALOG_PIN_INPUT as ANALOG_PIN_INPUT
from constants import WATER_SERVO_IDENTIFIER as SERVO_IDENTIFIER
from constants import WATER_SERVO_ANGLE_OPEN as OPEN_ANGLE
from constants import WATER_SERVO_ANGLE_CLOSED as CLOSED_ANGLE
from constants import WATER_LEVEL_LOWER_THRESHOLD as LOWER_THRESHOLD
from constants import WATER_LEVEL_UPPER_THRESHOLD as UPPER_THRESHOLD
from constants import WATER_REFILL_STOP_TIME as REFILL_STOP_TIME
from servo import set_servo_angle
from db_connection import update_DB_watering_parameters
from db_connection import get_water_container_fill_status as water_container_filled

flag_refill_impossibility = False


def get_current_water_level(I2C_address, analog_pin_input):
    bus = smbus.SMBus(1)  # port I2C1
    bus.write_byte(I2C_address, analog_pin_input)  # send one byte to raspi
    value = bus.read_byte(I2C_address)
    water_percentage = (value - 23) / 1.400
    print("W: " + str(water_percentage) + "%")
    print("adc_val=" + str(value))
    return water_percentage


# function used when working in pycharm

# return 50 # TEMPORARY FOR PYCHARM

def get_last_watering_date():
    ts = current_time_milliseconds()
    return ts


def watering_service():
    global flag_refill_impossibility
    if water_container_filled():
        current_water_level = get_current_water_level(I2C_ADDRESS, ANALOG_PIN_INPUT)
        print(water_container_filled())
        if current_water_level <= LOWER_THRESHOLD:
            refill_water_bowl()
        update_watering_parameters(flag_refill_impossibility)
        print(flag_refill_impossibility)
        current_water_level = get_current_water_level(I2C_ADDRESS, ANALOG_PIN_INPUT)
        if current_water_level <= LOWER_THRESHOLD:
            refill_water_bowl()
        sleep(3)


def refill_water_bowl():
    current_water_level = get_current_water_level(I2C_ADDRESS, ANALOG_PIN_INPUT)
    time_refill_triggered = datetime.now()
    while not is_refill_finished(UPPER_THRESHOLD) and not check_refill_impossibility(time_refill_triggered):
        set_servo_angle(OPEN_ANGLE, SERVO_IDENTIFIER)
    if current_water_level <= LOWER_THRESHOLD:
        while not is_refill_finished(UPPER_THRESHOLD):
            set_servo_angle(OPEN_ANGLE, SERVO_IDENTIFIER)
    # refill is done, set angle in initial position
    set_servo_angle(CLOSED_ANGLE, SERVO_IDENTIFIER)


def is_refill_finished(fullness_percentage):
    return get_current_water_level(I2C_ADDRESS, ANALOG_PIN_INPUT) >= fullness_percentage


# Function that checks if the refill is taking place for a time that fits into the
# refill time specification
# @param time_refill_started - datetime Object when refill was triggered
def check_refill_impossibility(time_refill_started):
    global flag_refill_impossibility
    if (datetime.now() - time_refill_started) >= REFILL_STOP_TIME:
        flag_refill_impossibility = True
    else:
        flag_refill_impossibility = False
    return flag_refill_impossibility


def update_watering_parameters(was_watering_process_successful):
    update_DB_watering_parameters(was_watering_process_successful)
