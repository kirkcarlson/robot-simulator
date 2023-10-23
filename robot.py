#### IMPORTS ####
import math
import rmath
import pygame
import mode
import info
import joystickManager

#### CONSTANTS ####
MAX_ROBOT_SPEED = 5  #need to scale this to be 16 feet per second

spinSpeedModes = [ 5, 2.5, 1, 0.5]

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
rotationModes = [ "manual", "to front", "spin CW", "spin CCW", "tank", "tank field mode", "to north", "to south", "to east", "to west"]
manualRotationMode  = 0
autoRotateFrontMode = 1
spinCWMode          = 2
spinCCWMode         = 3
tankMode            = 4
tankFieldMode       = 5
autoRotateNorthMode = 6
autoRotateSouthMode = 7
autoRotateEastMode  = 8
autoRotateWestMode  = 9


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
        self.joystickManager = joystickManager.JoystickManager( joystick) # assocates joystick with joystick manager
        self.assignedJoyforDrive = self.joystickManager.combinedJoy # joystick to be used for drive e.g. self.joystickManager.leftJoy
        self.driveByJoy= lambda : self.driveByJoystickDefault()
        self.joy # joystick values used to control robot motions.
        self.info = info.Info() # information area assiciated with this robot
        self.position = pygame.math.Vector2(*position)
        self.pointing = 0  # direction that the robot is pointing
        self.heading = 0  # directon in which the robot is moving
        self.spinSpeedMode = mode.Mode ( spinSpeedModes)
        self.elevatorMode = mode.Mode ( elevatorModes)
        self.rotationMode = mode.ActionMode ( rotationModes, [ 
            lambda : self.driveByJoystickNoRotation(),
            lambda : self.driveByJoystickRotateToFront(),
            lambda : self.driveByJoystickRotateCW(),
            lambda : self.driveByJoystickRotateCCW(),
            lambda : self.driveByJoystickTankMode(),
            lambda : self.driveByJoystickTankFieldMode(),
            lambda : self.drivself.eByJoystickRotateToNouth(),
            lambda : self.driveByJoystickRotateToEast(),
            lambda : self.driveByJoystickRotateToSouth(),
            lambda : self.driveByJoystickRotateToWest()
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
        self.joy = self.assignedJoy
        self.joystickManager.check() # update the joystick data for the robot
        self.driveByRobot = self.rotationMode.action 
        if self.joy.x != 0 or self.joy.y != 0:
            self.driveByRobot ()


        # Create the rotated copy.
        # py image has y down and 0 to the right, hence 90-angle
        self.image = pygame.transform.rotate(self.original_image, rmath.constrain360( 90-self.pointing)).convert()  # Angle is absolute value!

        # Make sure your rect represent the actual Surface.
        self.rect = self.image.get_rect()

        # Since the dimension probably changed you should move its center back to where it was.
        self.rect.center = self.position.x, self.position.y
            

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

    def handleWallCollision(self):
        # do not allow robot rectange to leave game rectangle
        # two points: upper left (min x y) and lower right (max x y)
        # define simple rectangles for the four walls, n,e,s,w
        # if e.collide(self.rect)
        #if pygame.Rect.colliderect(rect1, rect2):
        #    prevent overlap
        # if self
        #self.rect = self.image.get_rect()
        robotMinX, robotMinY, robotW, robotH = self.robot.rect
        robotMaxX = robotMinX + robotW
        robotMaxY = robotMinY + robotH
        w, h = pygame.display.get_surface().get_size()
        self.position = pygame.math.Vector2()
        if robotMinX < 0:
            x = robotW / 2
            #rect.left = 0
        if robotMaxX > w:
            x = w - robotW /2
            #rect.right = w
        if robotMinY < 0:
            y = 0 + robotH /2
            #rect.top = 0
        if robotMaxY > h: 
            y = robotH /2
            #rect.bottom = w
        self.robot.position.xy = x, y


    def driveByJoystickDefault(self):
        return


    def driveByJoystickNoRotation( self):
        self.position.x += self.joy.magnitude * MAX_ROBOT_SPEED * math.sin( math.radians( self.joy.angle))
        self.position.y -= self.joy.magnitude * MAX_ROBOT_SPEED * math.cos( math.radians( self.joy.angle))
        self.handleWallCollision()


    def driveByJoystickRotateToFront( self):
        self.heading = self.joy.angle
        self._turnToward( self.heading)
        self.driveByJoystickNoRotation(self)


    def driveByJoystickRotateCW( self):
        self.heading = self.joy.angle
        self._turnToward( self.pointing + self.spinSpeedMode.current())  # rotate clockwise
        self.driveByJoystickNoRotation(self)


    def driveByJoystickRotateCCW( self):
        self.heading = self.joy.angle
        self._turnToward( self.pointing - self.spinSpeedMode.current())  # rotate counter clockwise
        self.driveByJoystickNoRotation(self)


    def driveByJoystickTankMode( self):
        # tank mode, y ==> forward/backward speed, x ==> turn left/right
        
            # robot turning has a priority and if within +/-90 follows the robot vector, otherwise it is in reverse
            # velocity is controlled by the y coordinate of the joystick +forward, -backward
            # turn rate is controlled by the x coordinate of the joystick -left, +right
            #robotPointing = rmath.constrain360( robotPointing + (robot.spinSpeeds[ robot.spinSpeedMode.mode] * joyX))
        self._turnToward( self.pointing - self.spinSpeedMode.current()  * self.joy.position.x)
        self.heading = self.pointing
        self.position.x += (math.sin( math.radians(self.heading)) * self.joy.position.y * 5)
        self.position.y += (math.cos( math.radians(self.heading)) * self.joy.position.y * 5)
        self.handleWallCollision()


    def driveByJoystickTankFieldMode( self):
        diff = rmath.constrain180( self.pointing - self.joyAngle)
        if abs( diff) < 90: # normal
            self.turnToward( self.joy.angle)
            self.x += (math.sin( math.radians(self.heading)) * self.joy.magnitude * MAX_ROBOT_SPEED)
            self.y -= (math.cos( math.radians(self.heading)) * self.joy.magnitude * MAX_ROBOT_SPEED)
        else: #auto reverse
            self.turnToward( self.joy.angle - 180)
            self.x += (math.sin( math.radians(self.heading) + 180 ) * self.joy.magnitude * MAX_ROBOT_SPEED)
            self.y -= (math.cos( math.radians(self.heading) + 180 ) * self.joy.magnitude * MAX_ROBOT_SPEED)
        self.handleWallCollision()

   
    def driveByJoystickRotateToNouth( self):
        self.heading = self.joy.angle
        self.heading = self.joy.angle
        self.driveByJoystickNoRotation()


    def driveByJoystickRotateToEast( self):
        self.heading = self.joy.angle
        self._turnToward( 90)
        self.driveByJoystickNoRotation()


    def driveByJoystickRotateToSouth( self):
        self.heading = self.joy.angle
        self._turnToward( 180)
        self.driveByJoystickNoRotation()
        

    def driveByJoystickRotateToWest( self):
        self.heading = self.joy.angle
        self._turnToward( 270)
        self.driveByJoystickNoRotation()


    def turnCW( self):
        self._turnToward( self.pointing + self.spinSpeedMode.current())
        if self.rotationMode.mode == tankMode:
            self.heading = self.pointing
        else:
            self.rotationMode.setMode(manualRotationMode ) # turn off auto rotation
        self.handleWallCollision()

        
    def turnCCW( self):
        self._turnToward( self.pointing - self.spinSpeedMode.current())
        if self.rotationMode.mode == tankMode:
            self.heading = self.pointing
        else:
            self.rotationMode.setMode(manualRotationMode ) # turn off auto rotation
        self.handleWallCollision()