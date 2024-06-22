# Your new file!
import math

def lerp(start_color, end_color, t):    
    # Extract the individual color channels (R, G, B) from start_color and end_color
    start_r, start_g, start_b = start_color
    end_r, end_g, end_b = end_color

    # Calculate the interpolated color channels
    interpolated_r = int(start_r + (end_r - start_r) * t)
    interpolated_g = int(start_g + (end_g - start_g) * t)
    interpolated_b = int(start_b + (end_b - start_b) * t)

    # Return the interpolated RGB color as a tuple
    return (interpolated_r, interpolated_g, interpolated_b)
    
def PoligonLerp(lerpColors, t):
    colorCount = len(lerpColors)
    sideLength = 1/colorCount

    currentColorIndex = math.floor(t/sideLength)
    fadeamount = ((t%sideLength)*colorCount)

    colorResult = lerp(lerpColors[currentColorIndex-1], lerpColors[currentColorIndex], fadeamount)
    return colorResult
    