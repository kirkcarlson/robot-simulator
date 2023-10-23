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
robotSim -- glue other pieces together, assign functionality to elements (button->command, joystick->robot, etc)
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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2023 FRC 4513 Simulator")

# test info as a concept
joytext = info.Info ( screen, {'x': 500, 'y': 20}, font, 15 ) 



# these need to be part of a Class definition..#game loop
run = True
while run:
    clock.tick(FPS)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            controller = pygame.joystick.Joystick( event.device_index)
            joysticks.append(controller)
            if len( joysticks) > 0 and joysticks[0] != None:
                # Robot ( joystickManager, position, color, )
                joystickManager = joystickManager.JoystickManager( joysticks[ 0])
                robot1 = robot.Robot( joystickManager, position = (350, 200), color = "royalblue")  #define robot 1
                robot1.joy = joysticks[0]
                info1 = info.Info( screen, (10, 10), robot1,  )
                                    
                # set up the chords and actions
                robot1.joystickManager.onPress( [0,1], lambda : print( "South Engaged"))
                robot1.joystickManager.onPress( [2,3], lambda : print( "North Engaged"))
                robot1.joystickManager.onPress( [0,2], lambda : print( "West Engaged"))
                robot1.joystickManager.onPress( [1,3], lambda : print( "East Engaged"))
                robot1.joystickManager.onPress( [0], lambda : print( "CW Engaged")) # lambda : self.robot1.turnCCW()
                robot1.joystickManager.onPress( [1], lambda : print( "CCW Engaged")) # lambda : self.robot1.turnCCW()
                robot1.joystickMangger.onPress( [6], lambda : print( "elevator Engaged")) # lambda : self.robot1.elevatorMode.advanceCyclic()
                robot1.joystickMangger.onPress( [2], lambda : print( "rotation Engaged")) # lambda : self.robot1.rotationMode.advanceCyclic()
                robot1.joystickMangger.onPress( [5], lambda : print( "spin Engaged")) # lambda : self.robot1.spinSpeedMode.advanceCyclic()
                #info(           ( screen, upper_left, font, line_size, robot, color=TEXT_COLOR):

            if len( joysticks) > 1 and joysticks[1] != None:
                # Robot ( joystickManager, position, color, )
                joystickManager = joystickManager.JoystickManager( joysticks[ 1])
                robot2 = robot.Robot( joystickManager, position = (450, 200), color = "red")  #define robot 1
                robot2.joy = joysticks[1]
                info2 = info.Info( screen, (400, 10), robot2,  )
                # set up the chords and actions
                robot2.joystickManager.onPress([0,1], lambda : print("South Engaged"))
                robot2.joystickManager.onPress([2,3], lambda : print("North Engaged"))
                robot2.joystickManager.onPress([0,2], lambda : print("West Engaged"))
                robot2.joystickManager.onPress([1,3], lambda : print("East Engaged"))
                robot2.joystickManager.onPress([0], lambda : print("CW Engaged")) # lambda : self.robot1.turnCCW()
                robot2.joystickManager.onPress([1], lambda : print("CCW Engaged")) # lambda : self.robot1.turnCCW()
                robot2.joystickMangger.onPress([6], lambda : print("elevator Engaged")) # lambda : self.robot1.elevatorMode.advanceCyclic()
                robot2.joystickMangger.onPress([2], lambda : print("rotation Engaged")) # lambda : self.robot1.rotationMode.advanceCyclic()
                robot2.joystickMangger.onPress([5], lambda : print("spin Engaged")) # lambda : self.robot1.spinSpeedMode.advanceCyclic()


        #quit program
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                run = False

    #fill in background
    screen.fill(pygame.Color("midnightblue"))
    
    #update robots
    if robot1 != None:
        info1.update()
        robot1.update()
        screen.blit(robot1.image, robot1.rect)
    if robot2 != None:
        info2.update()
        robot2.update()
        screen.blit(robot2.image, robot2.rect)

    pygame.display.update()

pygame.quit()