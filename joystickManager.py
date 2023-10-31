# manager for adding fuctionality and mapping of functions to joysticks
#### IMPORTS ####
import math
import rmath
import buttonManager


#### CONSTANTS ####
DEAD_ZONE = 0.0005

#### CLASSES ####
class Vector ():
    def __init__( self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.magnitude = 0

    def to_str( self):
        return f"x:{self.x: 4.2f} y:{self.x: 4.2f} ang:{self.angle: 6.2f} mag:{self.magnitude: 4.2f}"

class JoystickManager ():
    def __init__(self, joystick):
        self.joystick = joystick # raw joystick device
        self.buttonManager = buttonManager.ButtonManager( joystick) # execute actions on button presses
        self.rightJoy = Vector()
        self.leftJoy = Vector()
        self.hat = Vector()
        self.combinedJoyList = [ self.rightJoy, self.leftJoy, self.hat]
        self.combinedJoy = Vector()
        self.leftTrigger = 0
        self.rightTrigger = 0

    def setCombinedJoyList ( self, listOfJoys): # use non-zero joystick from list
        if not isinstance( listOfJoys, list):
            listOfJoys = list( listOfJoys)
        self.combinedJoyList = listOfJoys

    def update(self): # periodic update of joystick variables
        # robot movement with hat
        move = self.joystick.get_hat( 0)
        self.hat.x = move [0]
        self.hat.y = move [1] # positive is forward
        self.hat.angle = rmath.atan360( self.hat.x, self.hat.y)
        self.hat.magnitude = math.sqrt( self.hat.y * self.hat.y + self.hat.x * self.hat.x)

        # left stick
        self.leftJoy.x = self.joystick.get_axis(0)
        self.leftJoy.y = -self.joystick.get_axis(1) # negate to make forward positive
        if abs( self.leftJoy.x ) <= DEAD_ZONE:
            self.leftJoy.x = 0
        if abs( self.leftJoy.y ) <= DEAD_ZONE:
            self.leftJoy.y = 0
        self.leftJoy.angle = rmath.atan360( self.leftJoy.x, self.leftJoy.y)
        self.leftJoy.magnitude = math.sqrt( self.leftJoy.y * self.leftJoy.y + self.leftJoy.x * self.leftJoy.x)

        # right stick
        self.rightJoy.x = self.joystick.get_axis(3)
        self.rightJoy.y = -self.joystick.get_axis(4) # negate to make forward positive
        if abs( self.rightJoy.x ) <= DEAD_ZONE:
            self.rightJoy.x = 0
        if abs( self.rightJoy.y ) <= DEAD_ZONE:
            self.rightJoy.y = 0
        self.rightJoy.angle = rmath.atan360( self.rightJoy.x, self.rightJoy.y)
        self.rightJoy.magnitude = math.sqrt( self.rightJoy.y * self.rightJoy.y + self.rightJoy.x * self.rightJoy.x)

        # normalize the triggers
        self.leftTrigger =   (self.joystick.get_axis(2) + 1) / 2   # normalized to range 0..1
        if self.leftTrigger < DEAD_ZONE:
            self.leftTrigger = 0
        self.rightTrigger =  (self.joystick.get_axis(5) + 1) / 2   # normalized to range 0..1
        if self.rightTrigger < DEAD_ZONE:
            self.rightTrigger = 0

        # Execute joystick actions
        activeJoyButtons = []
        for joyButton in range (self.joystick.get_numbuttons()):
            if self.joystick.get_button( joyButton):
                activeJoyButtons.append( joyButton)
        self.buttonManager.update( activeJoyButtons)

        # this should be obsolete when editing complete
        self.combinedJoy = Vector() # reset it to zero
        for joy in self.combinedJoyList:
            if  abs( joy.magnitude) > 0:
                self.combinedJoy = joy
                break

    # this should be obsolete when editing complete
    def combineJoys (self, joyList): # take first non-zero joy from list of joys
        for joy in joyList:
            # could trap if joy is not instance of Vector
            try:
                if  joy.magnitude != 0:
                    return joy
            except:
                print ("Input to joystickManager.combineJoy is not a list of joys")
        joy = Vector ()
        return joy