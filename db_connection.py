import time
import pyrebase
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
    
    