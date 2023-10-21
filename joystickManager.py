# manager for adding fuctionality and mapping of functions to joysticks
#### IMPORTS ####
import math
import rmath
import chord


#### CONSTANTS ####
DEAD_ZONE = 0.0005

#### CLASSES ####
class vector ():
    def __init__( self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.magnitude = 0

    def to_str( self):
        return f"x:{self.x: 4.2f} y:{self.x: 4.2f} ang:{self.angle: 6.2f} mag:{self.magnitude: 4.2f}"

class joystickManager ():
    def __init__(self, joystick):
        self.joystick = joystick # raw joystick device
        self.chord = chord.Chord() # button manager to execute actions on button presses
        self.rightJoy = vector()
        self.leftJoy = vector()
        self.hat = vector()
        self.lefTrigger = 0
        self.rightTrigger = 0


    def check(self): # periodic update of joystick variables
        # robot movement with hat
        move = self.joystick.get_hat( 0)
        #joyX = move[0]
        #joyY = move[1] # positive is up
        #joyAngle = rmath.atan360 ( joyY, joyX)
        self.hat.x = move [0]
        self.hat.y = move [1] # positive is forward
        self.hat.angle = rmath.atan360( self.hat.y / self.hat.x)
        self.hat.magnitude = math.sqrt( self.hat.y * self.hat.y + self.hat.x * self.hat.x)

        # left stick
        #horiz_move = joystick.get_axis(0)
        #vert_move =  -joystick.get_axis(1) # negative to make positive up
        #if abs(vert_move) >= minJoy or abs(horiz_move) >= minJoy: #over ride joyX and joyY
        #    joyX = horiz_move
        #    joyY = -vert_move # for common code below
        #    joyAngle = rmath.joyatan360 ( -joyY, joyX)
        self.leftJoy.x = self.joystick.get_axis(0)
        self.leftJoy.y = -self.joystick.get_axis(1) # negate to make forward positive
        if abs( self.leftJoy.x ) <= DEAD_ZONE:
            self.leftJoy.x = 0
        if abs( self.leftJoy.y ) <= DEAD_ZONE:
            self.leftJoy.y = 0
        if self.leftJoy.x != 0 or self.leftJoy.y != 0:
            self.leftJoy.angle = rmath.atan360( self.leftJoy.y / self.leftJoy.x)
            self.leftJoy.magnitude = math.sqrt( self.leftJoy.y * self.leftJoy.y + self.leftJoy.x * self.leftJoy.x)
        else:
            self.leftJoy.angle = 0
            self.leftJoy.magnitude = 0

        # right stick
        #horiz_move = joystick.get_axis(3)
        #vert_move =  -joystick.get_axis(4) # negative to make positive up
        #if abs(vert_move) >= minJoy or abs(horiz_move) >= minJoy: #over ride joyX and joyY
        #    joyX = horiz_move
        #    joyY = -vert_move # for common code below
        #    joyAngle = rmath.joyatan360 ( -joyY, joyX)
        self.rightJoy.x = self.joystick.get_axis(3)
        self.rightJoy.y = -self.joystick.get_axis(4) # negate to make forward positive
        if abs( self.rightJoy.x ) <= DEAD_ZONE:
            self.rightJoy.x = 0
        if abs( self.rightJoy.y ) <= DEAD_ZONE:
            self.rightJoy.y = 0
        if self.rightJoy.x != 0 or self.rightJoy.y != 0:
            self.rightJoy.angle = rmath.atan360( self.rightJoy.y / self.rightJoy.x)
            self.rightJoy.magnitude = math.sqrt( self.rightJoy.y * self.rightJoy.y + self.rightJoy.x * self.rightJoy.x)
        else:
            self.rightJoy.angle = 0
            self.rightJoy.magnitude = 0

        # normalize the triggers
        self.leftTrigger =   (joystick.get_axis(2) + 1) / 2   # normalized to 0..1
        self.rightTrigger =  (joystick.get_axis(5) + 1) / 2   # normalized to 0..1

        # Execute joystick actions
        activeJoyButtons = []
        for joyButton in range (joystick.get_numbuttons()):
            #print(f" hi {joyButton} {activeJoyButtons} {joystick.get_button( joyButton)}")
            if joystick.get_button( joyButton):
                #print (f"button {joyButton} is active {activeJoyButtons}")
                activeJoyButtons.append( joyButton)
        #print(f" hi {activeJoyButtons} {joystick.get_numbuttons()}" )
        #joyManager.buttonList = activeJoyButtons
        self.chord.check( activeJoyButtons) # and execute actions