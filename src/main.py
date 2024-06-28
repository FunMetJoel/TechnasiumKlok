import microbit as mb
from color import Color
from clock import Clock
from pattern import *
import music
import radio

NUM_LEDS = 24
LED_PIN = mb.pin0

patterns = {
    'rainbow': Rainbow,
    'solid': Solid,
    'gradient': Gradient,
    'snake': Snake
}
currentPattern = patterns['snake'](NUM_LEDS)
currentPattern.setParams(
    {
    'color1R': 255,
    'color1G': 0,
    'color1B': 0,
    'color2R': 0,
    'color2G': 255,
    'color2B': 0,
    'speed': 1,
    'length': 3
    }
)

commandStack = []

# 0 = start, 1 = running, 2 = paused, 3 = error
state = 0

nclock = Clock(NUM_LEDS, LED_PIN)

radio.config(group=177)
radio.on()

def setPattern(pattern:str):
    if pattern in patterns:
        currentPattern = (patterns[pattern](NUM_LEDS))
        return True
    else:
        return False

def mainUpdate():
    t = mb.running_time() / 1000
    colors = currentPattern.getColors(t)
    nclock.setAll(colors)
    nclock.show()

def startup():
    global state
    nclock.fill(Color(0, 0, 0))
    nclock.show()
    music.play(music.POWER_UP)
    state = 1
    

def error():
    nclock.fill(Color(255, 0, 0))
    nclock.show()
    music.play(music.POWER_DOWN)

def handleCommand(command:str):
    baseCommand = command.split(' ')[0]
    if baseCommand == 'pause':
        state = 2
    elif baseCommand == 'resume':
        state = 1
    elif baseCommand == 'stop':
        state = 3
    elif baseCommand == 'setPattern':
        result = setPattern(command.split(' ')[1])
        if not result:
            radio.send('error: invalid pattern')
    elif baseCommand == 'getParams':
        if currentPattern:
            radio.send(str(currentPattern.params))
        else:
            radio.send('error: no pattern set')
    elif baseCommand == 'setParam':
        if currentPattern:
            param = command.split(' ')[1]
            value = command.split(' ')[2]
            if param in currentPattern.params:
                currentPattern.params[param] = parseValue(value)
            else:
                radio.send('error: invalid param')
        else:
            radio.send('error: no pattern set')
    elif baseCommand == 'getPatterns':
        radio.send(str(list(patterns.keys())))
    else:
        pass

def parseValue(value:str):
    try:
        return int(value)
    except:
        try:
            return float(value)
        except:
            return value

def handleRadio():
    incoming = radio.receive()
    if incoming:
        commandStack.append(incoming)

while True:
    handleRadio()
    if len(commandStack) > 0:
        handleCommand(commandStack.pop(0))

    if state == 0:
        try:
            startup()
        except Exception as e:
            state = 3

    elif state == 1:
        try:
            mainUpdate()
        except Exception as e:
            print(e)
            state = 3
    
    elif state == 2:
        pass

    elif state == 3:
        error()
        break
        
    
