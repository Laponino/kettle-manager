from ky040.KY040 import KY040

CLOCK_PIN = 5
DATA_PIN = 6
SWITCH_PIN = 13

class RotaryEncoder(KY040):
    def __init__(self, display):
        self.display = display
        super().__init__(CLOCK_PIN, DATA_PIN, SWITCH_PIN, self.onRotated, self.onPressed)
        self.start()

    def onRotated(self, direction):
        if direction == KY040.CLOCKWISE:
            self.display.onRotaryNext()
        else:
            self.display.onRotaryPrevious()
    
    def onPressed(self):
        self.display.onRotaryPressed()