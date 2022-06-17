import time

from monitor.water_refill_monitoring import WaterRefillMonitoring
from monitor.food_refill_monitoring import FoodRefillMonitoring

food_monitoring = FoodRefillMonitoring()
water_monitoring = WaterRefillMonitoring()

def main():
    while True:
        food_monitoring.feeding_service()
        water_monitoring.watering_service()

        #time.sleep(10)
main()
