"""ROBOT MATH FUNCTIONS"""
import math

DEBUG = False

def dprint( string):
    if DEBUG:
        print(string)

def constrain360( angle): # constrain angle to range (0,360)
    return angle % 360

def constrain180( angle): # constrain angle to range (-180,180)
    angle = constrain360( angle + 180) - 180

def atan360( opp, adj):  # find the angle 0..360 from x and y values
    # opp is y and adj is x
    if abs( adj) < 0.000005:
        angle = 0
    elif abs(opp) < 0.000005:
        if (opp > 0) ^ (adj > 0):
            angle = 90
        else:
            angle = -90
    else:
        angle = math.degrees( math.atan (opp/adj))

    if opp >= 0 and adj >= 0: # NE quadrant            pygame SW quadrant
        angle += 0
    if opp < 0: # SE or SW quadrant                    pygame SE or NE quadrant
        angle += 180
    if adj < 0 and opp >=  0: # NW quadrant            pygame NW quadrant
        angle += 360
    dprint ( f"{opp: 7.2f} {adj: 7.2f} {angle: 7.2f}")
    return angle


def joyatan360( opp, adj):  # find the angle 0..360 from joystick x and -y values
    # opp is y and adj is x
    if abs( adj) < 0.000005:
        angle = 0
    elif abs(opp) < 0.000005:
        if (opp > 0) ^ (adj > 0):
            angle = 90
        else:
            angle = -90
    else:
        angle = math.degrees( math.atan (opp/adj)) + 90

    if adj < 0:  # SW or NW quadrants                    pygame SE or NE quadrant
        angle += 180
    angle = constrain360( angle)
    #dprint ( f"{opp: 7.2f} {adj: 7.2f} {angle: 7.2f}")
    return angle


#           expected (0 top cw)                                atan360 (y/x)
dprint ( f"   0 {math.degrees( math.atan(  0.0001)): > 7.2f}  {atan360(  1,  0): > 7.2f}")
dprint ( f"  45 {math.degrees( math.atan(       1)): > 7.2f}  {atan360(  1,  1): > 7.2f}")
dprint ( f"  90 {math.degrees( math.atan(  999999)): > 7.2f}  {atan360(  0,  1): > 7.2f}")
dprint ( f"  91 {math.degrees( math.atan( -999999)): > 7.2f}  {atan360(  0,  1): > 7.2f}")
dprint ( f" 135 {math.degrees( math.atan(      -1)): > 7.2f}  {atan360( -1,  1): > 7.2f}")
dprint ( f" 180 {math.degrees( math.atan(  0.0001)): > 7.2f}  {atan360( -1,  0): > 7.2f}")
dprint ( f" 225 {math.degrees( math.atan(       1)): > 7.2f}  {atan360( -1, -1): > 7.2f}")
dprint ( f" 270 {math.degrees( math.atan( -999999)): > 7.2f}  {atan360(  0, -1): > 7.2f}")
dprint ( f" 315 {math.degrees( math.atan(      -1)): > 7.2f}  {atan360(  1, -1): > 7.2f}")
