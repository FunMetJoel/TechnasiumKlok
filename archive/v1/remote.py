# Imports go at the top
from microbit import *
import radio

radio.config(group=177)
radio.on()

setting = 0
lastSetting = 0

settingNames = ["R", "G", "B", "r", "g", "b", "S"]
def settingName(index):
    if index < len(settingNames):
        return settingNames[index]
    else:
        return index

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

display.show(settingName(setting))

# Code in a 'while True:' loop repeats forever
while True:
    if pin_logo.is_touched():
        setting = setting + 1
        if (setting == 10):
            setting = 0
        display.show(settingName(setting))
        sleep(500)

    if (setting >= 0 and setting <= 5):
        #print(settingName(setting))
        if button_b.is_pressed():
            colorsToSend[setting] += 1
            if (colorsToSend[setting] > 255):
                colorsToSend[setting] = 255
            sendColor()
        if button_a.is_pressed():
            print(setting)
            colorsToSend[setting] -= 1
            if (colorsToSend[setting] < 0):
                colorsToSend[setting] = 0
            sendColor()
    if(settingName(setting) == "S"):
        if lastSetting != setting:
            print("Press A to start an interaction. Press B for help")
        if button_a.is_pressed():
            Input = input()
            for i in range(0,5):
                radio.send(Input)
                sleep(100)
        if button_b.is_pressed():
            print("Possible commands:")
            print("  Clr:RRR,GGG,BBB,rrr,ggg,bbb")
            print("   RRR ect zijn getallen tussen 0-255")
            print("   Bijv: Clr:255,100,050,210,002,102")
            sleep(1000)

    lastSetting = setting
