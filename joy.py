import pygame
import rmath
import math
import mode
pygame.init()

"""SPECIAL CLASSES"""
"""
need to define a better Class for
- Joysticks
  * modes states
  * temporary variables
  * button names
- Robot
  * position
  * heading
  * pointing angle

maybe use enums with Mode to tie names and values easier
"""
elevatorMode = mode.Mode ([ "idle", "low", "medium", "high"])
rotationMode = mode.Mode ([ "manual", "to front", "spin CW", "spin CCW", "tank", "tank field mode", "to north", "to south", "to east", "to west"])
manualRotationMode = 0
autoRotationMode = 1
spinCWMode = 2
spinCCWMode = 3
tankMode = 4
tankFieldMode = 5
autoRotateNorth = 6
autoRotateSouth = 7
autoRotateEast = 8
autoRotateWest = 9

spinSpeedMode = mode.Mode ([ "5", "2.5", "1", "0.5"])
spinSpeeds = [5, 2.5, 1, 0.5]
joyAngle = 0
joyMagnitude = 0
minJoy = 0.0005

button_A = 0
button_B = 1
button_X = 2
button_Y = 3

#define font
font_size = 16
font = pygame.font.SysFont("Futura", font_size)

def yline ( line):
    line_size = 15
    base_line = 10
    return base_line + line * line_size

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_joy ( col, y, controller):
    '''Print the values for all joysticks of a controller
       col is the x position for the text
       line is the starting line number
       controller is the joystick controller object
    '''
    draw_text("Battery Level: " + str(controller.get_power_level()),    font, pygame.Color("azure"), col, yline(1))
    draw_text("Controller Type: " + str(controller.get_name()),         font, pygame.Color("azure"), col, yline(2))
    numAxes = controller.get_numaxes()
    draw_text("Number of axes: " + str(numAxes),                        font, pygame.Color("azure"), col, yline(3))
    draw_text("Number of buttons: " + str(controller.get_numbuttons()), font, pygame.Color("azure"), col, yline(4))
    draw_text("Number of hats: " + str(controller.get_numhats()),       font, pygame.Color("azure"), col, yline(5))

    # report button number
    numButtons = controller.get_numbuttons()
    buttonString = ""
    for joyButton in range (numButtons):
        if controller.get_button(joyButton):
            buttonString += " " + str(joyButton)
    draw_text("Button: " + buttonString, font, pygame.Color("azure"), col, yline(6))
    for joyAxis in range (numAxes):
        draw_text(f"Axis {joyAxis}: {controller.get_axis( joyAxis):> 0.2f}", font, pygame.Color("azure"), col, yline( 7+ joyAxis))

    # Hat position. All or nothing for direction, not a float like
    hats = controller.get_numhats()
    for hat in range(hats):
        draw_text(f"Hat {hat}: {controller.get_hat( hat)}", font, pygame.Color("azure"), col, yline( 7+ numAxes + hat))


'''
class Controller (pygame.joystick.Joystick()):
    """ A class for a generic XBOX joystick and its current state"""

    # button indices
    BUTTON_A_INDEX = 0
    BUTTON_B_INDEX = 1
    BUTTON_X_INDEX = 2
    BUTTON_Y_INDEX = 3

    RIGHT_PADDLE = 0
    LEFT_PADDLE = 1

    # button states
    buttonA = False
    buttonB = False
    buttonX = False
    buttonY = False

    # past button and chord states
    buttonAlast = False
    buttonBlast = False 
    buttonXlast = False
    buttonYlast = False
    buttonABlast = False
    buttonXYlast = False
    buttonAXlast = False
    buttonBYlast = False

    def __init__(self, index):
        super.device_index = index
        #self.device_index = index
        ### BUTTONS on generic XBOX controller

        ### Button states
        self.buttonA = False
        self.buttonB = False
        self.buttonX = False
        self.buttonY = False

        ### Button past states
        self.buttonAlast = False
        self.buttonBlast = False 
        self.buttonXlast = False
        self.buttonYlast = False
        self.buttonABlast = False
        self.buttonXYlast = False
        self.buttonAXlast = False
        self.buttonBYlast = False

    def readButtons( self):     # this needs to be done once a frame to load current button states
        self.buttonA = joystick.get_button( self.BUTTON_A_INDEX)
        self.buttonB = joystick.get_button( self.BUTTON_B_INDEX)
        self.buttonX = joystick.get_button( self.BUTTON_X_INDEX)
        self.buttonY = joystick.get_button( self.BUTTON_Y_INDEX)


    def whileButtonA ( self, funct):
        if self.buttonA and not ( self.buttonB or self.buttonX or self.buttonY):
            self.buttonAlast = True
            funct()
        else:
            self.buttonAlast = True


    def onButtonA ( self, funct):
        if not self.buttonAlast:
            if not ( self.buttonB or self.buttonX or self.buttonY):
                funct()
            self.buttonAlast = True
        else:
            self.buttonAlast = False


    def onButtonB ( self, funct):
        if not self.buttonBlast:
            if not ( self.buttonA or self.buttonX or self.buttonY):
                funct()
            self.buttonBlast = True
        else:
            self.buttonBlast = False


    def onButtonX ( self, funct):
        if not self.buttonXlast:
            if not ( self.buttonA or self.buttonB or self.buttonY):
                funct()
            self.buttonXlast = True
        else:
            self.buttonXlast = False


    def onButtonY ( self, funct):
        if not self.buttonYlast:
            if not ( self.buttonA or self.buttonB or self.buttonX):
                funct()
            self.buttonYlast = True
        else:
            self.buttonYlast = False


    def onButtonAB ( self, funct):
        if not self.buttonABlast:
            if not ( self.buttonX or self.buttonY):
                funct()
            self.buttonABlast = True
            self.buttonBlast = False
            self.buttonBlast = False
        else:
            self.buttonABlast = False


    def onButtonXY ( self, funct):
        if not self.buttonXYlast:
            if not ( self.buttonA or self.buttonB):
                funct()
            self.buttonXYlast = True
            self.buttonXlast = False
            self.buttonYlast = False
        else:
            self.buttonXYlast = False


    def onButtonAX ( self, funct):
        if not self.buttonAXlast:
            if not ( self.buttonB or self.buttonY):
                funct()
            self.buttonAXlast = True
            self.buttonAlast = False
            self.buttonXlast = False
        else:
            self.buttonAXlast = False


    def onButtonBY ( self, funct):
        if not self.buttonBYlast:
            if not ( self.buttonA or self.buttonX):
                funct()
            self.buttonBYlast = True
            self.buttonBlast = False
            self.buttonYlast = False
        else:
                self.buttonBYlast = False
'''


class Robot(pygame.sprite.Sprite):
    def __init__(self, position=(0, 0)):
        super(Robot, self).__init__()
        self.original_image = pygame.Surface((32, 32))
        #pygame.draw.lines(self.original_image, robotColor, True, [( 0,0),  (31,0),  (31,13), (8,13),
        #                                                            (8,9),   (4,9),   (4,21), (8,21),
        #                                                            (9,17), (31,17), (31,31), (0,31)])
        pygame.draw.lines(self.original_image, robotColor, True, [( 0,0),  (31,0),  (31,31),  (0,31),
                                                                   ( 0,17), (23,17), (23,21), (27,21),
                                                                   (27,9),  (23,9),  (23,13),  (0,13)])
        self.image = self.original_image  # This will reference our rotated copy.
        self.rect  = self.image.get_rect()
        self.position = pygame.math.Vector2(*position)
        self.pointing = 0
        self.heading = 0

    def update(self):
        # Create the rotated copy.
        # py image has y down and 0 to the right, hence 90-angle
        self.image = pygame.transform.rotate(self.original_image, rmath.constrain360( 90-self.pointing)).convert()  # Angle is absolute value!

        # Make sure your rect represent the actual Surface.
        self.rect = self.image.get_rect()

        # Since the dimension probably changed you should move its center back to where it was.
        self.rect.center = self.position.x, self.position.y
            
    #def turnRobotTo( angle):
    def turnTo( self, angle):
        diff = rmath.constrain360( self.pointing - angle)
        if abs( diff ) > 3:
            if diff > 0 and diff <180:
                self.pointing = rmath.constrain360( self.pointing - spinSpeeds[ spinSpeedMode.mode])
            else:
                self.pointing = rmath.constrain360( self.pointing + spinSpeeds[ spinSpeedMode.mode])
        else:
            self.pointing = angle

"""CONSTANTS"""
robotColor = (255,0,0)

#define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
FPS = 60   # frames per seconds


"""VARIABLES"""
joyY = joyX = 0
joysticks = []              #create empty list to store joysticks

pygame.joystick.init()
clock = pygame.time.Clock() #create clock for setting game frame rate

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2022 FRC 4513 Simulator")


robotColor  = "royalblue"
x = 350
y = 200
robot = Robot(position=(x,y))  #define robot

# these need to be part of a Class definition..#game loop
run = True
while run:
    clock.tick(FPS)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            controller = pygame.joystick.Joystick(event.device_index)
            joysticks.append(controller)
        #quit program
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                run = False
    #fill in background
    screen.fill(pygame.Color("midnightblue"))

    #show number of connected joysticks
    draw_text("Controllers: " + str(pygame.joystick.get_count()), font, pygame.Color("azure"), 10, yline(0))
    for joystick in joysticks:
        draw_joy (4, 40, joystick)
        draw_joy (200, 40, joystick)


        # really want this to be for each robot.
        draw_text(f"Elevator Mode: {elevatorMode.current()}",   font, pygame.Color("azure"), 10, yline( 15))
        draw_text(f"Rotation Mode: {rotationMode.current()}",   font, pygame.Color("azure"), 10, yline( 16))
        draw_text(f"Rotation Speed: {spinSpeedMode.current()}", font, pygame.Color("azure"), 10, yline( 17))
        draw_text(f"Pointing Angle: {robot.pointing: 7.2f}",      font, pygame.Color("azure"), 10, yline( 18))
        draw_text(f"Heading Angle: {robot.heading: 7.2f}",      font, pygame.Color("azure"), 10, yline( 19))

        ''' mode control
        each press advances the mode by one
        X0-normal
        X1-rotate to direction of travel
        X2-rotate to anti direction of travel

        tower control              arm extend  elevator
        preset 0: stow point       0           deck
        preset 1: floor pickup     low         floor
        preset 2: station pickup   low         med
        preset 3: low stand        low         floor
        preset 4: medium stand     med         med
        preset 5: high stand       high        high

        '''
        if elevatorMode.isEdge ( joystick.get_button(6)):
            elevatorMode.advanceCyclic()

        if rotationMode.isEdge ( joystick.get_button(2)):
            rotationMode.advanceCyclic()

        if spinSpeedMode.isEdge ( joystick.get_button(5)):
            spinSpeedMode.advanceCyclic()

        '''
        joystick.onButtonAB( ( lambda autoRotationSouth : rotationMode.set( autoRotationSouth) ) )
        joystick.onButtonXY( ( lambda autoRotationNorth : rotationMode.set( autoRotationNorth) ) )
        joystick.onButtonAX( ( lambda autoRotationWest : rotationMode.set( autoRotationWest) ) )
        joystick.onButtonBY( ( lambda autoRotationEast : rotationMode.set( autoRotationEast) ) )
        '''


        ### get joystick vectors
        #robot movement with hat
        move = joystick.get_hat( 0)
        joyX = move[0]
        joyY = move[1] # positive is up
        joyAngle = rmath.atan360 ( joyY, joyX)

        #robot orientation with left analog stick
        horiz_move = joystick.get_axis(0)
        vert_move =  joystick.get_axis(1) # negative to make positive up
        if abs(vert_move) >= minJoy or abs(horiz_move) >= minJoy: #over ride joyX and joyY
            joyX = horiz_move
            joyY = -vert_move # for common code below
            joyAngle = rmath.joyatan360 ( -joyY, joyX)

        #robot movement with right analog stick
        horiz_move = joystick.get_axis(3)
        vert_move =  joystick.get_axis(4) # negative to make positive up
        if abs(vert_move) >= minJoy or abs(horiz_move) >= minJoy: #over ride joyX and joyY
            joyX = horiz_move
            joyY = -vert_move # for common code below
            joyAngle = rmath.joyatan360 ( -joyY, joyX)

        # ignore minor inputs from joysticks
        if abs( joyX) <= minJoy:
            joyX = 0
        if abs( joyY) <= minJoy:
            joyY = 0


        '''
        There are three angles to worry about

        robot.pointing is direction of front of robot with respect to the venue

        robot.heading is direction that the robot will move.
            for swerve drive this is independent of the pointing
            for tank drive this is either forward or backward in the direction of the robot

        joyAngle is the direction commanded by the joystick
            0,0 ==> no current command
        '''
        #calculate the joyVector
        #joyAngle = rmath.atan360 ( joyY, joyX)
        ##joyAngle = rmath.constrain360( 90 - rmath.atan360 ( joyX, joyY))
        joyMagnitude = math.sqrt( joyY*joyY + joyX*joyX)
        draw_text(f"Joy Angle: {joyAngle: 7.2f}",               font, pygame.Color("azure"), 10, yline( 20))
        draw_text(f"Joy Magnitude: {joyMagnitude: 7.2f}",       font, pygame.Color("azure"), 10, yline( 21))
        draw_text(f"joyX: {joyX: 5.2f}",       font, pygame.Color("azure"), 10, yline( 22))
        draw_text(f"joyY: {joyY: 5.2f}",       font, pygame.Color("azure"), 10, yline( 23))

        #move robot, but rotate only with paddles
        if rotationMode.mode == manualRotationMode and (joyX != 0 or joyY != 0): # only when moving...
            x += joyX * 5
            y -= joyY * 5

        #rotate robot to joy stick angle
        if rotationMode.mode == autoRotationMode and (joyX != 0 or joyY != 0): # only when moving...
            robot.turnTo( joyAngle)
            x += joyX * 5
            y -= joyY * 5

        # use h_move and v_move to use the other controls
        if rotationMode.mode == spinCWMode and (joyX != 0 or joyY != 0): # only when moving...
            #robotPointing = rmath.constrain360( robotPointing - spinSpeeds[ spinSpeedMode.mode]) # rotate clockwise
            robot.turnTo( robot.pointing - spinSpeeds[ spinSpeedMode.mode])  # rotate clockwise
            x += joyX * 5
            y -= joyY * 5

        if rotationMode.mode == spinCCWMode and (joyX != 0 or joyY != 0): # only when moving...
            #robotPointing = rmath.constrain360( robotPointing + spinSpeeds[ spinSpeedMode.mode]) # rotate counter clockwise
            robot.turnTo( robot.pointing + spinSpeeds[ spinSpeedMode.mode])  # rotate counter clockwise
            x += joyX * 5
            y -= joyY * 5

        # tank mode, v ==> forward/backward speed, h ==> turn left/right
        if rotationMode.mode == tankMode and (joyX != 0 or joyY != 0): # tank only when moving...
            # robot turning has a priority and if within +/-90 follows the robot vector, otherwise it is in reverse
            # velocity is controlled by the y coordinate of the joystick +forward, -backward
            # turn rate is controlled by the x coordinate of the joystick -left, +right
            #robotPointing = rmath.constrain360( robotPointing + (spinSpeeds[ spinSpeedMode.mode] * joyX))
            robot.turnTo( robot.pointing - spinSpeeds[ spinSpeedMode.mode] * joyX)
            robot.heading = robot.pointing
            x = x + (math.sin( math.radians(robot.heading)) * joyY * 5)
            y = y - (math.cos( math.radians(robot.heading)) * joyY * 5)
            #print (f"tank {joyX: 7.2f}, {joyY: 7.2f}, joy:{joyMagnitude: 7.2f}, {joyAngle: 7.2f}, robot:{robotPointing: 7.2f}, heading:{robotHeading: 7.2f}")

        # turn the robot to where joystick is pointing and move
        if rotationMode.mode == tankFieldMode and (joyX != 0 or joyY != 0): # tank only when moving...
            diff = rmath.constrain360( robot.pointing - joyAngle)
            if abs( diff ) > 3:
                if abs( diff) < 45:
                    robot.heading = robot.pointing = rmath.constrain360( robot.pointing - (diff /45))
                elif abs( diff) < 135:
                    robot.heading = robot.pointing = rmath.constrain360( robot.pointing - (diff /45))
                else: # auto reverse
                    robot.pointing = rmath.constrain360( robot.pointing + (diff /30))
                    robot.heading = rmath.constrain360( robot.pointing + 180)
            else:
                robot.pointing = rmath.constrain360( joyAngle)
            #if abs( diff) < 90:
            #    #robotPointing = rmath.constrain360( robotPointing + spinSpeeds[ spinSpeedMode.mode])
            #else:
            #    robotPointing = rmath.constrain360( -robotPointing - diff/45 * spinSpeeds[ spinSpeedMode.mode])
            robot.heading = robot.pointing
            x = x + (math.sin( math.radians(robot.heading)) * joyMagnitude * 5)
            y = y - (math.cos( math.radians(robot.heading)) * joyMagnitude * 5)

        # move to where joystick points, and turn robot to the north
        if rotationMode.mode == autoRotateNorth and (joyX != 0 or joyY != 0): # tank only when moving...
            robot.turnTo( 0)
            x += joyX * 5
            y -= joyY * 5

        # move to where joystick points, and turn robot to the south
        if rotationMode.mode == autoRotateSouth and (joyX != 0 or joyY != 0): # tank only when moving...
            robot.turnTo( 180)
            x += joyX * 5
            y -= joyY * 5

        # move to where joystick points, and turn robot to the east
        if rotationMode.mode == autoRotateEast and (joyX != 0 or joyY != 0): # tank only when moving...
            robot.turnTo( 90)
            x += joyX * 5
            y -= joyY * 5

        # move to where joystick points, and turn robot to the west
        if rotationMode.mode == autoRotateWest and (joyX != 0 or joyY != 0): # tank only when moving...
            robot.turnTo( 270)
            x += joyX * 5
            y -= joyY * 5


        #rotate robot manually with paddles or A-B buttons
        if joystick.get_button(0): # A or right paddle, clockwise
            #robotPointing = rmath.constrain360( robotPointing + spinSpeeds[ spinSpeedMode.mode])
            robot.turnTo( robot.pointing + spinSpeeds[ spinSpeedMode.mode])
            robot.heading = robot.pointing
            if rotationMode.mode != tankMode:
                rotationMode.mode = manualRotationMode # turn off auto rotation
            else:
                robot.heading = robot.pointing
        if joystick.get_button(1): # B or left paddle, counter clockwise
            #robotPointing = rmath.constrain360( robotPointing - spinSpeeds[ spinSpeedMode.mode])
            robot.turnTo( robot.pointing - spinSpeeds[ spinSpeedMode.mode])
            if rotationMode.mode != tankMode:
                rotationMode.mode = manualRotationMode # turn off auto rotation
            else:
                robot.heading = robot.pointing

    # keep the robot on the field
    robot.position = pygame.math.Vector2()
    if x < 0:
        x = 0
    if x > SCREEN_WIDTH:
        x = SCREEN_WIDTH
    if y < 0:
        y = 0
    if y > SCREEN_HEIGHT:
        y = SCREEN_HEIGHT
    robot.position.xy = x, y

    robot.update()
    screen.blit(robot.image, robot.rect)
    pygame.display.update()

pygame.quit()
