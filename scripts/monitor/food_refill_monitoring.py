from time import sleep
from datetime import datetime
from datetime import timedelta
from utils.constants import FOOD_SERVO_ANGLE_OPEN as OPEN_ANGLE
from utils.constants import FOOD_SERVO_ANGLE_CLOSED as CLOSED_ANGLE
from utils.constants import FOOD_SERVO_IDENTIFIER as SERVO_IDENTIFIER
from utils.constants import FOOD_COMPLETE_REFILL_TIME as SECONDS_FOR_COMPLETE_REFILL
from utils.constants import FOOD_QUICK_TREAT_TIME as SECONDS_FOR_TREAT
from utils.constants import FOOD_STANDARD_CYCLE_LENGTH as STANDARD_CYCLE_LENGTH
from servo import set_servo_angle
from database.db_connection import DatabaseConnection


def operate_servo(open_angle: int, closed_angle: int, servo_id: int, seconds_until_closed: int):
    """
        Function that is directly linked to the food servomotor. It rotates the servo considering the given parameters.
        fits the vent of the system
        :param closed_angle t:param open_angle the angle that he angle at which the vent is sealed
        :param servo_id the identifier for the servomotor
        :param seconds_until_closed the time, measured in seconds, for how long the open_angle param should persist

    """
    set_servo_angle(open_angle, servo_id)
    sleep(seconds_until_closed)
    set_servo_angle(closed_angle, servo_id)


class FoodRefillMonitoring:
    __cycle_length_minutes = STANDARD_CYCLE_LENGTH  # default mode: feeding occurs every 5 hours = 300 mins
    __completed_cycles: int
    __last_feeding_time: datetime
    __upcoming_feeding_time: datetime
    __is_bowl_refilled_on_startup: bool
    __database_connection: DatabaseConnection
    __flag_first_time_called: bool
    __first_time_called: bool

    def __init__(self):
        self.__database_connection = DatabaseConnection()
        self.__flag_first_time_called = True
        self.__first_time_called = datetime.now()
        self.__init_db_variables()

    def __init_db_variables(self):
        self.__cycle_length_minutes = self.__database_connection.get_feeding_cycle_length()
        self.__completed_cycles = self.__database_connection.get_completed_cycles()
        print("Cycle length: " + str(self.__cycle_length_minutes))
        self.__last_feeding_time = self.__database_connection.get_last_feeding_time()
        self.__is_bowl_refilled_on_startup = self.__database_connection.get_bowl_refilled_on_startup_field()
        self.__update_upcoming_feeding_time()
        print("Last feeding time: " + str(self.__last_feeding_time))

    def feeding_service(self):
        self.__init_db_variables()
        print("UPCOMING feeding time: " + str(self.__upcoming_feeding_time))
        print("Bowl refilled on startup: " + str(self.__is_bowl_refilled_on_startup))
        if self.__is_manual_feeding_performed():
            self.__refill_bowl_for_treat()

        if not self.__is_bowl_refilled_on_startup:
            self.__refill_bowl_completely()
            self.__notify_bowl_refilled_on_startup()

        elif self.__is_feeding_time_now():  # condition for cyclic feeding
            self.__refill_bowl_completely()

    # Bowl is refilled for a treat (small portion) -> abt. 0.5 seconds
    def __refill_bowl_for_treat(self):
        """
            Bowl is being refilled with a portion of food, smaller than a whole ratio. \n
            This function is used for manual feeding only.
        """
        operate_servo(OPEN_ANGLE, CLOSED_ANGLE, SERVO_IDENTIFIER, SECONDS_FOR_TREAT)
        self.__disable_manual_feeding()

    def __refill_bowl_completely(self):
        """
            Bowl is being refilled with one food ratio. \n
            This function is used for cyclic feeding only.
        """
        operate_servo(OPEN_ANGLE, CLOSED_ANGLE, SERVO_IDENTIFIER, SECONDS_FOR_COMPLETE_REFILL)
        self.__update_feeding_parameters()

    def __update_feeding_parameters(self):
        self.__last_feeding_time = datetime.now()
        self.__completed_cycles += 1
        print("Completed cycles: " + str(self.__completed_cycles))
        self.__flag_first_time_called = False
        self.__update_upcoming_feeding_time()
        self.__database_connection.update_db_feeding_parameters(self.__last_feeding_time, self.__completed_cycles)

    def __update_upcoming_feeding_time(self):
        if self.__flag_first_time_called:
            self.__upcoming_feeding_time = self.__first_time_called + timedelta(minutes=int(str(self.__cycle_length_minutes)))
        else:
            self.__upcoming_feeding_time = self.__last_feeding_time + timedelta(minutes=int(str(self.__cycle_length_minutes)))

    def __is_feeding_time_now(self):
        current_time = datetime.now()
        return current_time >= self.__upcoming_feeding_time

    def __is_manual_feeding_performed(self):
        return self.__database_connection.get_manual_feeding_field()

    def __disable_manual_feeding(self):
        self.__database_connection.update_db_manual_feeding(False)

    def __notify_bowl_refilled_on_startup(self):
        self.__database_connection.update_bowl_refilled_on_startup()
