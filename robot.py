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
elevatorModes = [ "idle", "floor pickup", "low", "medium", "high"]
elevatorIdleMode        = 0
elevatorFloorPickupMode = 1
elevatorLowMode         = 2
elevatorMediumMode      = 3
elevatorHighMode        = 4

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
        pygame.draw.lines(self.original_image, self.color, True, [( 0,0),  (31,0),  (31,31),  (0,31),
                                                                   ( 0,17), (23,17), (23,21), (27,21),
                                                                   (27,9),  (23,9),  (23,13),  (0,13)])
        self.image = self.original_image  # This will reference our rotated copy.
        self.rect  = self.image.get_rect()
        self.joystick = joystick # joystick object used to control robot motions.
        self.joystickManager = joystickManager.JoystickManager( joystick) # assocates joystick with joystick manager
        self.assignedJoyforDrive = self.joystickManager.combinedJoy # joystick to be used for drive e.g. self.joystickManager.leftJoy
        self.joy = None # joy object assigned for drive by joystick
        self.driveByJoy= lambda : self.driveByJoystickNoRotation() # pointer to a particular function
        #self.info = info.Info() # information area assiciated with this robot
        self.position = pygame.math.Vector2(*position)
        self.pointing = 0  # direction that the robot is pointing
        self.heading = 0  # directon in which the robot is moving
        self.spinSpeedMode = mode.Mode ( spinSpeedModes)
        self.elevatorMode = mode.Mode ( elevatorModes)
        self.rotationMode = mode.ActionMode ( rotationModes, [ 
            lambda : self.driveByJoystickNoRotation(),
            lambda : self.driveByJoystickTankMode(),
            lambda : self.driveByJoystickTankFieldMode(),
            lambda : self.driveByJoystickRotateToFront(),
            lambda : self.driveByJoystickRotateToNorth(),
            lambda : self.driveByJoystickRotateToSouth(),
            lambda : self.driveByJoystickRotateToEast(),
            lambda : self.driveByJoystickRotateToWest(),
            lambda : self.driveByJoystickRotateCW(),
            lambda : self.driveByJoystickRotateCCW(),
        ])


    def update(self):
        # need to do the real time drive by joystick command...
        # easiest way for now is to use the match case thing
        # would like to use a lambda function set by the mode selection
        '''
        same problem comes to play for the joystick paddles
        the joystick is scanned on each frame
        if an action/command is attached to a joystick it is executed from the joystickManager
        the same thing should happen for the joystick devices on the joystick controller
        in this case, the command/action would update the robot.position, etc. and this routing would paint
        the robot in its new postion, orientation, etc.
        '''
        # move the robot as prescribed with joystick
        #self.joy = self.assignedJoy
        self.joystickManager.check() # update the joystick data for the robot
        self.joy = self.joystickManager.combinedJoy
        self.driveByRobot = self.rotationMode.action 
        if self.joy.magnitude > 0: # this seems redundant
            self.driveByRobot ()


        # Create the rotated copy.
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
        if abs( diff ) > 3:
            if diff > 0 and diff <180:
                self.pointing = rmath.constrain360( self.pointing - self.spinSpeedMode.current())
            else:
                self.pointing = rmath.constrain360( self.pointing + self.spinSpeedMode.current())
        else:
            self.pointing = angle
            

    def turnCW( self):
        self._turnToward( self.pointing + self.spinSpeedMode.current())
            

    def turnCCW( self):
        self._turnToward( self.pointing - self.spinSpeedMode.current())

    '''
    MAX_ROBOT_SPEED is supposed the maximum speed of the robot. The current use here is incorrect
    as it would need to be broken down into its x and y components base on robot heading.
            x += joyX * MAX_ROBOT_SPEED
            y -= joyY * MAX_ROBOT_SPEED

            should be:
            x += self.joy.magnitude * math.sin(self.joy.angle) * MAX_ROBOT_SPEED
            y += self.joy.magnitude * math.cos(self.joy.angle) * MAX_ROBOT_SPEED

    joyX and joyY are  consoldiated angles ... need to known assigned joystick for the drive by functions
    '''

    def driveByJoystickNoRotation( self):
        if self.joy.magnitude > 0:
            self.position.x += self.joy.magnitude * MAX_ROBOT_SPEED * math.sin( math.radians( self.joy.angle))
            self.position.y -= self.joy.magnitude * MAX_ROBOT_SPEED * math.cos( math.radians( self.joy.angle))


    def driveByJoystickRotateToFront( self):
        if self.joy.magnitude > 0:
            self.heading = self.joy.angle
            self._turnToward( self.heading)
            self.driveByJoystickNoRotation()


    def driveByJoystickRotateCW( self):
        if self.joy.magnitude > 0:
            self.heading = self.joy.angle
            self._turnToward( self.pointing + self.spinSpeedMode.current())  # rotate clockwise
            self.driveByJoystickNoRotation()


    def driveByJoystickRotateCCW( self):
        if self.joy.magnitude > 0:
            self.heading = self.joy.angle
            self._turnToward( self.pointing - self.spinSpeedMode.current())  # rotate counter clockwise
            self.driveByJoystickNoRotation()


    def driveByJoystickTankMode( self):
        if self.joy.magnitude > 0:
            print (f"tank mode joy x:{self.joy.x:.2f} y:{self.joy.y:.2f} mag:{self.joy.magnitude:.2f} ang:{self.joy.angle:.1f}")
            # tank mode, y ==> forward/backward speed, x ==> turn left/right
            
                # robot turning has a priority and if within +/-90 follows the robot vector, otherwise it is in reverse
                # velocity is controlled by the y coordinate of the joystick +forward, -backward
                # turn rate is controlled by the x coordinate of the joystick -left, +right
                #robotPointing = rmath.constrain360( robotPointing + (robot.spinSpeeds[ robot.spinSpeedMode.mode] * joyX))
            self._turnToward( self.pointing + self.spinSpeedMode.current()  * self.joy.x)
            self.heading = self.pointing
            self.position.x += (math.sin( math.radians(self.heading)) * self.joy.y * 5)
            self.position.y -= (math.cos( math.radians(self.heading)) * self.joy.y * 5) # y is down on the screen


    def driveByJoystickTankFieldMode( self):
        if self.joy.magnitude > 0:
            diff = rmath.constrain180( self.pointing - self.joy.angle)
            if abs(diff) > 120:
                self._turnToward( self.joy.angle)
                self.position.x += math.sin( math.radians(self.heading)) * self.joy.magnitude * MAX_ROBOT_SPEED
                self.position.y -= math.cos( math.radians(self.heading)) * self.joy.magnitude * MAX_ROBOT_SPEED # y is down on screen
            else: #auto reverse
                self._turnToward( self.joy.angle + 180 )
                self.position.x -= (math.sin( math.radians(self.heading) ) * self.joy.magnitude * MAX_ROBOT_SPEED)
                self.position.y += (math.cos( math.radians(self.heading) ) * self.joy.magnitude * MAX_ROBOT_SPEED)

   
    def driveByJoystickRotateToNorth( self):
        if self.joy.magnitude > 0:
            self.heading = self.joy.angle
            self._turnToward( 0)
            self.driveByJoystickNoRotation()


    def driveByJoystickRotateToEast( self):
        if self.joy.magnitude > 0:
            self.heading = self.joy.angle
            self._turnToward( 90)
            self.driveByJoystickNoRotation()


    def driveByJoystickRotateToSouth( self):
        if self.joy.magnitude > 0:
            self.heading = self.joy.angle
            self._turnToward( 180)
            self.driveByJoystickNoRotation()
        

    def driveByJoystickRotateToWest( self):
        if self.joy.magnitude > 0:
            self.heading = self.joy.angle
            self._turnToward( 270)
            self.driveByJoystickNoRotation()


    def turnCW( self):
        self._turnToward( self.pointing + self.spinSpeedMode.current())
        if self.rotationMode.mode == tankMode:
            self.heading = self.pointing
        else:
            self.rotationMode.setMode(manualRotationMode ) # turn off auto rotation

        
    def turnCCW( self):
        self._turnToward( self.pointing - self.spinSpeedMode.current())
        if self.rotationMode.mode == tankMode:
            self.heading = self.pointing
        else:
            self.rotationMode.setMode(manualRotationMode ) # turn off auto rotation