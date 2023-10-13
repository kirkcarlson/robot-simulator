"""ROBOT MATH FUNCTIONS"""
import math

def constrain360( angle): # constrain angle to range (0,360)
    return angle % 360

def constrain180( angle): # constrain angle to range (-180,180)
    angle = constrain360( angle + 180) - 180

def atan360( adj, opp):  # find the angle 0..350 from x and y values
    if abs( adj) < 0.000005:
        angle = 0
    else:
        angle = math.degrees( math.atan (opp/adj))

    if opp >= 0 and adj >= 0: # NE quadrant            pygame SW quadrant
        angle += 0
    if adj < 0: # SE or SW quadrant                    pygame SE or NE quadrant
        angle += 180
    if opp < 0 and adj >=  0: # NW quadrant            pygame NW quadrant
        angle += 360
    return angle
