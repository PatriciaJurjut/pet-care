import time
import pyrebase
from water_refill_monitoring import get_last_watering_date
from servo import set_servo_angle

config = {
	"apiKey": "AlzaSyDEWCNEX_NiEEbw4dz8oJuQ9j1tNiTHMJk",
	"authDomain": "pet-care-application-2a313",
	"databaseURL": "https://pet-care-application-2a313-default-rtdb.europe-west1.firebasedatabase.app",
	"storageBucket": "pet-care-application-2a313.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

while True:
    #last_watering_date = get_last_watering_date()
    #db.child("lastWateringDate").set(last_watering_date)
    servo_pin = 3
    angle = 0
    set_servo_angle(angle, servo_pin) # NOT TO BE USED IN A WHILE - TRUE. 
    
    