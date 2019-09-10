import time

from rpilcdmenu import RpiLCDMenu
from rpilcdmenu.items import FunctionItem

RS_PIN = 27
E_PIN = 22
DB_PINS = [25, 24, 23, 18]

class Display(RpiLCDMenu):
    def __init__(self, temperature_sensor):
        self.temperature_sensor = temperature_sensor
        super().__init__(RS_PIN, E_PIN, DB_PINS)

        temp_item = FunctionItem("Read temp", self.showTempPage)
        other_item = FunctionItem("Other", lambda: print("other"))
        self.append_item(temp_item)
        self.append_item(other_item)
        self.start()

    def showTempPage(self):
        prev_temp = 0.0
        while True:
            temp = round(self.temperature_sensor.read(), 1)
            if temp != prev_temp:
                prev_temp = temp
                self.clearDisplay()
                self.message(f"T: {temp:.1f} C")
            time.sleep(1)