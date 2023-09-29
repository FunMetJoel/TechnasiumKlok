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
subState = 1

radio.config(group=177)
radio.on()

# Code in a 'while True:' loop repeats forever
while True:
    message = radio.receive()
    if message:
        #Format{Clr:255,255,255,000,000,000} 
        if (message[0:3] == "Clr"):
            print(message)
            print(message[4:7])
            print(message[8:11])
            print(message[12:15])
            print(message[16:19])
            print(message[20:23])
            print(message[24:27])
            colorScheme[0] = (int(message[4:7]),int(message[8:11]),int(message[12:15]))
            colorScheme[1] = (int(message[16:19]),int(message[20:23]),int(message[24:27]))
        elif(message[0:3] == "Mde"):
            subState = int(message.split(":")[1])

    
    if (state == 0):
        music.play(music.BA_DING)
        state = 1
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
            cl.ShowColorfade(LoopTimeFraction(3000), [(255,0,0),(0,0,0)])
    elif(state == 2):
        if(subState == 0):
            cl.ShowColorfade(LoopTimeFraction(3000), [colorScheme[0],colorScheme[0],colorScheme[0],colorScheme[0],colorScheme[0],colorScheme[0],(0,0,0),colorScheme[1],colorScheme[1],colorScheme[1],colorScheme[1],colorScheme[1],colorScheme[1],(0,0,0)])
        elif(subState == 1):
            pass
        else:
            cl.ShowColorfade(LoopTimeFraction(3000), [(255,0,0),(0,0,0)])

            

        
