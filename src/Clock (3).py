# Your new file!

from microbit import *
import neopixel
import math
import Colors
import random

Truecolor = (0,137,133)
Falsecolor = (239,121,17)

class Clock:
    def __init__(self, _numLeds, _brightness):
        self.numLeds = _numLeds
        self.brightness = _brightness
        self.pixels = [clPixel() for i in range(0, self.numLeds)]
        self.np = neopixel.NeoPixel(pin0, self.numLeds)
        self.ledFraction = 1/self.numLeds

    def RandomLeds(self, t, fadeMultiplyer):
        if(t < 0.02):
            self.setLed(random.randint(0, self.numLeds-1),color=(255, 255, 255) ,brightness=1)  
        
        for i in range(0, self.numLeds):
            self.pixels[i].A = self.pixels[i].A * fadeMultiplyer
        self.show()
    
    def ShowProgressBar(self, t, Truecolor, Falsecolor):
        fullLeds = math.floor(t/self.ledFraction)
        fadeamount = ((t%self.ledFraction)*24)
        
        for i in range(0, self.numLeds):
            if (i < fullLeds):
                self.setLed(i,Truecolor)
            elif (i == fullLeds):
                self.setLed(i,Colors.lerp(Falsecolor, Truecolor, fadeamount))
            else:
                self.setLed(i,Falsecolor)

        self.show()

    def ShowRadarfade(self, t, Truecolor, Falsecolor):
        
        currLed = round(t*self.numLeds)
        for i in range(0, self.numLeds):
            self.setLed(i, brightness=0)

        self.setLed(currLed-3, brightness=0.25)
        self.setLed(currLed-2, brightness=0.50)
        self.setLed(currLed-1, brightness=0.75)
        self.setLed(currLed, brightness=1)
        self.show()

    def ShowColorfade(self, t, fadecolors):
        for i in range(0, self.numLeds):
            self.setLed(i, Colors.PoligonLerp(fadecolors, t) )
        
        self.show()

    def ShowStaticColorfade(self, fadecolors):
        for i in range(0, self.numLeds):
            self.setLed(i, Colors.PoligonLerp(fadecolors, i/(self.numLeds+1)))
        self.show()

    def setLed(self, ledNum, color=(255,255,255), brightness=1.0):
        ledNum = ledNum%self.numLeds
        self.pixels[ledNum].R = color[0]
        self.pixels[ledNum].G = color[1]
        self.pixels[ledNum].B = color[2]
        self.pixels[ledNum].A = brightness

    def show(self):
        for i in range(0, self.numLeds):
            ledNum = self.numLeds - (i%self.numLeds) - 23
            hue = (self.pixels[i].R, self.pixels[i].G, self.pixels[i].B)
            self.np[ledNum] = tuple([round(self.brightness*self.pixels[i].A*x) for x in hue])

        self.np.show()


class clPixel:
    def __init__(self):
        self.R = 0
        self.G = 0
        self.B = 0
        self.A = 0.0