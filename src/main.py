# Imports go at the top
from microbit import *
from Tijd import *
from Clock import *

cl = Clock(24, 0.05)
# Code in a 'while True:' loop repeats forever
while True:
    currTime = time.ticks_ms()
    #cl.ShowProgressBar(TimeFraction(currTime), Truecolor, Falsecolor)
    cl.ShowRadarfade(TimeFraction(currTime), Truecolor, Falsecolor)
    #cl.ShowColorfade(TimeFraction(currTime), [(255,0,0),(0,255,0),(0,0,255)])
    #cl.ShowStaticColorfade([(255,0,0),(0,255,0),(0,0,255),(255,0,0),(0,255,0),(0,0,255)])

        
