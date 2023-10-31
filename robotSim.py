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
  * [x] button names
- Robot
  * [x] position
  * [x] heading
  * [x] pointing angle

maybe use enums with Mode to tie names and values easier... doesn't seem so


hierarchy 
robotSim -- glue other pieces together
  -pygame -- provides serices for game development
    -sprite -- defines moveable graphic elements
      -robot -- a graphic representation of a robot
        - joystickManager -- adds functionality to joystick
          -joystick -- provided an interface to a joystick
      -field -- graphic elements of the playing field
    -info overlay -- details of various element, usually for debugging
  -rmath
  -configureRobotx -- define robot x
    - buttons and joysticks  associations with particular command(s)
    - information area
    - graphic representation
  -...

...
main loop
"""
import pygame
#import info
#import robot
#import joystickManager
#import buttonManager
import configureRobot1
import configureRobot2

#### CONSTANTS ####
#define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
FONT_SIZE = 16
FPS = 60   # frames per seconds

#### VARIABLES ####
joysticks = []     #create empty list to store joysticks
robot1 = None
robot2 = None

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
                robot1 = configureRobot1.configureRobotX( joysticks[0], screen, font)
            if len( joysticks) > 1 and joysticks[1] != None:
                robot2 = configureRobot2.configureRobotX( joysticks[1], screen, font)
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