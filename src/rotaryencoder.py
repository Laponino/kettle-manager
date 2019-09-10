from ky040.KY040 import KY040

CLOCKPIN = 5
DATAPIN = 6
SWITCHPIN = 13

class RotaryEncoder(KY040):
    def __init__(self, display):
        self.display = display
        super().__init__(CLOCKPIN, DATAPIN, SWITCHPIN, self.onRotated, self.onPressed)

    def onRotated(self, direction):
        if direction == KY040.CLOCKWISE:
            self.onNext()
        else:
            self.onPrevious()

    def onNext(self):
        self.display.processDown()

    def onPrevious(self):
        self.display.processUp()
    
    def onPressed(self):
        self.display.pressEnter()