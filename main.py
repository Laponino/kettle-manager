import os
import glob
import time

from rpilcdmenu import RpiLCDMenu
from rpilcdmenu.items import FunctionItem
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


if __name__ == "__main__":
    lcd = RpiLCDMenu(27, 22, [25, 24, 23, 18])
    def showTempPage():
        lcd.clearDisplay()
        temp = read_temp()
        lcd.message(f"T: {temp:.1}°C")
    
    temp_item = FunctionItem("Read temp", showTempPage)
    other_item = FunctionItem("Other", showTempPage)
    lcd.append_item(temp_item)
    lcd.append_item(other_item)
    lcd.start()

    time.sleep(1)
    lcd.processDown()
    time.sleep(1)
    lcd.processEnter()