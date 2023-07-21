# Your new file!

from microbit import *
import neopixel
import math
import Colors

Truecolor = (0,137,133)
Falsecolor = (239,121,17)

 

class Clock:
    def __init__(self, _numLeds, _brightness):
        self.numLeds = 24
        self.brightness = _brightness
        self.np = neopixel.NeoPixel(pin0, self.numLeds)
        self.ledFraction = 1/self.numLeds
    
    def ShowProgressBar(self, t, Truecolor, Falsecolor):
        fullLeds = math.floor(t/self.ledFraction)
        fadeamount = ((t%self.ledFraction)*24)
        
        for i in range(0, self.numLeds):
            if (i <= fullLeds):
                self.setLed(i,Truecolor)
            elif (i == fullLeds+1):
                self.setLed(i,Colors.lerp(Falsecolor, Truecolor, fadeamount))
            else:
                self.setLed(i,Falsecolor)

        self.np.show()

    def ShowRadarfade(self, t, Truecolor, Falsecolor):
        
        currLed = round(t*self.numLeds)
        for i in range(0, self.numLeds):
            self.setLed(i, brightness=0)

        self.setLed(currLed-3, brightness=0.25)
        self.setLed(currLed-2, brightness=0.50)
        self.setLed(currLed-1, brightness=0.75)
        self.setLed(currLed, brightness=1)
        self.np.show()

    def ShowColorfade(self, t, fadecolors):
        for i in range(0, self.numLeds):
            self.setLed(i, Colors.PoligonLerp(fadecolors, t) )
        
        self.np.show()

    def ShowStaticColorfade(self, fadecolors):
        for i in range(0, self.numLeds):
            self.setLed(i, Colors.PoligonLerp(fadecolors, i/(self.numLeds+1)))
        self.np.show()

    def setLed(self, ledNum, color=(255,255,255), brightness=1.0):
        ledNum = self.numLeds - (ledNum%self.numLeds) - 23
        self.np[ledNum] = tuple([round(self.brightness*brightness*x) for x in color])
   
