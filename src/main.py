# Imports go at the top
from microbit import *
from Tijd import *
from Clock import *
import music
import radio

cl = Clock(24, 0.05)
lt = 0.0

colorScheme = [(0,137,133),(239,121,17)]

state = 0 #0: lost Energy, 1: calibrated, 2: settings
subState = 0

radio.config(group=177)
radio.on()

# Code in a 'while True:' loop repeats forever
while True:
    message = radio.receive()
    if message:
        display.scroll(message)
    
    if (state == 0):
        music.play(music.BA_DING)
        state = 2
    elif(state == 1):
        if(subState == 0):
            cl.ShowProgressBar(LoopTimeFraction(3000), colorScheme[0], colorScheme[1])
        elif(subState == 1):
            cl.ShowRadarfade(LoopTimeFraction(3000), colorScheme[0], colorScheme[1])
        elif(subState == 2):
            cl.ShowColorfade(LoopTimeFraction(3000), [(255,0,0),(0,255,0),(0,0,255)])
        elif(subState == 3):
            cl.ShowStaticColorfade([(255,0,0),(0,255,0),(0,0,255),(255,0,0),(0,255,0),(0,0,255)])
        elif(subState == 4):
            cl.ShowStaticColorfade([(0,255,0)])
        elif(subState == 5):
            cl.RandomLeds(LoopTimeFraction(250), 0.99)
        else:
            cl.ShowStaticColorfade([(255,0,0)])
    elif(state == 2):
        if(subState == 0):
            cl.ShowStaticColorfade([colorScheme[0],colorScheme[0],colorScheme[0],colorScheme[0],colorScheme[0],colorScheme[0],colorScheme[1],colorScheme[1],colorScheme[1],colorScheme[1],colorScheme[1],colorScheme[1]])
        elif(subState == 1):
            pass
            

        
