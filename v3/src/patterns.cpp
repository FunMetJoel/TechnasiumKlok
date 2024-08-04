#include "Patterns.h"
#include <cmath>
#include <Arduino.h>

String intToHex(int value) {
  String hexString = String(value, HEX);
  if (hexString.length() < 2) {
    hexString = "0" + hexString;
  }
  return hexString;
}

float lerp(float a, float b, float t)
{
  return a + (b - a) * t; //This returns a + t percent (t = 0.f is 0% and t = 1.f is 100%) of b
}


void freePatternMemory(byte** pattern, int rows) {
  for (int i = 0; i < rows; ++i) {
    delete[] pattern[i];
  }
  delete[] pattern;
}

// Helper function to create a 2D byte array with given rows and cols
byte** create2DArray(int rows, int cols) {
    byte** array = new byte*[rows];
    for (int i = 0; i < rows; ++i) {
        array[i] = new byte[cols];
    }
    return array;
}

// Implementation of the RainbowPattern generate function
byte** RainbowPattern::generate(float t) {
    const int cols = 3;
    byte** pattern = create2DArray(ledCount, cols);

    float reducedT = fmod((t + phaseShift) * speed, 1.0f);

    for (int i = 0; i < ledCount; ++i) {
        float phase = (i / static_cast<float>(ledCount)) - reducedT;
        pattern[i][0] = static_cast<byte>((sin(phase * 2.0f * M_PI) * 127.5f) + 127.5f); // Red
        pattern[i][1] = static_cast<byte>((sin((phase + 0.33f) * 2.0f * M_PI) * 127.5f) + 127.5f); // Green
        pattern[i][2] = static_cast<byte>((sin((phase + 0.66f) * 2.0f * M_PI) * 127.5f) + 127.5f); // Blue
    }

    return pattern;
}

String** RainbowPattern::getParameters() {
    numParameters = 3;
    String** parameters = new String*[numParameters];
    parameters[0] = new String[3]{ "speed", String(parameterType::FLOAT), String(speed) };
    parameters[1] = new String[3]{ "phaseShift", String(parameterType::FLOAT), String(phaseShift) };
    parameters[2] = new String[3]{ "timer", String(parameterType::FLOAT), String(1.0f / speed) };
    return parameters;
}

void RainbowPattern::setParameter(String name, String value) {
  if (name == "speed") {
    speed = value.toFloat();
  }
  else if (name == "phaseShift") {
    phaseShift = value.toFloat();
  }
  else if (name == "timer") {
    float timerLength = value.toFloat();
    speed = 1.0f / timerLength;
    phaseShift = fmod(millis(), 1.0f);
  }
}

// Implementation of the SolidPattern generate function
byte** SolidPattern::generate(float t) {
    const int cols = 3;
    byte** pattern = create2DArray(ledCount, cols);

    for (int i = 0; i < ledCount; ++i) {
        pattern[i][0] = red;
        pattern[i][1] = green;
        pattern[i][2] = blue;
    }

    return pattern;
}

String** SolidPattern::getParameters() {
    numParameters = 4;
    String** parameters = new String*[numParameters];
    parameters[0] = new String[3]{ "red", String(parameterType::BYTE), String(red) };
    parameters[1] = new String[3]{ "green", String(parameterType::BYTE), String(green) };
    parameters[2] = new String[3]{ "blue", String(parameterType::BYTE), String(blue) };
    parameters[3] = new String[3]{ "color", String(parameterType::COLOR), "#" + intToHex(red) + intToHex(green) + intToHex(blue) };
    return parameters;
}

void SolidPattern::setParameter(String name, String value) {
  if (name == "red") {
    red = value.toInt();
  } else if (name == "green") {
    green = value.toInt();
  } else if (name == "blue") {
    blue = value.toInt();
  } else if (name == "color") {
    // Hex to rgb

    red = (int)strtol(value.substring(0, 2).c_str(), NULL, 16);
    green = (int)strtol(value.substring(2, 4).c_str(), NULL, 16);
    blue = (int)strtol(value.substring(4, 6).c_str(), NULL, 16);
    Serial.println(String(value.substring(0, 2).c_str()) + ": " + String(red));
    Serial.println(String(value.substring(2, 4).c_str()) + ": " + String(green));
    Serial.println(String(value.substring(4, 6).c_str()) + ": " + String(blue));
  }
}

byte** LoadingPattern::generate(float t) {
  const int cols = 3;
  byte** pattern = create2DArray(ledCount, cols);

  float reducedT = fmod((t + phaseShift) * speed, 1.0f);
  float frondLedT = fmod(reducedT * ledCount, 1.0f);

  byte currentFrontled = static_cast<byte>(floor(reducedT * ledCount));

  for (int i = 0; i < ledCount; ++i) {
    if (i == currentFrontled) {
      pattern[i][0] = round(lerp(redB, redH, frondLedT));
      pattern[i][1] = round(lerp(greenB, greenH, frondLedT));
      pattern[i][2] = round(lerp(blueB, blueH, frondLedT));
    } else if (i == (currentFrontled-1) % ledCount) {
      pattern[i][0] = round(lerp(redH, redT, frondLedT));
      pattern[i][1] = round(lerp(greenH, greenT, frondLedT));
      pattern[i][2] = round(lerp(blueH, blueT, frondLedT));
    } else if (i < currentFrontled-1) {
      pattern[i][0] = redT;
      pattern[i][1] = greenT;
      pattern[i][2] = blueT;
    } else {
      pattern[i][0] = redB;
      pattern[i][1] = greenB;
      pattern[i][2] = blueB;
    }
  }

  return pattern;
}

String** LoadingPattern::getParameters() {
  numParameters = 6;
  String** parameters = new String*[numParameters];
  parameters[0] = new String[3]{ "speed", String(parameterType::FLOAT), String(speed) };
  parameters[1] = new String[3]{ "phaseShift", String(parameterType::FLOAT), String(phaseShift) };
  parameters[2] = new String[3]{ "HeadColor", String(parameterType::COLOR), "#" + intToHex(redH) + intToHex(greenH) + intToHex(blueH) };
  parameters[3] = new String[3]{ "TailColor", String(parameterType::COLOR), "#" + intToHex(redT) + intToHex(greenT) + intToHex(blueT) };
  parameters[4] = new String[3]{ "BackgroundColor", String(parameterType::COLOR), "#" + intToHex(redB) + intToHex(greenB) + intToHex(blueB) };
  parameters[5] = new String[3]{ "Timer", String(parameterType::FLOAT), String(1.0f / speed) };

  return parameters;
}

void LoadingPattern::setParameter(String name, String value) {
  if (name == "speed") {
    speed = value.toFloat();
  } else if (name == "phaseShift") {
    phaseShift = value.toFloat();
  } else if (name == "HeadColor") {
    redH = (int)strtol(value.substring(0, 2).c_str(), NULL, 16);
    greenH = (int)strtol(value.substring(2, 4).c_str(), NULL, 16);
    blueH = (int)strtol(value.substring(4, 6).c_str(), NULL, 16);
  } else if (name == "TailColor") {
    redT = (int)strtol(value.substring(0, 2).c_str(), NULL, 16);
    greenT = (int)strtol(value.substring(2, 4).c_str(), NULL, 16);
    blueT = (int)strtol(value.substring(4, 6).c_str(), NULL, 16);
  } else if (name == "BackgroundColor") {
    redB = (int)strtol(value.substring(0, 2).c_str(), NULL, 16);
    greenB = (int)strtol(value.substring(2, 4).c_str(), NULL, 16);
    blueB = (int)strtol(value.substring(4, 6).c_str(), NULL, 16);
  } else if (name == "Timer") {
    float timerLength = value.toFloat();
    speed = 1.0f / timerLength;
    phaseShift = fmod(millis(), 1.0f/speed);
  }
}
