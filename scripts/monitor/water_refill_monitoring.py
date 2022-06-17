from time import sleep
import smbus
from datetime import datetime

from servo import set_servo_angle
from utils.constants import WATER_I2C_ADDRESS as I2C_ADDRESS
from utils.constants import WATER_CONTROL_BYTE as CONTROL_BYTE
from utils.constants import WATER_SERVO_IDENTIFIER as SERVO_IDENTIFIER
from utils.constants import WATER_SERVO_ANGLE_OPEN as OPEN_ANGLE
from utils.constants import WATER_SERVO_ANGLE_CLOSED as CLOSED_ANGLE
from utils.constants import WATER_LEVEL_LOWER_THRESHOLD as LOWER_THRESHOLD
from utils.constants import WATER_LEVEL_UPPER_THRESHOLD as UPPER_THRESHOLD
from utils.constants import WATER_REFILL_STOP_TIME as REFILL_STOP_TIME
from database.db_connection import DatabaseConnection


class WaterRefillMonitoring:
    __flag_refill_impossibility: bool

    def __init__(self):
        self.__database_connection = DatabaseConnection()
        self.__flag_refill_impossibility = not self.__does_container_have_water()

    def __get_current_water_level(self, i2c_address):
        bus = smbus.SMBus(1)  # port I2C1
        bus.write_byte(i2c_address, CONTROL_BYTE)
        value = bus.read_byte(i2c_address)
        water_percentage = (value - 21) / 1.4
        return water_percentage

    def watering_service(self):
        if self.__does_container_have_water():
            current_water_level = self.__get_current_water_level(I2C_ADDRESS)
            if current_water_level <= LOWER_THRESHOLD:
                self.__refill_water_bowl()
                self.__update_watering_parameters(self.__flag_refill_impossibility)

    def __refill_water_bowl(self):
        current_water_level = self.__get_current_water_level(I2C_ADDRESS)
        time_refill_triggered = datetime.now()
        while not self.__is_refill_process_finished(UPPER_THRESHOLD) and not self.__mark_refill_impossibility(
                time_refill_triggered):
            print(self.__flag_refill_impossibility)
            set_servo_angle(OPEN_ANGLE, SERVO_IDENTIFIER)
        # refill is done, set angle in initial position
        set_servo_angle(CLOSED_ANGLE, SERVO_IDENTIFIER)

    def __does_container_have_water(self) -> bool:
        return self.__database_connection.get_water_container_fill_status()

    def __is_refill_process_finished(self, fullness_percentage):
        return self.__get_current_water_level(I2C_ADDRESS) >= fullness_percentage

    def __mark_refill_impossibility(self, time_refill_started):
        if (datetime.now() - time_refill_started) >= REFILL_STOP_TIME:
            self.__flag_refill_impossibility = True
        else:
            self.__flag_refill_impossibility = False
        return self.__flag_refill_impossibility

    def __update_watering_parameters(self, was_watering_process_successful):
        self.__database_connection.update_db_watering_parameters(was_watering_process_successful)
