# Imports go at the top
from microbit import *
import radio
import time
radio.config(group=177)
radio.on()

timeoutTime = 10000
sendTime = time.ticks_ms()

# Code in a 'while True:' loop repeats forever
print('')
print('Started')
while True:
    INPUT = input(">")
    radio.send(INPUT)
    sendTime = time.ticks_ms()
    while (sendTime > time.ticks_ms() - timeoutTime):
        incoming = radio.receive()
        if incoming:
            if incoming == 'COMMANDEND':
                break
            else:
                print(incoming)
    
            
    
