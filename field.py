### THIS FILE IS NOT COMPLETE AND HAS NOT BEEN INTEGRATED OR DEBUGGED ###
import pygame
import rmath

SCREEN_WIDTH = 648
SCREEN_HEIGHT = 324
fieldColor = (80,80,80)
'''
STRATEGY for integrating field to game
- use the existing size and use the field sprite and charge station sprites
- play within the field area and get it right
- change to resize or scale the field and robot sprites to fill resized screen dynamically
  - change the corresponding robot speed variables as well


- this may be MESSED UP... South should be the drive stations and North should be the far end of the field
  - this is the perspective of the driver and that is all important for this simulation
  - as set up it is the perspecitive of the audience which is not a player!
  - but then you have to flip thing based on red and blue alliances
   N                        RED                 BLUE
 W---E   should be    PICKUP SCORE    or    SCORE PICKUP
   S                        BLUE                RED

'''


'''This file is intended to set up the field. Elements within the field will become immovable sprites that will collide with the robot.

All dimensions are in inches and are nominal before scaling to pixels.

the field is showed with audience to the north, blue to the west, red to the east and judges to the south.
'''
scaling = 2 # pixels per inch ...IDEAL
width  = 648 #inches
height = 324 #inches

fieldNW = ( 0,     0)
fieldNE = ( width, 0)
fieldSW = ( 0,     height)
fieldSE = ( width, height)

redLoadingStationNW = (  0,   1)
redLoadingStationNE = ( 14,   1)
redLoadingStationSW = (  0, 117)
redLoadingStationSE = ( 14, 117)

blueGridNNW = (  0, 118)
blueGridNNE = ( 49, 118)
blueGridNSW = (  0, 193)
blueGridNSE = ( 49, 193)

blueGridMNW = (  0, 193)
blueGridMNE = ( 49, 193)
blueGridMSW = (  0, 259)
blueGridMSE = ( 49, 259)

blueGridSNW = (  0, 259)
blueGridSNE = ( 49, 259)
blueGridSSW = (  0, 334)
blueGridSSE = ( 49, 334)

blueBarrierNW = (  49, 116) # looks like y s/b 99... that would push everything down blueBarrierNE = ( 119, 116) # guessing length = 70
blueBarrierNE = ( 119, 116)
blueBarrierSW = (  49, 120)
blueBarrierSE = ( 119, 120)

blueChargerNW = ( 108, 178) # looks like y s/b 118+59 = 177
blueChargerNE = ( 180, 178) # assuming 4x8' top and 1x8' ramps
blueChargerSW = ( 108, 274)
blueChargerSE = ( 180, 274)

blueLoadingStationNW = ( 634,   1)
blueLoadingStationNE = ( 648,   1)
blueLoadingStationSW = ( 634, 117)
blueLoadingStationSE = ( 648, 117)

redGridNNW = ( 599, 118)
redGridNNE = ( 648, 118)
redGridNSW = ( 599, 193)
redGridNSE = ( 648, 193)

redGridMNW = ( 599, 193)
redGridMNE = ( 648, 193)
redGridMSW = ( 599, 259)
redGridMSE = ( 648, 259)

redGridSNW = ( 599, 259)
redGridSNE = ( 648, 259)
redGridSSW = ( 599, 334)
redGridSSE = ( 648, 334)

redBarrierNW = ( 529, 116) # looks like y s/b 99... that would push everything down
redBarrierNE = ( 599, 116) # guessing length = 70
redBarrierSW = ( 529, 120)
redBarrierSE = ( 599, 120)

redChargerNW = ( 468, 178) # looks like y s/b 118+59 = 177
redChargerNE = ( 540, 178) # assuming 4x8' top and 1x8 ramps
redChargerSW = ( 468, 274)
redChargerSE = ( 540, 274)

'''how do we draw the field?
at least 3 parts... those connected to the walls, and the two charge platforms
the sprite is drawn as a list of points [(,),(,),...]
We can built the list symbollically and then scale the coordinates within the list

'''

class Field(pygame.sprite.Sprite):

    def __init__(self, position=(0, 0)):
        super(Field, self).__init__()
        self.original_image = pygame.Surface((648, 324))
        pygame.draw.lines(self.original_image, fieldColor, True, [ # moving clockwise around the field
            # north side
            fieldNW, #goes along wall inside of loading stations
            fieldNE,
            # east side
            blueLoadingStationNE,
            blueLoadingStationNW,
            blueLoadingStationSW,
            blueLoadingStationSE,
            redGridNNE,
            redGridNNW,
            redBarrierNE,
            redBarrierNW,
            redBarrierSW,
            redBarrierSE,
            redGridSSW,
            # south side
            # east side
            blueGridSSE,
            blueBarrierSW,
            blueBarrierSE,
            blueBarrierNE,
            blueBarrierNW,
            blueGridNNE,
            blueGridNNW,
            #add in red loading station
            redLoadingStationSW,
            redLoadingStationSE,
            redLoadingStationNE,
            redLoadingStationNW
        ])
        self.image = self.original_image  # This will reference our rotated copy.
        self.rect  = self.image.get_rect()
        self.position = pygame.math.Vector2(*position)

    def update(self):
        # Create the rotated copy.
        self.image = pygame.transform.rotate(self.original_image, rmath.constrain360(-robotHeading)).convert()  # Angle is absolute value!

        # Make sure your rect represent the actual Surface.
        self.rect = self.image.get_rect()

        # Since the dimension probably changed you should move its center back to where it was.
        self.rect.center = self.position.x, self.position.y

class Charger(pygame.sprite.Sprite):

    def __init__(self, position=(0, 0)):
        super(Field, self).__init__()
        self.original_image = pygame.Surface((72, 96)) # assuming 6x8'
        pygame.draw.lines(self.original_image, fieldColor, True, [ # moving clockwise around charge station
            (  0, 0),  #NW,
            ( 72, 0),  #NE,
            (  0, 96), #SW,
            ( 72, 96)  #SE
        ])
        self.image = self.original_image  # This will reference our rotated copy.
        self.rect  = self.image.get_rect()
        self.position = pygame.math.Vector2(*position)

    def update(self):
        # Create the rotated copy.
        self.image = self.original_image

        # Make sure your rect represent the actual Surface.
        self.rect = self.image.get_rect()

        # Since the dimension probably changed you should move its center back to where it was.
        self.rect.center = self.position.x, self.position.y

# need to place the field, the two charging stations and a robot or two


"""CONSTANTS"""
robotColor = (255,0,0)
robotHeading =  90 # relative to right of window
robotVector = 90 # relative to right of window

#define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
FPS = 60   # frames per seconds



#initialise the joystick module
pygame.joystick.init()

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2022 FRC 4513 Simulator")

joysticks = []              #create empty list to store joysticks
clock = pygame.time.Clock() #create clock for setting game frame rate

robotColor  = "royalblue"
x = 350
y = 200
robot = Robot(position=(x,y))  #define robot

screen.fill(pygame.Color("midnightblue"))
