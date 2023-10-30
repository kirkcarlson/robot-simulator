# robotSim -- video robot simulator to evaluate with joystick control options
"""
Notes
need to refactor to make modules smaller:
  - [x] controller stuff ... and allow more than one
  - [x] chord  = button Manager
  - [x] screen printing stuff ... part of controller and robot?
  - [x] robot stuff ... and allow more than one
  - [_] field stuff
need to define a better Class for
- Joysticks
  * [x] modes states
  * [x] temporary variables
  * [_] button names
- Robot
  * [x] position
  * [x] heading
  * [x] pointing angle

maybe use enums with Mode to tie names and values easier... doesn't seem so


hierarchy 
robotSim -- glue other pieces together, assign functionality to elements ( button->command, joystick->robot, etc)
  -pygame -- provides serices for game development
    -sprite -- defines moveable graphic elements
      -robot -- a graphic representation of a robot
        - joystickManager -- adds functionality to joystick
          -joystick -- provided an interface to a joystick
      -field -- graphic elements of the playing field
    -info overlay -- details of various element, usually for debugging
  -rmath
  -...

there should be some configuration assigments here, something like:
intialize pygame
get list of joysticks
robot1 = Robot( x=0, y=0, color='red')
robot1.info = info.Info ( screen, {'x': 500, 'y': 20}, font, 15 ) 
robot1.joystickManager = joystickManager( joysticks[ 0])
robot1.joystickManager.onPress([0,1], lambda : print("South Engaged"))
...assign specific joysticks to particular functions i.g
robot1.joy = robot1.joystickManager.leftJoy
...
robot2 = Robot( x=0, y=200, color='blue')
robot2.joystickManager = joystickManager( joysticks[ 1])
robot2.joystickManager.onPress([0,1], lambda : print("South Engaged"))
...
main loop
"""
import pygame
import info
import robot
import joystickManager
import buttonManager

#### CONSTANTS ####
#define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
FONT_SIZE = 16
FPS = 60   # frames per seconds

#### VARIABLES ####
joysticks = []     #create empty list to store joysticks
robot1 = None
info1  = None
robot2 = None
info2  = None

'''MAIN'''
pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock() #create clock for setting game frame rate
font = pygame.font.SysFont( "Futura", FONT_SIZE)

#create game window
screen = pygame.display.set_mode(( SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2023 FRC 4513 Simulator")


# these need to be part of a Class definition..#game loop
run = True
while run:
    clock.tick( FPS)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            controller = pygame.joystick.Joystick( event.device_index)
            joysticks.append( controller)
            if len( joysticks) > 0 and joysticks[0] != None:
                # Set up robot and its info instances
                robot1 = robot.Robot( joysticks[0], position = (350, 200), color = "royalblue")  #define robot 1
                # Info ( screen, upper_left, font, robot, line_size=LINE_SIZE, color=TEXT_COLOR):
                robot1.info = info.Info( screen, (10, 10), font, robot1 )
                                    
                # set up the mapping of chords and commands
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.A_BUTTON, buttonManager.B_BUTTON],
                    lambda : robot1.rotationMode.setMode( robot.autoRotateSouthMode ))
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.X_BUTTON, buttonManager.Y_BUTTON],
                    lambda : robot1.rotationMode.setMode( robot.autoRotateNorthMode ))
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.A_BUTTON, buttonManager.X_BUTTON],
                    lambda : robot1.rotationMode.setMode( robot.autoRotateWestMode ))
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.B_BUTTON, buttonManager.Y_BUTTON],
                    lambda : robot1.rotationMode.setMode( robot.autoRotateEastMode ))
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.A_BUTTON, buttonManager.B_BUTTON,
                    buttonManager.X_BUTTON, buttonManager.Y_BUTTON],
                    lambda : robot1.rotationMode.setMode( robot.autoRotateFrontMode ))
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.A_BUTTON, buttonManager.X_BUTTON,
                    buttonManager.LEFT_BUTTON],
                    lambda : robot1.rotationMode.setMode( robot.spinCWMode ))
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.B_BUTTON, buttonManager.Y_BUTTON,
                    buttonManager.LEFT_BUTTON],
                    lambda : robot1.rotationMode.setMode( robot.spinCCWMode ))
                robot1.joystickManager.buttonManager.onWhile(
                    [buttonManager.A_BUTTON],
                    lambda : robot1.turnCCW())
                robot1.joystickManager.buttonManager.onWhile(
                    [buttonManager.B_BUTTON],
                    lambda : robot1.turnCW())
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.LEFT_BUTTON],
                    lambda : robot1.elevatorMode.advanceCyclic())
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.XBOX_BUTTON],
                    lambda : robot1.rotationMode.advanceCyclic())
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.X_BUTTON],
                    lambda : robot1.rotationMode.advanceCyclic())
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.RIGHT_BUTTON],
                    lambda : robot1.spinSpeedMode.advanceCyclic())
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.VIEW_BUTTON],
                    lambda : robot1.setSpecial( 'Start'))
                robot1.joystickManager.buttonManager.onRelease(
                    [buttonManager.VIEW_BUTTON],
                    lambda : robot1.setSpecial( ''))
                robot1.joystickManager.buttonManager.onPress(
                    [buttonManager.MENU_BUTTON],
                    lambda : robot1.setSpecial( ' Back'))
                robot1.joystickManager.buttonManager.onRelease(
                    [buttonManager.MENU_BUTTON],
                    lambda : robot1.setSpecial( ''))
                
                # map the joystick and trigger commands
                robot1.driveByAxis = [
                    lambda : robot1.turnCWBy( robot1.joystickManager.rightTrigger),
                    lambda : robot1.turnCCWBy( robot1.joystickManager.leftTrigger)
                ]
            
                # set startup modes
                robot1.rotationMode.setMode( robot.manualRotationMode )
                robot1.spinSpeedMode.setMode( robot.spinSpeedHigh)
                robot1.driveByJoystick =  lambda : robot1.rotationMode.command(
                    robot1.joystickManager.combineJoys( [
                        robot1.joystickManager.rightJoy,
                        robot1.joystickManager.leftJoy,
                        robot1.joystickManager.hat]))

            if len( joysticks) > 1 and joysticks[1] != None:
                # Set up robot and its info instances
                robot2 = robot.Robot( joysticks[1], position = (550, 200), color = "red")  #define robot 1
                # Info ( screen, upper_left, font, robot, line_size=LINE_SIZE, color=TEXT_COLOR):
                robot2.info = info.Info( screen, (400, 10), font, robot2 )

                # set up the mapping of chords and commands
                robot2.joystickManager.buttonManager.onWhile(
                    [buttonManager.A_BUTTON],
                    lambda : robot2.turnCCW())
                robot2.joystickManager.buttonManager.onWhile(
                    [buttonManager.B_BUTTON],
                    lambda : robot2.turnCW())
                robot2.joystickManager.buttonManager.onPress(
                    [buttonManager.XBOX_BUTTON],
                    lambda : robot2.rotationMode.advanceCyclic())
                robot2.joystickManager.buttonManager.onPress(
                    [buttonManager.VIEW_BUTTON],
                    lambda : robot2.setSpecial( 'Start'))
                robot2.joystickManager.buttonManager.onRelease(
                    [buttonManager.VIEW_BUTTON],
                    lambda : robot2.setSpecial( ''))
                robot2.joystickManager.buttonManager.onPress(
                    [buttonManager.MENU_BUTTON],
                    lambda : robot2.setSpecial(' Back'))
                robot2.joystickManager.buttonManager.onRelease(
                    [buttonManager.MENU_BUTTON],
                    lambda : robot2.setSpecial( ''))
                
                # map the joystick and trigger commands
                robot2.driveByAxis = [
                    lambda : robot2.turnCWBy( robot2.joystickManager.rightTrigger),
                    lambda : robot2.turnCCWBy( robot2.joystickManager.leftTrigger)
                ]
            
                # set startup modes
                robot2.rotationMode.setMode( robot.manualRotationMode )
                robot2.spinSpeedMode.setMode( robot.spinSpeedHigh)
                robot2.driveByJoystick =  lambda : robot2.rotationMode.command(
                    robot2.joystickManager.combineJoys( [
                        robot2.joystickManager.leftJoy ],))

            
        #quit program
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                run = False

    #fill in background
    screen.fill( pygame.Color("midnightblue"))
    
    #update text first to make it under the robots
    if robot1 != None:
        robot1.info.update()
    if robot2 != None:
        robot2.info.update()
    #update robots
    if robot1 != None:
        robot1.update()
        screen.blit( robot1.image, robot1.rect) # probably should do in the robot module...
    if robot2 != None:
        robot2.update()
        screen.blit( robot2.image, robot2.rect) # probably should do in the robot module...

    pygame.display.update()

pygame.quit()