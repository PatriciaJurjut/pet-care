import time
import pyrebase
from utils import datetime_to_timestamp
from datetime import datetime
from water_refill_monitoring import get_last_watering_date
from water_refill_monitoring import watering_service
from food_refill_monitoring import feeding_service
from servo import set_servo_angle

config = {
	"apiKey": "AlzaSyDEWCNEX_NiEEbw4dz8oJuQ9j1tNiTHMJk",
	"authDomain": "pet-care-application-2a313",
	"databaseURL": "https://pet-care-application-2a313-default-rtdb.europe-west1.firebasedatabase.app",
	"storageBucket": "pet-care-application-2a313.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def get_feeding_cycles_number():
    return db.child("feeding").child("feedingCycles").get().val()

def get_feeding_cycle_length():
    return db.child("feeding").child("feedingCycles").child("cycleLength").get().val()

# Sets a second-level nested variable's value in the database
# nesting is: child1 -> child2 (key) = @param value
def update_DB_timestamp(child1_name, child2_name, value):
    db.child(child1_name).child(child2_name).set(value)

def get_feeding_cycles():
    return db.child("feedingCycles").value().get()



while True:
    #last_watering_date = get_last_watering_date()
    #db.child("lastWateringDate").set(last_watering_date)
    servo_pin = 40
    angle = 0
    #set_servo_angle(angle, servo_pin) # NOT TO BE USED IN A WHILE - TRUE.
    watering_service()
    feeding_service()
    
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
        #update_level2_nested_variable("watering", "refillImpossibility", False)
        #update_level2_nested_variable("watering", "doesContainerHaveWater", True)
                                              
def update_DB_refill_impossibility(booleanValue):
    update_level2_nested_variable("watering", "refillImpossibility", booleanValue)
    
def get_water_container_fill_status():
    #print(db.child("doesContainerHaveWater").get().val())
    return db.child("watering").child("doesContainerHaveWater").get().val()

def get_last_feeding_time():
    return datetime.fromtimestamp(db.child("feeding").child("lastFeedingTime").get().val())

def get_manual_feeding_field():
    return db.child("feeding").child("manualFeeding").get().val()
    