import time
import RPi.GPIO as GPIO

from display import Display
from temperature import TemperatureSensor


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    temperature_sensor = TemperatureSensor()
    display = Display(temperature_sensor)
    
    try: 
        while True:
            time.sleep(0.1)
    finally:
        pass
