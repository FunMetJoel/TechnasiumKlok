import microbit as mb
import neopixel
from color import Color

class Clock:
    def __init__(self, led_count:int, led_pin:mb._Pin):
        self.ledStrip:neopixel.NeoPixel = neopixel.NeoPixel(led_pin, led_count)
        self.ledStrip.clear()
        self.ledStrip.show()
        self.pixels:list[Color] = [Color(0, 0, 0) for _ in range(led_count)]
        self.brightness:float = 1

    def show(self):
        for i, color in enumerate(self.pixels):
            ncolor = color.setBrightness(self.brightness)
            self.ledStrip[i] = ncolor.to_rgb()
        self.ledStrip.show()

    def setPixel(self, index:int, color:Color):
        index = index % len(self.pixels)
        self.pixels[index] = color

    def setBrightness(self, brightness:float):
        self.brightness = brightness

    def clear(self):
        self.pixels = [Color(0, 0, 0) for _ in range(len(self.pixels))]
        
    def fill(self, color:Color):
        self.pixels = [color for _ in range(len(self.pixels))]

    def setAll(self, colors:list[Color]):
        self.pixels = colors

    def rotate(self, amount:int):
        self.pixels = self.pixels[-amount:] + self.pixels[:-amount]

    def shift(self, amount:int):
        self.pixels = [Color(0, 0, 0)] * amount + self.pixels[:-amount]

        

    


