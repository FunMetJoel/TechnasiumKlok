// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// Released under the GPLv3 license to match the rest of the
// Adafruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#include "clock.h"
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define PIN 5 
#define NUMPIXELS 24 

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500

void clock_setup() {

#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif

  pixels.begin(); 
}

// void clock_loop() {
//   pixels.clear(); // Set all pixel colors to 'off'

//   for(int i=0; i<NUMPIXELS; i++) { 
//     pixels.setPixelColor(i, pixels.Color(1, 0, 0));

//     pixels.show();

//     delay(DELAYVAL);
//   }
// }

void clock_showPixels(byte colors[][3], float brightness) {
    constrain(brightness, 0.0, 1.0);

    for(int i=0; i<NUMPIXELS; i++) {
        pixels.setPixelColor(23-i, pixels.Color(round(colors[i][0] * brightness), round(colors[i][1] * brightness), round(colors[i][2] * brightness)));
    }
    pixels.show();
}