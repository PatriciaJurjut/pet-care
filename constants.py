from datetime import datetime, timedelta

#Water constants
WATER_I2C_ADDRESS=0x48
WATER_SENSOR_ANALOG_PIN_INPUT = 0x40 # water sensor
WATER_SERVO_PIN = 7 #7
WATER_SERVO_NUMBER = 0 # Pin 7 is mapped to value 0 
WATER_SERVO_ANGLE_CLOSED = 240 #240
WATER_SERVO_ANGLE_OPEN = 145 #170
WATER_LEVEL_LOWER_THRESHOLD = 15
WATER_LEVEL_UPPER_THRESHOLD = 70
WATER_REFILL_STOP_TIME = timedelta(seconds=10) # stop condition, for when refill cannot be made

#Food constants 
FOOD_SERVO_PIN = 12
FOOD_SERVO_NUMBER = 2 
FOOD_SERVO_ANGLE_CLOSED = 88 
FOOD_SERVO_ANGLE_OPEN = 60
FOOD_SERVO_PIN = 12
FOOD_SERVO_NUMBER = 2 
FOOD_SERVO_ANGLE_CLOSED = 88 
FOOD_SERVO_ANGLE_OPEN = 60
FOOD_REFILL_TIME = 1.5 # seconds until bowl is refilled with one portion of food
