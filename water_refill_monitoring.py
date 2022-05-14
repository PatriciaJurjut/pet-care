import time
import smbus
from datetime import datetime
from utils import current_time_milliseconds
from constants import WATER_I2C_ADDRESS, WATER_SENSOR_ANALOG_PIN_INPUT
from constants import WATER_SERVO_NUMBER, WATER_SERVO_ANGLE_OPEN
from servo import set_servo_angle

# TODO: define threshhold
threshhold = 30 # (almost empty, I guess)


def get_current_water_level(I2C_address, analog_pin_input):
    bus = SMBus(1) # port I2C1
    bus.write_byte(I2C_address, analog_pin_input) # send one byte to raspi
    value = bus.read_byte(address)
    
def get_last_watering_date():
    ts = current_time_milliseconds() 
    return ts

def watering_service():
    while True:
        current_water_level = get_current_water_level()
        if(current_water_level <= threshhold):
            refill_water_bowl()
        sleep(10)
                
def refill_water_bowl():
    set_servo_angle(WATER_SERVO_ANGLE_OPEN, WATER_SERVO_NUMBER)
    