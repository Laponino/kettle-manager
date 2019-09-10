import time

from display import Display
from rotaryencoder import RotaryEncoder
from temperaturesensor import TemperatureSensor

# Callback for rotary change

if __name__ == "__main__":
    temperature_sensor = TemperatureSensor()
    lcd = Display(temperature_sensor)
    rotary_encoder = RotaryEncoder(lcd)
    
    try:
        while True:
            time.sleep(0.1)
    finally:
        rotary_encoder.stop()