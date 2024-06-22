from abc import ABC, abstractmethod
from color import Color
from typing import Union

class Pattern(ABC):
    def __init__(self, num_leds:int):
        self.num_leds = num_leds
        self.params = {}

    def getParams(self):
        return self.params
    
    def setParams(self, params):
        self.params.update(params)

    @abstractmethod
    def getDescription(self) -> str:
        pass

    @abstractmethod
    def getColors(self, t:float) -> list[Color]:
        pass


class Rainbow(Pattern):
    def __init__(self, num_leds:int):
        super().__init__(num_leds)
        self.params = {'speed': 1}

    def getDescription(self) -> str:
        return 'retruns a rotating rainbow pattern'
    
    def getColors(self, t:float) -> list[Color]:
        speed = self.params['speed']
        colors = []
        for i in range(self.num_leds):
            hue = (t * speed + i) % 1
            colors.append(Color.from_hsv(hue * 360, 100, 100))
        return colors

    
class Solid(Pattern):
    def __init__(self, num_leds:int):
        super().__init__(num_leds)
        self.params = {
            'colorR': 0,
            'colorG': 0,
            'colorB': 0
        }

    def getDescription(self) -> str:
        return 'returns a solid color pattern'
    
    def getColors(self, t:float) -> list[Color]:
        return [self.params['color'] for _ in range(self.num_leds)]


class Gradient(Pattern):
    def __init__(self, num_leds:int):
        super().__init__(num_leds)
        self.params = {
            'startColorR': 0,
            'startColorG': 0,
            'startColorB': 0,
            'endColorR': 0,
            'endColorG': 0,
            'endColorB': 0
        }

    def getDescription(self) -> str:
        return 'returns a gradient pattern'
    
    def getColors(self, t:float) -> list[Color]:
        start_color = Color(self.params['startColorR'], self.params['startColorG'], self.params['startColorB'])
        end_color = Color(self.params['endColorR'], self.params['endColorG'], self.params['endColorB'])
        colors = []
        for i in range(self.num_leds):
            colors.append(Color.lerp(start_color, end_color, i/self.num_leds))
        return colors
    
class Snake:
    def __init__(self, num_leds:int):
        super().__init__(num_leds)
        self.params = {
            'color1R': 0,
            'color1G': 0,
            'color1B': 0,
            'color2R': 0,
            'color2G': 0,
            'color2B': 0,
            'speed': 1,
            'length': 3
        }

    def getDescription(self) -> str:
        return 'pattern with head and tail'
    
    def getColors(self, t:float) -> list[Color]:
        speed = self.params['speed']
        length = self.params['length']
        color1 = Color(self.params['color1R'], self.params['color1G'], self.params['color1B'])
        color2 = Color(self.params['color2R'], self.params['color2G'], self.params['color2B'])
        colors = []
        for i in range(self.num_leds):
            hue = (t * speed + i) % 1
            colors.append(Color.from_hsv(hue * 360, 100, 100))
        return colors

    
