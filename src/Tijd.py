# Your new file!
import time

def TimeToMs(uur, minuten, seconden):
    sec = 0
    sec += uur * 3600
    sec += minuten * 60
    sec += seconden
    ms = sec * 1000
    return ms

tijden = [
    TimeToMs(0, 0, 0),
    TimeToMs(0, 1, 0),
    TimeToMs(0, 2, 0),
    TimeToMs(8, 10, 0),
    TimeToMs(8, 55, 0),
    TimeToMs(9, 40, 0)
]

def TimeFraction(t):
    for i in range(0, len(tijden)):
        if time.ticks_diff(t, tijden[i]) < 0:
            timeSinceBel = time.ticks_diff(tijden[i-1], t)
            lenghtOfLesson = time.ticks_diff(tijden[i-1], tijden[i])
            return float(timeSinceBel/lenghtOfLesson)
    return float(0)