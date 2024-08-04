#include <Arduino.h>

#ifndef CLOCK_H /* include guards */
#define CLOCK_H

/* blinky initialization function */
void clock_setup();

/* blinks the LED once for an length of <ms> milliseconds. */
void clock_showPixels(byte colors[][3], float brightness = 0.1);

#endif /* CLOCK_H */