from time import sleep
import smbus
from datetime import datetime

from scripts.servo import set_servo_angle
from scripts.utils.constants import WATER_I2C_ADDRESS as I2C_ADDRESS
from scripts.utils.constants import WATER_SENSOR_ANALOG_PIN_INPUT as ANALOG_PIN_INPUT
from scripts.utils.constants import WATER_SERVO_IDENTIFIER as SERVO_IDENTIFIER
from scripts.utils.constants import WATER_SERVO_ANGLE_OPEN as OPEN_ANGLE
from scripts.utils.constants import WATER_SERVO_ANGLE_CLOSED as CLOSED_ANGLE
from scripts.utils.constants import WATER_LEVEL_LOWER_THRESHOLD as LOWER_THRESHOLD
from scripts.utils.constants import WATER_LEVEL_UPPER_THRESHOLD as UPPER_THRESHOLD
from scripts.utils.constants import WATER_REFILL_STOP_TIME as REFILL_STOP_TIME
from scripts.database.db_connection import DatabaseConnection


class WaterRefillMonitoring:
    __flag_refill_impossibility: bool

    def __init__(self):
        self.__database_connection = DatabaseConnection()
        self.__flag_refill_impossibility = self.__does_container_have_water()

    def __get_current_water_level(I2C_address, analog_pin_input):
        bus = smbus.SMBus(1)  # port I2C1
        bus.write_byte(I2C_address, analog_pin_input)  # send one byte to raspi
        value = bus.read_byte(I2C_address)
        water_percentage = (value - 23) / 1.400
        print("W: " + str(water_percentage) + "%")
        print("adc_val=" + str(value))
        return water_percentage

    # function used when working in pycharm

    # def __get_current_water_level(self, I2C_address, analog_pin_input) -> int:
    #     return 5  # TEMPORARY FOR PYCHARM. TODO: REMOVE

    def watering_service(self):
        if self.__does_container_have_water():
            current_water_level = self.__get_current_water_level(I2C_ADDRESS, ANALOG_PIN_INPUT)
            print("Water container filled: " + str(self.__does_container_have_water()))
            if current_water_level <= LOWER_THRESHOLD:
                self.__refill_water_bowl()
                self.__update_watering_parameters(self.__flag_refill_impossibility)
        print("Refill impossibility: " + str(self.__flag_refill_impossibility))
        sleep(3) #TODO

    def __refill_water_bowl(self):
        current_water_level = self.__get_current_water_level(I2C_ADDRESS, ANALOG_PIN_INPUT)
        time_refill_triggered = datetime.now()
        while not self.__is_refill_process_finished(UPPER_THRESHOLD) and not self.__mark_refill_impossibility(
                time_refill_triggered):
            print(self.__flag_refill_impossibility)
            set_servo_angle(OPEN_ANGLE, SERVO_IDENTIFIER)
            print("Water angle open")
            if current_water_level <= LOWER_THRESHOLD:
                set_servo_angle(OPEN_ANGLE, SERVO_IDENTIFIER)
                print("Water angle open")
                a = 5
        # refill is done, set angle in initial position
        set_servo_angle(CLOSED_ANGLE, SERVO_IDENTIFIER)
        print("Water angle closed")

    def __does_container_have_water(self) -> bool:
        return self.__database_connection.get_water_container_fill_status()

    def __is_refill_process_finished(self, fullness_percentage):
        return self.__get_current_water_level(I2C_ADDRESS, ANALOG_PIN_INPUT) >= fullness_percentage

    def __mark_refill_impossibility(self, time_refill_started):
        if (datetime.now() - time_refill_started) >= REFILL_STOP_TIME:
            self.__flag_refill_impossibility = True
        else:
            self.__flag_refill_impossibility = False
        return self.__flag_refill_impossibility

    def __update_watering_parameters(self, was_watering_process_successful):
        self.__database_connection.update_db_watering_parameters(was_watering_process_successful)
