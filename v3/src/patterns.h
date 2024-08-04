#ifndef PATTERNS_H
#define PATTERNS_H

#include <cstdint>
#include <arduino.h>

enum parameterType{
  INT = 0,
  FLOAT = 1,
  BYTE = 2,
  COLOR = 3,
  PERCENTAGE = 4,
  BOOL = 5
};

void freePatternMemory(uint8_t** pattern, int rows);

class Pattern {
protected:
    int ledCount; // Number of LEDs in the pattern

public:
    String displayName;
    int numParameters;

    // Constructor to initialize ledCount
    explicit Pattern(String name, int count) : displayName(name), ledCount(count) {}

    virtual ~Pattern() = default;

    // Pure virtual function to generate a 2D byte array
    virtual byte** generate(float t) = 0;

    virtual String** getParameters() = 0;
    virtual void setParameter(String name, String value) = 0;
};

// Concrete class RainbowPattern
class RainbowPattern : public Pattern {
public:
    float speed = 1.0f;
    float phaseShift = 0.0f;

    // Constructor to initialize ledCount in the base class
    explicit RainbowPattern(int count) : Pattern("RotatingRainbow", count) {}

    ~RainbowPattern() override = default;

    // Override the generate function to implement the rainbow pattern
    byte** generate(float t) override;

    String** getParameters() override;
    void setParameter(String name, String value) override;
};

// Concrete class SolidPattern
class SolidPattern : public Pattern {
    byte red, green, blue;

public:
    // Constructor to initialize ledCount and RGB values
    explicit SolidPattern(int count, byte r, byte g, byte b) : Pattern("Solid", count), red(r), green(g), blue(b) {}

    ~SolidPattern() override = default;

    // Override the generate function to implement the solid pattern
    byte** generate(float t) override;

    String** getParameters() override;
    void setParameter(String name, String value) override;
};

class LoadingPattern : public Pattern {
    byte redH, greenH, blueH;
    byte redT, greenT, blueT;
    byte redB, greenB, blueB;
    float speed = 1.0f;
    float phaseShift = 0.0f;

public:
    explicit LoadingPattern(int count) : Pattern("Loading", count) {}

    ~LoadingPattern() override = default;

    byte** generate(float t) override;

    String** getParameters() override;
    void setParameter(String name, String value) override;
};

#endif // PATTERNS_H
