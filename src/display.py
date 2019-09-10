import time

from rpilcdmenu import RpiLCDMenu, RpiLCDSubMenu
from rpilcdmenu.items import FunctionItem, SubmenuItem, MessageItem, MenuItem
from rotaryencoder import RotaryEncoder

RS_PIN = 27
E_PIN = 22
DB_PINS = [25, 24, 23, 18]

class Display(object):
    def __init__(self, temperature_sensor):
        self.temperature_sensor = temperature_sensor
        self.menu = RpiLCDMenu(RS_PIN, E_PIN, DB_PINS)
        self.rotary_encoder = RotaryEncoder(self)

        temp_submenu = RpiLCDSubMenu(self.menu)
        temp_submenu.append_item(FunctionItem("Back", lambda: temp_submenu.exit()))
        temp_submenu.append_item(MessageItem(self.getTemp(), "That's cool right?", temp_submenu))

        temp_item = SubmenuItem("Read temp", temp_submenu, self.menu)
        other_item = FunctionItem("Other", lambda: print("other"))
        self.menu.append_item(temp_item).append_item(other_item)

        self.menu.start()

    def onRotaryNext(self):
        self.menu.processDown()

    def onRotaryPrevious(self):
        self.menu.processUp()

    def onRotaryPressed(self):
        self.menu = self.menu.processEnter()

    def getTemp(self):
        temp = round(self.temperature_sensor.read(), 1)
        return f"T: {temp:.1f} C"

    def showTempPage(self):
        prev_temp = 0.0
        while True:
            temp = round(self.temperature_sensor.read(), 1)
            if temp != prev_temp:
                prev_temp = temp
                self.menu.clearDisplay()
                self.menu.message(f"T: {temp:.1f} C")
            time.sleep(1)