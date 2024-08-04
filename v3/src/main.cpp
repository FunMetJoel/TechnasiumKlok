#include <Arduino.h>
#include "clock.h"
#include "webinterface.h"
#include "patterns.h"
#include "OTA.h"

byte colors[24][3] = {
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0},
  {0,0,0}
};

float brightness = 0.1;

byte currentPatternId = 0;
Pattern* patterns[4] = {
  new RainbowPattern(24),
  new SolidPattern(24, 255, 0, 0),
  new LoadingPattern(24),
  new SnakePattern(24)
};

void setup() {
  clock_setup();
  webinterface_setup(patterns);
  OTA_setup();
}

void loop() {
  clock_showPixels(colors, brightness);

  float t = millis() * 0.001f;
  webinterface_loop(&currentPatternId);

  byte** pattern = patterns[currentPatternId]->generate(t);
  for (int i = 0; i < 24; i++) {
    byte shiftedIndex = (i + 22) % 24;
    colors[shiftedIndex][0] = pattern[i][0];
    colors[shiftedIndex][1] = pattern[i][1];
    colors[shiftedIndex][2] = pattern[i][2];
  }

  freePatternMemory(pattern, 24);

  OTA_loop();
}