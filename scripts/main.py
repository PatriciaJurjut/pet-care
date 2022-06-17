import time

from monitor.water_refill_monitoring import WaterRefillMonitoring
from monitor.food_refill_monitoring import FoodRefillMonitoring


def main(self):
    while True:
        self.food_monitoring = FoodRefillMonitoring()
        self.food_monitoring.feeding_service()
        self.water_monitoring = WaterRefillMonitoring()
        self.water_monitoring.watering_service()

        time.sleep(10)


main.main()
