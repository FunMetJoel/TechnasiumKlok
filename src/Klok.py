# Imports go at the top
from microbit import *
import neopixel
import time
import math

numLeds = 24
np = neopixel.NeoPixel(pin0, numLeds)

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



class Clock:
    def __init__(self, _brightness):
        self.brightness = _brightness
    
    def ShowProgressBar(self, t, Truecolor, Falsecolor):
        ledFraction = 1/numLeds
        fullLeds = math.floor(t/ledFraction)
        fadeamount = ((t%ledFraction)*24)
        for i in range(0, numLeds):
            if (i <= 24-fullLeds):
                np[i-23] = tuple([round(self.brightness*x) for x in Truecolor])
            elif (i == 24-fullLeds+1):
                np[i-23] = tuple([round(self.brightness*x) for x in lerp(Truecolor, Falsecolor, fadeamount)])
                print(lerp(Falsecolor, Truecolor, fadeamount))
            else:
                np[i-23] = tuple([round(self.brightness*x) for x in Falsecolor])

        np.show()

    def ShowRGBfade(self, t):
        color = (1,1,1)
        for i in range(0, numLeds):
            np[i] = color


cl = Clock(0.05)
# Code in a 'while True:' loop repeats forever
while True:
    currTime = time.ticks_ms()
    cl.ShowProgressBar(TimeFraction(currTime), Truecolor, Falsecolor)
