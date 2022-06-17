import pyrebase
from utils.utils import datetime_to_timestamp
from datetime import datetime
from typing import Final


class DatabaseConnection:
    __config = {
        "apiKey": "AIzaSyBqbVqrQKEaUkEWLqnhh0_9Cv1p-Majox4",
        "authDomain": "pet-care-bkp-23319",
        "databaseURL": "https://pet-care-bkp-23319-default-rtdb.europe-west1.firebasedatabase.app",
        "storageBucket": "pet-care-bkp-23319.appspot.com"
    }

    __firebase: Final[any] = pyrebase.initialize_app(__config)
    __db: Final[any] = __firebase.database()

    def get_feeding_cycle_length(self) -> int:
        return self.__db.child("feeding").child("feedingCycles").child("cycleLength").get().val()

    def get_completed_cycles(self) -> int:
        return self.__db.child("feeding").child("feedingCycles").child("completedCycles").get().val()

    def get_feeding_cycles(self) -> int:
        return self.__db.child("feedingCycles").value().get()

    def get_last_feeding_time(self) -> datetime:
        return datetime.fromtimestamp(self.__db.child("feeding").child("lastFeedingTime").get().val())

    def get_manual_feeding_field(self) -> bool:
        return self.__db.child("feeding").child("manualFeeding").get().val()

    def get_bowl_refilled_on_startup_field(self) -> bool:
        return self.__db.child("feeding").child("bowlRefilledOnStartup").get().val()

    def get_water_container_fill_status(self) -> bool:
        # print(db.child("doesContainerHaveWater").get().val())
        return self.__db.child("watering").child("doesContainerHaveWater").get().val()

    def update_db_timestamp(self, child1_name, child2_name, value):
        self.__db.child(child1_name).child(child2_name).set(value)

    def update_db_feeding_parameters(self, last_feeding_time, completed_cycles):
        self.update_db_timestamp("feeding", "lastFeedingTime", datetime_to_timestamp(last_feeding_time))
        self._update_level3_nested_variable("feeding", "feedingCycles", "completedCycles", completed_cycles)

    def update_db_watering_parameters(self, was_watering_process_unsuccessful):
        if was_watering_process_unsuccessful:
            self._update_level2_nested_variable("watering", "refillImpossibility", True)
            self._update_level2_nested_variable("watering", "doesContainerHaveWater", False)
        else:
            self._update_level2_nested_variable("watering", "lastWateringTime", datetime_to_timestamp(datetime.now()))
            self._update_level2_nested_variable("watering", "refillImpossibility", False)
            self._update_level2_nested_variable("watering", "doesContainerHaveWater", True)

    def update_db_refill_impossibility(self, is_water_container_empty):
        self._update_level2_nested_variable("watering", "refillImpossibility", is_water_container_empty)

    def update_bowl_refilled_on_startup(self):
        self._update_level2_nested_variable("feeding", "bowlRefilledOnStartup", True)

    def update_db_manual_feeding(self, value):
        self._update_level2_nested_variable("feeding", "manualFeeding", value)

    def _update_level1_nested_variable(self, child_name, value):
        self.__db.child(child_name).set(value)

    def _update_level2_nested_variable(self, child1_name, child2_name, value):
        self.__db.child(child1_name).child(child2_name).set(value)

    def _update_level3_nested_variable(self, child1_name, child2_name, child3_name, value):
        self.__db.child(child1_name).child(child2_name).child(child3_name).set(value)