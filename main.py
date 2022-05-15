from water_refill_monitoring import get_last_watering_date
from water_refill_monitoring import watering_service
from food_refill_monitoring import feeding_service
from servo import set_servo_angle

def main():
    while True:
    #last_watering_date = get_last_watering_date()
    #db.child("lastWateringDate").set(last_watering_date)
        servo_pin = 40
        angle = 0
        #set_servo_angle
        (240, 0)
        watering_service()
        feeding_service()
    
main()