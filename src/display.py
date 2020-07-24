import time

from rpilcdmenu import RpiLCDMenu, RpiLCDSubMenu
from rpilcdmenu.items import FunctionItem, SubmenuItem, MessageItem, MenuItem
from button import RotaryEncoder
from switch import Power
from model import ServerModel

RS_PIN = 27
E_PIN = 22
DB_PINS = [25, 24, 23, 18]
POWER_PIN = 21

class Display(object):
    def __init__(self, temperature_sensor):
        self.temperature_sensor = temperature_sensor
        self.rotary_encoder = RotaryEncoder(self)
        self.power = Power(POWER_PIN)
        self.model = ServerModel(1)

        self.boil_temps = [60, 65, 70, 75, 80, 85, 90, 95, 100]
        self.boil_volumes = [0.50, 0.75, 1.00, 1.25, 1.50, 1.75]

        self.init_menu()

    def init_menu(self):
        self.menu = RpiLCDMenu(RS_PIN, E_PIN, DB_PINS)
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
        for t in self.boil_temps:
            boil_message = FunctionItem(f"{t} C", self.onTempSelected, [t])
            boil_temp_submenu.append_item(boil_message) 
        boil_temp_submenu.append_item(
                FunctionItem("Back", lambda: boil_temp_submenu.exit()))

        # Select-volume Submenu
        boil_vol_submenu = RpiLCDSubMenu(self.menu)
        for v in self.boil_volumes:
            boil_vol_submenu.append_item(
                    SubmenuItem(f"{v:.2f} L", boil_temp_submenu, boil_vol_submenu))
        boil_vol_submenu.append_item(
                FunctionItem("Back", lambda: boil_vol_submenu.exit()))

        # Select-volume Submenu
        calib_vol_submenu = RpiLCDSubMenu(self.menu)
        for v in self.boil_volumes:
            calib_vol_submenu.append_item(
                    FunctionItem(f"{v:.2f} L", self.calibrate, [v]))
        boil_vol_submenu.append_item(
                FunctionItem("Back", lambda: calib_vol_submenu.exit()))

        # Main Menu
        boil_item = SubmenuItem("Boil", boil_vol_submenu, self.menu)
        temp_item = SubmenuItem("Calibrate", calib_vol_submenu, self.menu)
        other_item = SubmenuItem("Options", options_submenu, self.menu)
        self.menu.append_item(boil_item) \
                 .append_item(temp_item) \
                 .append_item(other_item)

        self.menu.start()

    def onTempSelected(self, t):
        print(f"Boiling to {t} C...")
        self.menu.clearDisplay()
        self.menu.message(f"Boiling to {t} C...")
        self.power.on()
        go_on = True
        while go_on:
            temp = round(self.temperature_sensor.read(), 1)
            print(f"Temp: {temp} C")
            if temp > int(t):
                go_on = False
            time.sleep(1)
        self.power.off()
        self.menu.clearDisplay()
        self.menu.message(f"Done! {temp} C")

    def calibrate(self, volume=1.5):
        target_temp = 99
        print(f"Calibrating...")
        self.menu.clearDisplay()
        self.menu.message(f"Boiling {volume}L…")
        self.power.on()
        go_on = True
        st = time.time()
        temps = []
        times = []
        while go_on:
            temp_i = round(self.temperature_sensor.read(), 1)
            time_i = time.time() - st
            temps.append(temp_i)
            times.append(time_i)
            print(f"{time_i}, {temp_i}")
            if temp_i > int(target_temp):
                go_on = False
            time.sleep(1)
        self.power.off()
        self.menu.clearDisplay()
        self.menu.message(f"Done! Sending data to the server…")
        self.model.train(volume, temps, times)
        self.menu.message(f"Model updated!")
        print("Done training")
        time.sleep(1)
        self.init_menu()

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
