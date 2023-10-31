#### IMPORTS ####
import math
import rmath
import pygame
import mode
import info
import joystickManager

#### CONSTANTS ####
MAX_ROBOT_SPEED = 5  #need to scale this to be 16 feet per second
                     # field is 84 feet long so 7.7 seconds to traverse

spinSpeedModes = [ 0.5, 1, 2,5, 5 ]
spinSpeedLow     = 0
spinSpeedMedium  = 1
spinSpeedHigh    = 2
spinSpeedExtreme = 3

# elevatorMode values
'''
tower control              arm extend  elevator
preset 0: stow point       0           deck
preset 1: floor pickup     low         floor
preset 2: station pickup   low         med
preset 3: low stand        low         floor
preset 4: medium stand     med         med
preset 5: high stand       high        high
'''
elevatorModes = [ "stowed", "floor pickup", "low", "medium", "high"]
elevatorStowed            = 0
elevatorFloorPickupMode   = 1
elevatorStationPickupMode = 2
elevatorLowMode           = 3
elevatorMediumMode        = 4
elevatorHighMode          = 5

#rotationMode values
rotationModes = [ "manual", "tank", "tank field mode", "to front", "to north", "to south", "to east", "to west", "spin CW", "spin CCW"]
manualRotationMode  = 0
tankMode            = 1
tankFieldMode       = 2
autoRotateFrontMode = 3
autoRotateNorthMode = 4
autoRotateSouthMode = 5
autoRotateEastMode  = 6
autoRotateWestMode  = 7
spinCWMode          = 8
spinCCWMode         = 9


#### VARIABLES ####


#### CLASSES ####
'''Robot class for robots in simulator'''
class Robot(pygame.sprite.Sprite):
    def __init__(self, joystick, position=(0, 0), color= "white"):
        super(Robot, self).__init__()
        self.color = color
        self.original_image = pygame.Surface((32, 32))
        #pygame.draw.lines(self.original_image, robotColor, True, [( 0,0),  (31,0),  (31,13), (8,13),
        #                                                            (8,9),   (4,9),   (4,21), (8,21),
        #                                                            (9,17), (31,17), (31,31), (0,31)])
        # ideally the following line should be passed to the __init__ method to
        # allow different robot shapes
        pygame.draw.lines(self.original_image, self.color, True, [( 0,0),  (31,0),  (31,31),  (0,31),
                                                                   ( 0,17), (23,17), (23,21), (27,21),
                                                                   (27,9),  (23,9),  (23,13),  (0,13)])
        self.image = self.original_image  # This will reference our rotated copy.
        self.rect  = self.image.get_rect()
        self.joystick = joystick # joystick object used to control robot motions.
        self.joystickManager = joystickManager.JoystickManager( joystick) # assocates joystick with joystick manager
        self.driveByJoy= None # pointer to a particular function and joysticks
        self.info  = None     # information area assiciated with this robot
        self.driveByAxis = None # list of methods to monitor axis values
        self.position = pygame.math.Vector2(*position)
        self.pointing = 0  # direction that the robot is pointing
        self.heading = 0  # directon in which the robot is moving
        self.spinSpeedMode = mode.Mode ( spinSpeedModes)
        self.elevatorMode = mode.Mode ( elevatorModes)
        self.rotationMode = mode.CommandMode ( rotationModes, [  # define commands for each mode
            lambda joy : self.driveByJoystickNoRotation( joy),
            lambda joy : self.driveByJoystickTankMode( joy),
            lambda joy : self.driveByJoystickTankFieldMode( joy),
            lambda joy : self.driveByJoystickRotateToFront( joy),
            lambda joy : self.driveByJoystickRotateToNorth( joy),
            lambda joy : self.driveByJoystickRotateToSouth( joy),
            lambda joy : self.driveByJoystickRotateToEast( joy),
            lambda joy : self.driveByJoystickRotateToWest( joy),
            lambda joy : self.driveByJoystickRotateCW( joy),
            lambda joy : self.driveByJoystickRotateCCW( joy),
        ])
        self.driveByCommands = []
        self.special = ""


    def update(self):
        ''' This method relies on commands set to particular lamda functions.
        This makes the method independent on what is being done.
        Its primary purpose is to pass joystick commands to particular commands.

        thinking through this a bit more...
        each driveByJoystick function can be controlled by one or more joysticks or individual axis
        each axis can be normalized to be 0..1 instead of -1..1
        this would be a list of tuples like:
        [(command, joy),...] or [(command, axis)...]
        or it could be a list of lambda functions like:
        [lamda input : command( input),...]
        the "input" could be a raw .joy attribute or it could be a .combined([listOfJoys])
        let's try this first...
        '''
        # update keys and axis before joysticks to give them a little priority
        self.joystickManager.check() # update the since commands have same code
        for command in self.driveByAxis:
            command()

        self.driveByJoystick () # this should just be self.rotationMode.command  or one of the driveByCommands

        # Create the rotated copy of the robot.
        # py image has y down and 0 to the right, hence 90-angle
        self.image = pygame.transform.rotate(self.original_image, rmath.constrain360( 90-self.pointing)).convert()  # Angle is absolute value!

        # Make sure your rect represent the actual Surface.
        self.rect = self.image.get_rect()

        # Since the dimension probably changed you should move its center back to where it was.
        self.rect.center = self.position.x, self.position.y

        # keep the robot on the field
        robotMinX, robotMinY, robotWidth, robotHeight = self.rect 
        robotMaxX = robotMinX + robotWidth
        robotMaxY = robotMinY + robotHeight
        x = self.position.x
        y = self.position.y
        displayWidth, displayHeight = pygame.display.get_surface().get_size()
        if robotMinX < 0:
            self.position.x = robotWidth / 2
        if robotMaxX > displayWidth:
            self.position.x = displayWidth - robotWidth /2
        if robotMinY < 0:
            self.position.y = 0 + robotHeight /2
        if robotMaxY > displayHeight: 
            self.position.y = displayHeight - robotHeight /2
            

    def _turnToward( self, angle):
        diff = rmath.constrain360( self.pointing - angle)
        if abs( diff ) > self.spinSpeedMode.current():
            if diff > 0 and diff <180:
                self.pointing = rmath.constrain360( self.pointing - self.spinSpeedMode.current())
            else:
                self.pointing = rmath.constrain360( self.pointing + self.spinSpeedMode.current())
        else:
            self.pointing = angle
            

    def driveByJoystickNoRotation( self, joy):
        # joy.magnitude and joy.angle is used as a unit vector, rather than joy.x and joy.y which distort the vector'''
        if joy.magnitude > 0:
            self.position.x += joy.magnitude * MAX_ROBOT_SPEED * math.sin( math.radians( joy.angle))
            self.position.y -= joy.magnitude * MAX_ROBOT_SPEED * math.cos( math.radians( joy.angle))


    def driveByJoystickRotateToFront( self, joy):
        if joy.magnitude > 0:
            self.heading = joy.angle
            self._turnToward( self.heading)
            self.driveByJoystickNoRotation( joy)


    def driveByJoystickRotateCW( self, joy):
        if joy.magnitude > 0:
            self.heading = joy.angle
            self._turnToward( self.pointing + self.spinSpeedMode.current())  # rotate clockwise
            self.driveByJoystickNoRotation( joy)


    def driveByJoystickRotateCCW( self, joy):
        if joy.magnitude > 0:
            self.heading = joy.angle
            self._turnToward( self.pointing - self.spinSpeedMode.current())  # rotate counter clockwise
            self.driveByJoystickNoRotation( joy)


    def driveByJoystickTankMode( self, joy):
        # tank mode, joystick y ==> forward/backward speed, joystick x ==> turn left/right
        if joy.magnitude > 0:
            self._turnToward( self.pointing + self.spinSpeedMode.current()  * joy.x)
            self.heading = self.pointing
            self.position.x += (math.sin( math.radians(self.heading)) * joy.y * MAX_ROBOT_SPEED)
            self.position.y -= (math.cos( math.radians(self.heading)) * joy.y * MAX_ROBOT_SPEED) # y is down on the screen


    def driveByJoystickTankFieldMode( self, joy):
        if joy.magnitude > 0:
            self._turnToward( joy.angle)
            self.heading = self.pointing
            self.position.x += math.sin( math.radians(self.heading)) * joy.magnitude * MAX_ROBOT_SPEED
            self.position.y -= math.cos( math.radians(self.heading)) * joy.magnitude * MAX_ROBOT_SPEED # y is down on screen

            ''' may be start code for an auto reverse, doesn't work as it is
            diff = rmath.constrain180( self.pointing - self.joy.angle)
            if abs(diff) > 120:
                self._turnToward( self.joy.angle)
                self.position.x += math.sin( math.radians(self.heading)) * self.joy.magnitude * MAX_ROBOT_SPEED
                self.position.y -= math.cos( math.radians(self.heading)) * self.joy.magnitude * MAX_ROBOT_SPEED # y is down on screen
            else: #auto reverse .... doesn't quite work right. oscillates
                self._turnToward( self.joy.angle + 180 )
                self.position.x -= (math.sin( math.radians(self.heading) ) * self.joy.magnitude * MAX_ROBOT_SPEED)
                self.position.y += (math.cos( math.radians(self.heading) ) * self.joy.magnitude * MAX_ROBOT_SPEED)
            '''

   
    def driveByJoystickRotateToNorth( self, joy):
        if joy.magnitude > 0:
            self.heading = joy.angle
            self._turnToward( 0)
            self.driveByJoystickNoRotation( joy)


    def driveByJoystickRotateToEast( self, joy):
        if joy.magnitude > 0:
            self.heading = joy.angle
            self._turnToward( 90)
            self.driveByJoystickNoRotation( joy)


    def driveByJoystickRotateToSouth( self, joy):
        if joy.magnitude > 0:
            self.heading = joy.angle
            self._turnToward( 180)
            self.driveByJoystickNoRotation( joy)
        

    def driveByJoystickRotateToWest( self, joy):
        if joy.magnitude > 0:
            self.heading = joy.angle
            self._turnToward( 270)
            self.driveByJoystickNoRotation( joy)


    def turnCW( self):
        self._turnToward( self.pointing + self.spinSpeedMode.current())
        if self.rotationMode.mode == tankMode or self.rotationMode.mode == tankFieldMode:
            self.heading = self.pointing
        else:
            self.rotationMode.setMode(manualRotationMode ) # turn off auto rotation

        
    def turnCCW( self):
        self._turnToward( self.pointing - self.spinSpeedMode.current())
        if self.rotationMode.mode == tankMode or self.rotationMode.mode == tankFieldMode:
            self.heading = self.pointing
        else:
            self.rotationMode.setMode(manualRotationMode ) # turn off auto rotation

    def turnCWBy( self, value):
        # value is in range 0..1
        if value > joystickManager.DEAD_ZONE:
            self._turnToward( self.pointing + self.spinSpeedMode.current() * value)
            if self.rotationMode.mode == tankMode or self.rotationMode.mode == tankFieldMode:
                self.heading = self.pointing
            else:
                self.rotationMode.setMode(manualRotationMode ) # turn off auto rotation

        
    def turnCCWBy( self, value):
        # value is in range 0..1
        if value > joystickManager.DEAD_ZONE:
            self._turnToward( self.pointing - self.spinSpeedMode.current() * value)
            if self.rotationMode.mode == tankMode or self.rotationMode.mode == tankFieldMode:
                self.heading = self.pointing
            else:
                self.rotationMode.setMode(manualRotationMode ) # turn off auto rotation


    def setSpecial (self,message):
        if not isinstance( message, str):
            str( message)
        self.special = message