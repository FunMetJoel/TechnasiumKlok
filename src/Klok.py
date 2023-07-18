# Imports go at the top
from microbit import *
import neopixel
import time

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
    TimeToMs(0, 0, 10),
    TimeToMs(8, 10, 0),
    TimeToMs(8, 55, 0),
    TimeToMs(9, 40, 0)
]

def TimeFraction(t):
    for i in range(0, len(tijden)):
        if time.ticks_diff(currTime, tijden[i]) < 0:
            timeSinceBel = time.ticks_diff(tijden[i-1], currTime)
            lenghtOfLesson = time.ticks_diff(tijden[i-1], tijden[i])
            return float(timeSinceBel/lenghtOfLesson)
    return float(0)

def UpdateLeds(t):
    for i in range(0, numLeds):
        if (TimeFraction(t) >= float(i/numLeds)):
            np[i] = Truecolor
        else:
            np[i] = Falsecolor
            
    np.show()

# Code in a 'while True:' loop repeats forever
while True:
    currTime = time.ticks_ms()
    print(TimeFraction(currTime))
    UpdateLeds(currTime)
