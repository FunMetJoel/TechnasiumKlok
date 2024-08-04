#include <Arduino.h>
#include "patterns.h"

#ifndef WEBINTERFACE_H /* include guards */
#define WEBINTERFACE_H

void webinterface_setup(Pattern** newPatternsPtr);
void webinterface_loop(byte *currLed);

String SendHTML();

void handle_OnConnect();
void handle_setMode();
void handle_setParameter();
void handle_NotFound();
void handle_status();
void handle_getMode();

#endif /* WEBINTERFACE_H */