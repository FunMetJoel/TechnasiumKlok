# Your new file!
import microbit as mb

timeOffset = 0

def getDayTime(t):
    offsetTime = t + timeOffset
    dayTime = offsetTime % (60 * 60 * 24)
    return dayTime

def setCurrentTime(h,m,s):
    global timeOffset
    desredTime = (h * 3600 + m * 60 + s)
    currentTime = mb.running_time() / 1000
    timeOffset = desredTime - currentTime

