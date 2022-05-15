import RPi.GPIO as GPIO
from time import sleep
import time
import smbus
import os

#servo_pin = 10

# pwm.changeDutyCycle -> 1.45 - 12.5
# SetAngle -> max. 190

last_set_angle = 1000

# TODO: variabila last_set_angle, care daca e identica cu cea venita ca param., sa nu seteze unghiul
# (ca sa nu o ia servo-ul razna)
def set_servo_angle_bkp(angle, servo_pin):
    global last_set_angle
    if angle is not last_set_angle:
        last_set_angle = angle
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servo_pin, GPIO.OUT)
    
        pwm=GPIO.PWM(servo_pin, 50)
        pwm.start(0)
    
        duty = angle / 18 + 2
        GPIO.output(servo_pin, True)
        pwm.ChangeDutyCycle(duty)
	#sleep(2)
	#pwm.ChangeDutyCycle(12.5)
        sleep(1)
        GPIO.output(servo_pin, False)
        pwm.ChangeDutyCycle(0)
        pwm.stop()
        GPIO.cleanup()

def set_servo_angle(angle, servo_number):
    os.system("echo " + str(servo_number) + "=" + str(angle) + " > /dev/servoblaster")
        

#set_servo_angle(0, 3)

#SetAngle(190)


