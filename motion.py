from time import sleep

# import RPi.GPIO as GPIO
import telepot
from gpiozero import MotionSensor

from log import get_logger

log = get_logger()
PIR_PIN = 4

pir = MotionSensor(PIR_PIN)

log.info("Motion sensor started")
while True:
    pir.wait_for_motion()
    log.info("You moved")
    pir.wait_for_no_motion()

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(PIR_PIN, GPIO.IN)
#
#
# def motion_callback():
#     print("Motion detected!")
#
#
# def motion_detected():
#     return GPIO.input(PIR_PIN)
#
#
# while True:
#     if motion_detected():
#         motion_callback()
#     else:
#         pass
#     sleep(0.1)

# GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_callback)
