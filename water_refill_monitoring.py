from time import sleep
import smbus
from datetime import datetime
from utils import current_time_milliseconds
from constants import WATER_I2C_ADDRESS as I2C_address
from constants import WATER_SENSOR_ANALOG_PIN_INPUT as analog_pin_input
from constants import WATER_SERVO_NUMBER as servo_number
from constants import WATER_SERVO_ANGLE_OPEN as open_angle
from constants import WATER_SERVO_ANGLE_CLOSED as closed_angle
from constants import WATER_LEVEL_LOWER_THRESHOLD as lower_threshold
from constants import WATER_LEVEL_UPPER_THRESHOLD as upper_threshold
from constants import WATER_REFILL_STOP_TIME as refill_stop_time
from servo import set_servo_angle
from db_connection import update_DB_watering_parameters
from db_connection import get_water_container_fill_status as water_container_filled

flag_refill_impossibility = False

def get_current_water_level(I2C_address, analog_pin_input):
    bus = smbus.SMBus(1) # port I2C1
    bus.write_byte(I2C_address, analog_pin_input) # send one byte to raspi
    value = bus.read_byte(I2C_address)
    water_percentage = (value-23)/1.400
    print("W: "+str(water_percentage)+"%")
    print("adc_val="+str(value))
    return water_percentage
    
def get_last_watering_date():
    ts = current_time_milliseconds() 
    return ts

def watering_service():
    global flag_refill_impossibility
    if(water_container_filled()):
        current_water_level = get_current_water_level(I2C_address, analog_pin_input)
        print(water_container_filled())
        if(current_water_level <= lower_threshold):
            refill_water_bowl()
        update_watering_parameters(flag_refill_impossibility)
        print(flag_refill_impossibility)
        sleep(3)
                
def refill_water_bowl():
    current_water_level = get_current_water_level(I2C_address, analog_pin_input)
    time_refill_triggered = datetime.now()
    while not is_refill_finished(upper_threshold) and not check_refill_impossibility(time_refill_triggered):
        set_servo_angle(open_angle, servo_number)
    #refill is done, set angle in initial position
    set_servo_angle(closed_angle, servo_number)
    
def is_refill_finished(fullness_percentage):
    return get_current_water_level(I2C_address, analog_pin_input) >= fullness_percentage

# Function that checks if the refill is taking place for a time that fits into the
# refill time specification
# @param time_refill_started - datetime Object when refill was triggered
def check_refill_impossibility(time_refill_started):
    global flag_refill_impossibility
    if (datetime.now() - time_refill_started) >= refill_stop_time:
        flag_refill_impossibility = True
    else:
        flag_refill_impossibility = False
    return flag_refill_impossibility

def update_watering_parameters(wasWateringProcessSuccessful):
    update_DB_watering_parameters(wasWateringProcessSuccessful)

