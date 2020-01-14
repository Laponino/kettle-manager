import time

from rpilcdmenu import RpiLCDMenu, RpiLCDSubMenu
from rpilcdmenu.items import FunctionItem, SubmenuItem, MessageItem, MenuItem
from rotaryencoder import RotaryEncoder
from power import Power

RS_PIN = 27
E_PIN = 22
DB_PINS = [25, 24, 23, 18]
POWER_PIN = 21

class Display(object):
    def __init__(self, temperature_sensor):
        self.temperature_sensor = temperature_sensor
        self.menu = RpiLCDMenu(RS_PIN, E_PIN, DB_PINS)
        self.rotary_encoder = RotaryEncoder(self)
        self.power = Power(POWER_PIN)

        # Calibrate Submenu
        read_temp_submenu = RpiLCDSubMenu(self.menu)
        read_temp_submenu.append_item(
                FunctionItem("Back", lambda: read_temp_submenu.exit()))
        read_temp_submenu.append_item(MenuItem(self.getTemp()))

        # Options Submenu
        options_submenu = RpiLCDSubMenu(self.menu)
        options_submenu.append_item(
                FunctionItem("Setup", lambda: print("setup")))
        options_submenu.append_item(
                SubmenuItem("Read temp", read_temp_submenu, options_submenu))
        options_submenu.append_item(
                FunctionItem("Back", lambda: options_submenu.exit()))

        # Select-temperature Submenu
        boil_temp_submenu = RpiLCDSubMenu(self.menu)
        for t in [60, 65, 70, 75, 80, 85, 90, 95, 100]:
            boil_message = FunctionItem(f"{t} C", self.onTempSelected, [t])
            boil_temp_submenu.append_item(boil_message) 
        boil_temp_submenu.append_item(
                FunctionItem("Back", lambda: boil_temp_submenu.exit()))

        # Select-volume Submenu
        boil_vol_submenu = RpiLCDSubMenu(self.menu)
        for v in [0.50, 0.75, 1.00, 1.25, 1.50, 1.75]:
            boil_vol_submenu.append_item(
                    SubmenuItem(f"{v:.2f} L", boil_temp_submenu, boil_vol_submenu))
        boil_vol_submenu.append_item(
                FunctionItem("Back", lambda: boil_vol_submenu.exit()))

        # Main Menu
        boil_item = SubmenuItem("Boil", boil_vol_submenu, self.menu)
        temp_item = FunctionItem("Calibrate", lambda: print("calibrate"))
        other_item = SubmenuItem("Options", options_submenu, self.menu)
        self.menu.append_item(boil_item) \
                 .append_item(temp_item) \
                 .append_item(other_item)

        self.menu.start()

    def onTempSelected(self, t):
        print(f"Boiling to {t} C...")
        self.power.on()

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
