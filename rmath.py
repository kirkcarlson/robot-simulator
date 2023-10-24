"""ROBOT MATH FUNCTIONS"""
import math

DEBUG = False

def dprint( string):
    if DEBUG:
        print(string)

dprint ("starting up")

def constrain360( angle): # constrain angle to range (0,360)
    return angle % 360

def constrain180( angle): # constrain angle to range (-180,180)
    return constrain360( angle + 180) - 180



def atan360( x, y):  # find the angle 0..360 from joystick x and -y values
    # opp is x and adj is y
    if abs( x) < 0.000005:
        angle = 0
    elif abs(y) < 0.000005:
        if (x >= 0) ^ (y >= 0):
            angle = -90
        else:
            angle =  90
    else:
        angle = math.degrees( math.atan (x/y))

    if y < 0:  # SW or SE quadrants                    pygame SE or NE quadrant
        angle = 180 + angle
    elif y>=0 and x<0:
        angle = 360 + angle
    #angle = constrain360( angle)
    #dprint ( f"{x: 7.2f} {y: 7.2f} {angle: 7.2f}")
    return angle


#           expected (0 top cw)                                atan360 (x/y)
sqrt3 = math.sqrt(3)
dprint ( f"   0 {math.degrees( math.atan(  0.0001)): > 7.2f}  {atan360(  0,     1): > 7.2f}") # NE
dprint ( f"  30 {math.degrees( math.atan( 1/sqrt3)): > 7.2f}  {atan360(  1, sqrt3): > 7.2f}")
dprint ( f"  45 {math.degrees( math.atan(       1)): > 7.2f}  {atan360(  1,     1): > 7.2f}")
dprint ( f"  60 {math.degrees( math.atan(   sqrt3)): > 7.2f}  {atan360(  sqrt3, 1): > 7.2f}")
dprint ( f"  90 {math.degrees( math.atan(  999999)): > 7.2f}  {atan360(  1, 0.0001): > 7.2f}")
dprint ( f"  91 {math.degrees( math.atan( -999999)): > 7.2f}  {atan360(  1,-0.0001): > 7.2f}") #SE
dprint ( f" 120 {math.degrees( math.atan(  -sqrt3)): > 7.2f}  {atan360(  sqrt3,-1): > 7.2f}")
dprint ( f" 135 {math.degrees( math.atan(      -1)): > 7.2f}  {atan360(  1,    -1): > 7.2f}")
dprint ( f" 150 {math.degrees( math.atan(-1/sqrt3)): > 7.2f}  {atan360(  1,-sqrt3): > 7.2f}")
dprint ( f" 180 {math.degrees( math.atan(  0.0001)): > 7.2f}  {atan360(  0.0001,-1): > 7.2f}")
dprint ( f" 181 {math.degrees( math.atan(  0.0001)): > 7.2f}  {atan360( -0.0001,-1): > 7.2f}") #SW
dprint ( f" 210 {math.degrees( math.atan( 1/sqrt3)): > 7.2f}  {atan360( -1, -sqrt3): > 7.2f}")
dprint ( f" 225 {math.degrees( math.atan(       1)): > 7.2f}  {atan360( -1,    -1): > 7.2f}")
dprint ( f" 240 {math.degrees( math.atan(   sqrt3)): > 7.2f}  {atan360( -sqrt3, -1): > 7.2f}")
dprint ( f" 270 {math.degrees( math.atan(  999999)): > 7.2f}  {atan360( -1,-0.0001): > 7.2f}")
dprint ( f" 271 {math.degrees( math.atan( -999999)): > 7.2f}  {atan360( -1, 0.0001): > 7.2f}") #NW
dprint ( f" 300 {math.degrees( math.atan(  -sqrt3)): > 7.2f}  {atan360( -sqrt3, 1): > 7.2f}")
dprint ( f" 315 {math.degrees( math.atan(      -1)): > 7.2f}  {atan360( -1,     1): > 7.2f}")
dprint ( f" 330 {math.degrees( math.atan(-1/sqrt3)): > 7.2f}  {atan360( -1, sqrt3): > 7.2f}")
dprint ( f" 359 {math.degrees( math.atan( -0.0001)): > 7.2f}  {atan360( -0.0001, 1): > 7.2f}")
dprint(f" -90 constrain180:{constrain180(-90)}")
dprint(f"-180 constrain180:{constrain180(-180)}")
dprint(f"   0 constrain180:{constrain180(0)}")
dprint(f"  90 constrain180:{constrain180(90)}")
dprint(f"-180 constrain180:{constrain180(180)}")
dprint( "done")