import pyrebase
from utils import datetime_to_timestamp
from datetime import datetime
from typing import Final

# from water_refill_monitoring import get_last_watering_date

config = {
    "apiKey": "AIzaSyBqbVqrQKEaUkEWLqnhh0_9Cv1p-Majox4",
    "authDomain": "pet-care-bkp-23319",
    "databaseURL": "https://pet-care-bkp-23319-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "pet-care-bkp-23319.appspot.com"
}

firebase: Final[any] = pyrebase.initialize_app(config)
db: Final[any] = firebase.database()

feedingCycles: int


def get_feeding_cycles_number() -> int:
    return db.child("feeding").child("feedingCycles").get().val()


def get_feeding_cycle_length() -> int:
    # return db.child("feeding").child("feedingCycles").child("cycleLength").get().val()
    global feedingCycles
    # feedingCycles = db.child("feeding").child("feedingCycles").child("cycleLength").stream(stream_handler)
    returnVar = db.child("feeding").child("feedingCycles").child("cycleLength").get().val()
    # feedingCycles.close()
    print(returnVar)
    return int(returnVar)


# Sets a second-level nested variable's value in the database
# nesting is: child1 -> child2 (key) = @param value
def update_DB_timestamp(child1_name, child2_name, value):
    db.child(child1_name).child(child2_name).set(value)


def get_feeding_cycles() -> int:
    return db.child("feedingCycles").value().get()


def update_level1_nested_variable(child_name, value):
    print(value)
    db.child(child_name).set(value)


def update_level2_nested_variable(child1_name, child2_name, value):
    db.child(child1_name).child(child2_name).set(value)


def update_DB_feeding_parameters(last_feeding_time):
    update_DB_timestamp("feeding", "lastFeedingTime", datetime_to_timestamp(last_feeding_time))


def update_DB_watering_parameters(wasWateringProcessUnsuccessful):
    if wasWateringProcessUnsuccessful:
        update_level2_nested_variable("watering", "refillImpossibility", True)
        update_level2_nested_variable("watering", "doesContainerHaveWater", False)
    else:
        update_level2_nested_variable("watering", "lastWateringTime", datetime_to_timestamp(datetime.now()))
        # update_level2_nested_variable("watering", "refillImpossibility", False)
        # update_level2_nested_variable("watering", "doesContainerHaveWater", True)


def update_DB_refill_impossibility(is_water_container_empty):
    update_level2_nested_variable("watering", "refillImpossibility", is_water_container_empty)


def get_water_container_fill_status() -> bool:
    # print(db.child("doesContainerHaveWater").get().val())
    return db.child("watering").child("doesContainerHaveWater").get().val()


def get_last_feeding_time() -> datetime:
    return datetime.fromtimestamp(db.child("feeding").child("lastFeedingTime").get().val())


def get_manual_feeding_field() -> bool:
    return db.child("feeding").child("manualFeeding").get().val()


def stream_handler(message):
    # print(message["event"]) # put
    # print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"])  # {'title': 'Pyrebase', "body": "etc..."}
    print(str(message["data"]).split())
    global feedingCycles
    feedingCycles = str(message["data"]).split()
    strFdCy = ''.join(feedingCycles)
    # print(type(strFdCy))

    return strFdCy

# time.sleep(10)
# print(lastFeedingTime)
