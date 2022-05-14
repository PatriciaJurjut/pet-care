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
from servo import set_servo_angle

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
        current_water_level = get_current_water_level(I2C_address, analog_pin_input)
        if(current_water_level <= lower_threshold):
            refill_water_bowl()
        sleep(3)
                
def refill_water_bowl():
    current_water_level = get_current_water_level(I2C_address, analog_pin_input)
    if current_water_level <= lower_threshold:
        while not is_refill_finished(upper_threshold):
            set_servo_angle(open_angle, servo_number)
    #refill is done, set angle in initial position
    set_servo_angle(closed_angle, servo_number)
    
def is_refill_finished(fullness_percentage):
    return get_current_water_level(I2C_address, analog_pin_input) >= fullness_percentage
    