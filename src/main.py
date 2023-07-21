# Imports go at the top
from microbit import *
from Tijd import *
from Clock import *

cl = Clock(24, 0.05)
# Code in a 'while True:' loop repeats forever
while True:
    #cl.ShowProgressBar(LoopTimeFraction(3000), Truecolor, Falsecolor)
    #cl.ShowRadarfade(LoopTimeFraction(3000), Truecolor, Falsecolor)
    #cl.ShowColorfade(LoopTimeFraction(3000), [(255,0,0),(0,255,0),(0,0,255)])
    #cl.ShowStaticColorfade([(255,0,0),(0,255,0),(0,0,255),(255,0,0),(0,255,0),(0,0,255)])
    #cl.ShowStaticColorfade([(0,255,0)])
    cl.RandomLeds()
    sleep(1000)

        
