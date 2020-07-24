import RPi.GPIO as GPIO
import time
 
class Power:
    def __init__(self, relay_pin): 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relay_pin,GPIO.OUT)
        self.relay_pin = relay_pin
        self.off()

    def on(self):
        GPIO.output(self.relay_pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.relay_pin, GPIO.LOW)
