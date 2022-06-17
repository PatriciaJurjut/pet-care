import os


def set_servo_angle(angle, servo_number):
    os.system("echo " + str(servo_number) + "=" + str(angle) + " > /dev/servoblaster")
