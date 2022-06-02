import time

from water_refill_monitoring import watering_service
from food_refill_monitoring import feeding_service


def main():
    while True:
        # last_watering_date = get_last_watering_date()
        # db.child("lastWateringDate").set(last_watering_date)
        # set_servo_angle(240, 0)

        # watch_service_triggering_markers()

        watering_service()
        feeding_service()
        time.sleep(10)


main()
