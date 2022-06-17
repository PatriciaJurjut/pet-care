from datetime import timedelta

# Water constants
WATER_I2C_ADDRESS = 0x48  # PCF8591 I2C address
WATER_CONTROL_BYTE = 0x0  # water sensor - channel 0
WATER_SERVO_PIN = 7
WATER_SERVO_IDENTIFIER = 0  # Pin 7 is mapped to value 0 (servoblaster)
WATER_SERVO_ANGLE_CLOSED = 240  # 240
WATER_SERVO_ANGLE_OPEN = 145  # 170
WATER_LEVEL_LOWER_THRESHOLD = 15
WATER_LEVEL_UPPER_THRESHOLD = 45
WATER_REFILL_STOP_TIME = timedelta(seconds=40)  # stop condition, for when refill cannot be made => container empty

# Food constants
FOOD_SERVO_PIN = 12
FOOD_SERVO_IDENTIFIER = 2
FOOD_SERVO_ANGLE_CLOSED = 88
FOOD_SERVO_ANGLE_OPEN = 60
FOOD_COMPLETE_REFILL_TIME = 0.43  # seconds until bowl is refilled with one portion of food
FOOD_QUICK_TREAT_TIME = 0.21  # seconds until bowl has enough food for a treat
FOOD_STANDARD_CYCLE_LENGTH = 600  # minutes
