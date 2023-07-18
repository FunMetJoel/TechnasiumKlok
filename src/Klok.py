# Imports go at the top
from microbit import *
import neopixel
import time
import math

numLeds = 24
np = neopixel.NeoPixel(pin0, numLeds)
Truecolor = (255, 0, 0)
Falsecolor = (0, 0, 255)

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

def UpdateLeds(t):
    ledFraction = 1/numLeds
    fullLeds = math.floor(t/numLeds)
    fadeamount = ((t%ledFraction)*24)
    for i in range(0, numLeds):
        if (i <= fullLeds):
            np[i] = Truecolor
        elif (i == fullLeds+1):
            np[i] = lerp(Falsecolor, Truecolor, fadeamount)
            print(lerp(Falsecolor, Truecolor, fadeamount))
        else:
            np[i] = Falsecolor
    
    np.show()

# Code in a 'while True:' loop repeats forever
while True:
    currTime = time.ticks_ms()
    #print(TimeFraction(currTime))
    UpdateLeds(TimeFraction(currTime))
