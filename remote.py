# Imports go at the top
from microbit import *
import radio
import random

radio.config(group=177)
radio.on()

setting = 0

colorsToSend = [0,0,0,0,0,0]

def sendColor():
    r = colorsToSend[0]
    g = colorsToSend[1]
    b = colorsToSend[2]
    r2 = colorsToSend[3]
    g2 = colorsToSend[4]
    b2 = colorsToSend[5]
    print('Clr:' + "%03d"%r + ',' + "%03d"%g + ',' + "%03d"%b + ',' + "%03d"%r2 + ',' + "%03d"%g2 + ',' + "%03d"%b2)
    radio.send('Clr:' + "%03d"%r + ',' + "%03d"%g + ',' + "%03d"%b + ',' + "%03d"%r2 + ',' + "%03d"%g2 + ',' + "%03d"%b2)

display.show(setting)

# Code in a 'while True:' loop repeats forever
while True:
    if pin_logo.is_touched():
        setting = setting + 1
        if (setting == 10):
            setting = 0
        display.show(setting)
        sleep(250)

    if (setting >= 0 & setting <= 5):
        if button_b.is_pressed():
            colorsToSend[setting] += 1
            if (colorsToSend[setting] > 255):
                colorsToSend[setting] = 255
            sendColor()
        if button_a.is_pressed():
            colorsToSend[setting] -= 1
            if (colorsToSend[setting] < 0):
                colorsToSend[setting] = 0
            sendColor()
        
