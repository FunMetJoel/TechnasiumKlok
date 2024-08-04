from color import Color
import math
import timeManager

class Pattern():
    def __init__(self, num_leds:int):
        self.num_leds = num_leds
        self.params = {}

    def getParams(self):
        return self.params
    
    def setParams(self, params):
        self.params.update(params)

    def getDescription(self) -> str:
        pass

    def getColors(self, t:float):
        pass


class Rainbow(Pattern):
    def __init__(self, num_leds:int):
        super().__init__(num_leds)
        self.params = {'speed': 1}

    def getDescription(self) -> str:
        return 'retruns a rotating rainbow pattern'
    
    def getColors(self, t:float):
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
            'colorR': 255,
            'colorG': 255,
            'colorB': 255
        }

    def getDescription(self) -> str:
        return 'returns a solid color pattern'
    
    def getColors(self, t:float):
        color = Color(self.params['colorR'], self.params['colorG'], self.params['colorB'])
        return [color for _ in range(self.num_leds)]


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
    
    def getColors(self, t:float):
        start_color = Color(self.params['startColorR'], self.params['startColorG'], self.params['startColorB'])
        end_color = Color(self.params['endColorR'], self.params['endColorG'], self.params['endColorB'])
        colors = []
        for i in range(self.num_leds):
            colors.append(Color.lerp(start_color, end_color, i/self.num_leds))
        return colors
    
class Snake(Pattern):
    def __init__(self, num_leds:int):
        super().__init__(num_leds)
        self.params = {
            'color1R': 255,
            'color1G': 0,
            'color1B': 0,
            'color2R': 0,
            'color2G': 255,
            'color2B': 0,
            'speed': 1,
            'length': 3
        }

    def getDescription(self) -> str:
        return 'pattern with head and tail'
    
    def getColors(self, t:float):
        speed = self.params['speed']
        length = self.params['length']
        color1 = Color(self.params['color1R'], self.params['color1G'], self.params['color1B'])
        color2 = Color(self.params['color2R'], self.params['color2G'], self.params['color2B'])
        colors = []
        currentFrontLed = int(math.floor(((t * speed) % 1)*self.num_leds))
        for i in range(self.num_leds):
            if currentFrontLed == i:
                colors.append(color1)
            elif ( (currentFrontLed - i) % self.num_leds < length ):
                colors.append(color2)
            else:
                colors.append(Color(0,0,0))
            
        return colors

class ShowTime(Pattern):
    def __init__(self, num_leds:int):
        super().__init__(num_leds)
        self.params = {
            'color1R': 255,
            'color1G': 0,
            'color1B': 0,
            'color2R': 0,
            'color2G': 255,
            'color2B': 0
        }

    def getDescription(self) -> str:
        return 'Shows hour and minute hands'
    
    def getColors(self, t:float):
        speed = self.params['speed']
        length = self.params['length']
        color1 = Color(self.params['color1R'], self.params['color1G'], self.params['color1B'])
        color2 = Color(self.params['color2R'], self.params['color2G'], self.params['color2B'])
        colors = []
        currentHour = (timeManager.getDayTime(t) / (60*60*24)) % 24
        current12Hour = currentHour % 12
        for i in range(self.num_leds):
            
            if ((current12Hour ) % 12)* 2 == i:
                colors.append(color1)
            else:
                colors.append(Color(0,0,0))
            
        return colors
