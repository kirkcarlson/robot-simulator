import pygame
import rmath
import math
import mode
import info
import robot
pygame.init()

"""SPECIAL CLASSES"""
"""
need to refactor to make modules smaller:
  - controller stuff ... and allow more than one
  - chord 
  - screen printing stuff ... part of controller and robot?
  - robot stuff ... and allow more than one
  - field stuff
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

joyAngle = 0
joyMagnitude = 0
minJoy = 0.0005



# would be nice to extend joystick....
def draw_joy ( controller, joyinfo):
    '''Print the values for all joysticks of a controller
       col is the x position for the text
       line is the starting line number
       controller is the joystick controller object
    '''
    joyinfo.drawln (f"Controller number: {controller.get_instance_id()}", 1)
    joyinfo.drawln (f"Battery Level: {controller.get_power_level()}")
    joyinfo.drawln (f"Controller Type: {controller.get_name()}")
    numAxes = controller.get_numaxes()

    joyinfo.drawln (f"Number of axes: {numAxes}")
    joyinfo.drawln (f"Number of buttons: {controller.get_numbuttons()}")
    joyinfo.drawln (f"Number of hats: {controller.get_numhats()}")

    # report button number
    numButtons = controller.get_numbuttons()
    buttonString = ""
    for joyButton in range (numButtons):
        if controller.get_button(joyButton):
            buttonString += " " + str(joyButton)
    joyinfo.drawln (f"Button: {buttonString}")
    for joyAxis in range (numAxes):
        joyinfo.drawln (f"Axis {joyAxis}: {controller.get_axis( joyAxis):> 0.2f}")

    # Hat position. All or nothing for direction, not a float like
    hats = controller.get_numhats()
    for hat in range(hats):
        joyinfo.drawln (f"Hat {hat}: {controller.get_hat( hat)}")
        
    # really want this to be for each robot.
    joyinfo.drawln (f"Elevator Mode: {elevatorMode.current()}", 20)
    joyinfo.drawln (f"Rotation Mode: {rotationMode.current()}")
    joyinfo.drawln (f"Rotation Speed: {robot.spinSpeedMode.current()}")
    joyinfo.drawln (f"Pointing Angle: {robot.pointing: 7.2f}")
    joyinfo.drawln (f"Heading Angle: {robot.heading: 7.2f}")
    




#define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
FPS = 60   # frames per seconds


"""VARIABLES"""
joyY = joyX = 0
joysticks = []              #create empty list to store joysticks
joyinfos = []               #create empty list to store joystick info

pygame.joystick.init()
clock = pygame.time.Clock() #create clock for setting game frame rate

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2023 FRC 4513 Simulator")
font = pygame.font.SysFont("Futura", 16)

# test info as a concept
joytext = info.Info ( screen, {'x': 500, 'y': 20}, font, 15 ) 


x = 350
y = 200
robot = robot.Robot(position=(x,y), color = "royalblue")  #define robot

# these need to be part of a Class definition..#game loop
run = True
while run:
    clock.tick(FPS)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            #controller = Controller(event.device_index)
            controller = pygame.joystick.Joystick( event.device_index)
            # back door way of extending Joystick
            joyinfo = info.Info ( screen, {'x': 10+event.device_index*500, 'y': 20}, font, 15 ) 
            joysticks.append(controller)
            joyinfos.append(joyinfo)
        #quit program
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                run = False
    #fill in background
    screen.fill(pygame.Color("midnightblue"))

    #show number of connected joysticks
    joyinfo.drawln (f"Controllers: {pygame.joystick.get_count()}", 0)
    for i, joystick in enumerate( joysticks):
        joyinfo = joyinfos [i]
        draw_joy( joystick, joyinfo)


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

        if robot.spinSpeedMode.isEdge ( joystick.get_button(5)):
            robot.spinSpeedMode.advanceCyclic()

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
        joyinfo.drawln( f"Joy Angle: {joyAngle: 7.2f}")
        joyinfo.drawln( f"Joy Magnitude: {joyMagnitude: 7.2f}")
        joyinfo.drawln( f"joyX: {joyX: 5.2f}")
        joyinfo.drawln( f"joyY: {joyY: 5.2f}")

        #move robot, but rotate only with paddles
        if rotationMode.mode == manualRotationMode and (joyX != 0 or joyY != 0): # only when moving...
            robot.heading = joyAngle
            x += joyX * 5
            y -= joyY * 5

        #rotate robot to joy stick angle
        if rotationMode.mode == autoRotationMode and (joyX != 0 or joyY != 0): # only when moving...
            robot.heading = joyAngle
            robot.turnTo( joyAngle)
            x += joyX * 5
            y -= joyY * 5

        # use h_move and v_move to use the other controls
        if rotationMode.mode == spinCWMode and (joyX != 0 or joyY != 0): # only when moving...
            #robotPointing = rmath.constrain360( robotPointing - robot.spinSpeeds[ robot.spinSpeedMode.mode]) # rotate clockwise
            robot.heading = joyAngle
            robot.turnTo( robot.pointing - robot.spinSpeedMode.current())  # rotate clockwise
            x += joyX * 5
            y -= joyY * 5

        if rotationMode.mode == spinCCWMode and (joyX != 0 or joyY != 0): # only when moving...
            #robotPointing = rmath.constrain360( robotPointing + spinSpeeds[ spinSpeedMode.mode]) # rotate counter clockwise
            robot.heading = joyAngle
            robot.turnTo( robot.pointing + robot.spinSpeedMode.current())  # rotate counter clockwise
            x += joyX * 5
            y -= joyY * 5

        # tank mode, v ==> forward/backward speed, h ==> turn left/right
        if rotationMode.mode == tankMode and (joyX != 0 or joyY != 0): # tank only when moving...
            # robot turning has a priority and if within +/-90 follows the robot vector, otherwise it is in reverse
            # velocity is controlled by the y coordinate of the joystick +forward, -backward
            # turn rate is controlled by the x coordinate of the joystick -left, +right
            #robotPointing = rmath.constrain360( robotPointing + (robot.spinSpeeds[ robot.spinSpeedMode.mode] * joyX))
            robot.turnTo( robot.pointing - robot.spinSpeedMode.mode  * joyX)
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
            #    #robotPointing = rmath.constrain360( robotPointing + robot.spinSpeeds[ robot.spinSpeedMode.mode])
            #else:
            #    robotPointing = rmath.constrain360( -robotPointing - diff/45 * robot.spinSpeeds[ robot.spinSpeedMode.mode])
            #robot.heading = robot.pointing
            x = x + (math.sin( math.radians(robot.heading)) * joyMagnitude * 5)
            y = y - (math.cos( math.radians(robot.heading)) * joyMagnitude * 5)

        # move to where joystick points, and turn robot to the north
        if rotationMode.mode == autoRotateNorth and (joyX != 0 or joyY != 0): # tank only when moving...
            robot.heading = joyAngle
            robot.turnTo( 0)
            x += joyX * 5
            y -= joyY * 5

        # move to where joystick points, and turn robot to the south
        if rotationMode.mode == autoRotateSouth and (joyX != 0 or joyY != 0): # tank only when moving...
            robot.turnTo( 180)
            robot.heading = joyAngle
            x += joyX * 5
            y -= joyY * 5

        # move to where joystick points, and turn robot to the east
        if rotationMode.mode == autoRotateEast and (joyX != 0 or joyY != 0): # tank only when moving...
            robot.heading = joyAngle
            robot.turnTo( 90)
            x += joyX * 5
            y -= joyY * 5

        # move to where joystick points, and turn robot to the west
        if rotationMode.mode == autoRotateWest and (joyX != 0 or joyY != 0): # tank only when moving...
            robot.heading = joyAngle
            robot.turnTo( 270)
            x += joyX * 5
            y -= joyY * 5


        #rotate robot manually with paddles or A-B buttons
        if joystick.get_button(0): # A or right paddle, clockwise
            #robotPointing = rmath.constrain360( robotPointing + robot.spinSpeedMode.current())
            robot.turnTo( robot.pointing + robot.spinSpeedMode.current())
            if rotationMode.mode == tankMode:
                robot.heading = robot.pointing
            else:
                rotationMode.mode = manualRotationMode # turn off auto rotation
        if joystick.get_button(1): # B or left paddle, counter clockwise
            #robotPointing = rmath.constrain360( robotPointing - robot.spinSpeedMode.current())
            robot.turnTo( robot.pointing - robot.spinSpeedMode.current())
            if rotationMode.mode == tankMode:
                robot.heading = robot.pointing
            else:
                rotationMode.mode = manualRotationMode # turn off auto rotation
        #chord.check()

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
