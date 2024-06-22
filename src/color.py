import math

class Color:
    def __init__(self, r:int, g:int, b:int):
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def from_hex(cls, hex:str):
        hex = hex.lstrip('#')
        return cls(*[int(hex[i:i+2], 16) for i in (0, 2, 4)])
    
    @classmethod
    def from_rgb(cls, r:int, g:int, b:int):
        return cls(r, g, b)
    
    @classmethod
    def from_hsv(cls, h:int, s:int, v:int):
        h, s, v = h/360, s/100, v/100
        i = math.floor(h * 6)
        f = (h * 6) - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        i %= 6
        if i == 0:
            return cls(v, t, p)
        if i == 1:
            return cls(q, v, p)
        if i == 2:
            return cls(p, v, t)
        if i == 3:
            return cls(p, q, v)
        if i == 4:
            return cls(t, p, v)
        if i == 5:
            return cls(v, p, q)
        
    def to_hex(self):
        return f'#{self.r:02x}{self.g:02x}{self.b:02x}'
    
    def to_rgb(self):
        return self.r, self.g, self.b
    
    def to_hsv(self):
        r, g, b = self.r/255, self.g/255, self.b/255
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin
        if delta == 0:
            h = 0
        elif cmax == r:
            h = 60 * (((g - b) / delta) % 6)
        elif cmax == g:
            h = 60 * (((b - r) / delta) + 2)
        elif cmax == b:
            h = 60 * (((r - g) / delta) + 4)
        if cmax == 0:
            s = 0
        else:
            s = delta / cmax
        v = cmax
        return h, s * 100, v * 100

    def __str__(self):
        return f'Color({self.r}, {self.g}, {self.b})'
    
    @classmethod
    def lerp(cls, color1, color2, t):
        return cls(
            math.floor(color1.r + (color2.r - color1.r) * t),
            math.floor(color1.g + (color2.g - color1.g) * t),
            math.floor(color1.b + (color2.b - color1.b) * t)
        )
    
    @classmethod
    def 