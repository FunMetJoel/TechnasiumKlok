# Your new file!
import time

def CurrentTime():
    return time.ticks_ms()

def LoopTimeFraction(looptime):
    return (time.ticks_ms()%looptime)/looptime

def TimerFraction(startTime, targetTime):
    return time.ticks_diff(targetTime, time.ticks_add(time.ticks_ms(), -startTime)) / time.ticks_diff(startTime, targetTime)

def TimeToMs(uur, minuten, seconden):
    sec = 0
    sec += uur * 3600
    sec += minuten * 60
    sec += seconden
    ms = sec * 1000
    return ms

tijden = [
    TimeToMs(0, 0, 0),
    TimeToMs(0, 0, 10),
    TimeToMs(0, 2, 0),
    TimeToMs(8, 10, 0),
    TimeToMs(8, 55, 0),
    TimeToMs(9, 40, 0)
]

def ClassTimeFraction():
    for i in range(0, len(tijden)):
        if time.ticks_diff(time.ticks_ms(), tijden[i]) < 0:
            timeSinceBel = time.ticks_diff(tijden[i-1], time.ticks_ms())
            lenghtOfLesson = time.ticks_diff(tijden[i-1], tijden[i])
            return float(timeSinceBel/lenghtOfLesson)
    return float(0)