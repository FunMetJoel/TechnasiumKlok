# Imports go at the top
from microbit import *
import neopixel
import time
import math

Truecolor = (0,137,133)
Falsecolor = (239,121,17)

def TimeToMs(uur, minuten, seconden):
    sec = 0
    sec += uur * 3600
    sec += minuten * 60
    sec += seconden
    ms = sec * 1000
    return ms

tijden = [
    TimeToMs(0, 0, 0),
    TimeToMs(0, 1, 0),
    TimeToMs(0, 2, 0),
    TimeToMs(8, 10, 0),
    TimeToMs(8, 55, 0),
    TimeToMs(9, 40, 0)
]

def TimeFraction(t):
    for i in range(0, len(tijden)):
        if time.ticks_diff(t, tijden[i]) < 0:
            timeSinceBel = time.ticks_diff(tijden[i-1], t)
            lenghtOfLesson = time.ticks_diff(tijden[i-1], tijden[i])
            return float(timeSinceBel/lenghtOfLesson)
    return float(0)

class colors:
    def __init__(self, _themecolors):
        self.themecolors = _themecolors

    @staticmethod
    def lerp(start_color, end_color, t):    
        # Extract the individual color channels (R, G, B) from start_color and end_color
        start_r, start_g, start_b = start_color
        end_r, end_g, end_b = end_color
    
        # Calculate the interpolated color channels
        interpolated_r = int(start_r + (end_r - start_r) * t)
        interpolated_g = int(start_g + (end_g - start_g) * t)
        interpolated_b = int(start_b + (end_b - start_b) * t)
    
        # Return the interpolated RGB color as a tuple
        return (interpolated_r, interpolated_g, interpolated_b)
        
    @staticmethod
    def PoligonLerp(lerpColors, t):
        colorCount = len(lerpColors)
        sideLength = 1/colorCount

        currentColorIndex = math.floor(t/sideLength)
        fadeamount = ((t%sideLength)*colorCount)

        colorResult = colors.lerp(lerpColors[currentColorIndex-1], lerpColors[currentColorIndex], fadeamount)
        return colorResult
        

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
                self.setLed(i,colors.lerp(Falsecolor, Truecolor, fadeamount))
            else:
                self.setLed(i,Falsecolor)

        self.np.show()

    def ShowRadarfade(self, t, Truecolor, Falsecolor):
        
        currLed = round(t*self.numLeds)
        for i in range(0, self.numLeds):
            self.setLed(i, brightness=0)

        cl.setLed(currLed-3, brightness=0.25)
        cl.setLed(currLed-2, brightness=0.50)
        cl.setLed(currLed-1, brightness=0.75)
        cl.setLed(currLed, brightness=1)
        cl.np.show()

        self.np.show()

    def ShowColorfade(self, t, fadecolors):
        for i in range(0, self.numLeds):
            self.setLed(i, colors.PoligonLerp(fadecolors, t) )
        
        self.np.show()

    def ShowStaticColorfade(self, fadecolors):
        for i in range(0, self.numLeds):
            self.setLed(i, colors.PoligonLerp(fadecolors, i/(self.numLeds+1)))
        self.np.show()

    def setLed(self, ledNum, color=(255,255,255), brightness=1.0):
        ledNum = self.numLeds - (ledNum%self.numLeds) - 23
        self.np[ledNum] = tuple([round(self.brightness*brightness*x) for x in color])
    
cl = Clock(24, 0.05)
# Code in a 'while True:' loop repeats forever
while True:
    currTime = time.ticks_ms()
    cl.ShowProgressBar(TimeFraction(currTime), Truecolor, Falsecolor)
    #cl.ShowRadarfade(TimeFraction(currTime), Truecolor, Falsecolor)
    #cl.ShowColorfade(TimeFraction(currTime), [(255,0,0),(0,255,0),(0,0,255)])
    #cl.ShowStaticColorfade([(255,0,0),(0,255,0),(0,0,255),(255,0,0),(0,255,0),(0,0,255)])

        
