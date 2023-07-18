# Imports go at the top
from microbit import *
import neopixel
import random

numLeds = 24
np = neopixel.NeoPixel(pin0, numLeds)
Truecolor = (255, 0, 0)
Falsecolor = (0, 0, 255)

tijden = [
    0,
    45
]

t = 720;

def RoundTime():
    for i in range(0, len(tijden)):
        if tijden[i] <= t:
            return float((t - tijden[i])/(tijden[i+1] - tijden[i]))

    return float(0)

def UpdateLeds():
    for i in range(0, numLeds):
        if (RoundTime() >= float(i/numLeds)):
            np[i] = Truecolor
        else:
            np[i] = Falsecolor
            
    np.show()

# Code in a 'while True:' loop repeats forever
while True:
    UpdateLeds()
    t = t + 1
    sleep(1000)
