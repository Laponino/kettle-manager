import time

from display import Display
from temperaturesensor import TemperatureSensor


if __name__ == "__main__":
    temperature_sensor = TemperatureSensor()
    display = Display(temperature_sensor)
    
    try: 
        while True:
            time.sleep(0.1)
    finally:
        pass