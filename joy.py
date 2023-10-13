import pygame
import math
pygame.init()

playerColor = (255,0,0)
playerAngle =  90 # relative to right of window
playerVector = 90 # relative to right of window
class Mode:

    def __init__( self, modes):
        self.modes = modes
        self.mode = 0
        self.lastTrigger = 0

    def isEdge( self, trigger):
        if trigger:
            if self.lastTrigger == 0:
                self.lastTrigger = 1
                return True
        else:
            self.lastTrigger = 0
        return False

    def advance( self):
        if self.mode + 1 < len(self.modes):
            self.mode += 1

    def advanceCyclic( self):
        self.mode += 1
        if self.mode >= len(self.modes):
            self.mode = 0

    def reset():
        self.mode = 0

elevatorMode = Mode ([ "idle", "low", "medium", "high"])
rotationMode = Mode ([ "stable", "to front", "spin clockwise", "spin counter clockwise"])

class Player(pygame.sprite.Sprite):

    def __init__(self, position=(0, 0)):
        super(Player, self).__init__()
        self.original_image = pygame.Surface((32, 32))
        #pygame.draw.lines(self.original_image, playerColor, True, [( 0,0),  (31,0),  (31,13), (8,13),
        #                                                            (8,9),   (4,9),   (4,21), (8,21),
        #                                                            (9,17), (31,17), (31,31), (0,31)])
        pygame.draw.lines(self.original_image, playerColor, True, [( 0,0),  (31,0),  (31,31),  (0,31),
                                                                   ( 0,17), (23,17), (23,21), (27,21),
                                                                   (27,9),  (23,9),  (23,13),  (0,13)])
        self.image = self.original_image  # This will reference our rotated copy.
        self.rect  = self.image.get_rect()
        self.position = pygame.math.Vector2(*position)

    def update(self):
        # Create the rotated copy.
        self.image = pygame.transform.rotate(self.original_image, constrain360(-playerAngle)).convert()  # Angle is absolute value!

        # Make sure your rect represent the actual Surface.
        self.rect = self.image.get_rect()

        # Since the dimension probably changed you should move its center back to where it was.
        self.rect.center = self.position.x, self.position.y

def constrain360( angle): # constrain angle to range (0,360)
    return angle % 360

def constrain180( angle): # constrain angle to range (-180,180)
    angle = constrain360( angle)
    if angle > 180:
        return angle - 360
    else:
        return angle

def atan360( adj, opp):  # find the angle 0..350 from x and y values
    if abs( adj) < 0.000005:
        angle = 0
    else:
        angle = math.degrees( math.atan (opp/adj))

    if opp >= 0 and adj >= 0: # NE quadrant            pygame SW quadrant
        angle += 0
    if adj < 0: # SE or SW quadrant                    pygame SE or NE quadrant
        angle += 180
    if opp < 0 and adj >=  0: # NW quadrant            pygame NW quadrant
        angle += 360
    return angle


#initialise the joystick module
pygame.joystick.init()

#define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2022 FRC 4513 Simulator")

#define font
font_size = 16
font = pygame.font.SysFont("Futura", font_size)
base_line = 10
line_size = 15

def yline ( line):
    return base_line + line * line_size

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#create clock for setting game frame rate
clock = pygame.time.Clock()
FPS = 60

#create empty list to store joysticks
joysticks = []

#define player colour
playerColor  = "royalblue"
#create player rectangle
x = 350
y = 200
player = Player(position=(x,y))

#game loop
run = True
while run:

    clock.tick(FPS)

    #update background
    screen.fill(pygame.Color("midnightblue"))

    #show number of connected joysticks
    draw_text("Controllers: " + str(pygame.joystick.get_count()), font, pygame.Color("azure"), 10, yline(0))
    for joystick in joysticks:
        draw_text("Battery Level: " + str(joystick.get_power_level()), font, pygame.Color("azure"), 10, yline(1))
        draw_text("Controller Type: " + str(joystick.get_name()), font, pygame.Color("azure"), 10, yline(2))
        draw_text("Number of axes: " + str(joystick.get_numaxes()), font, pygame.Color("azure"), 10, yline(3))
        draw_text("Number of buttons: " + str(joystick.get_numbuttons()), font, pygame.Color("azure"), 10, yline(4))
        draw_text("Number of hats: " + str(joystick.get_numhats()), font, pygame.Color("azure"), 10, yline(5))

    for joystick in joysticks:
        # report button number
        numButtons = joystick.get_numbuttons()
        draw_text("Button: ", font, pygame.Color("azure"), 10, yline(6))
        for joyButton in range (numButtons):
            if joystick.get_button(joyButton):
                draw_text("Button: " + str(joyButton), font, pygame.Color("azure"), 10, yline(6))

        numAxes = joystick.get_numaxes()
        for joyAxis in range (numAxes):
            move = joystick.get_axis( joyAxis)
            draw_text("Axis " + str(joyAxis) + ": " + str( move), font, pygame.Color("azure"), 10, yline( 7+ joyAxis))

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
        hats = joystick.get_numhats()
        for hat in range(hats):
            move = joystick.get_hat( hat)
            draw_text("Hat " + str(hat) + ": " + str( move), font, pygame.Color("azure"), 10, yline( 8+joyAxis))

        draw_text("Elevator Mode: " + elevatorMode.modes[elevatorMode.mode], font, pygame.Color("azure"), 10, yline( 9+joyAxis))
        draw_text("Rotation Mode: " + rotationMode.modes[rotationMode.mode], font, pygame.Color("azure"), 10, yline( 10+joyAxis))
        draw_text("Rotation Angle: " + str( playerAngle), font, pygame.Color("azure"), 10, yline( 11+joyAxis))
        draw_text("Heading: " + str( playerVector), font, pygame.Color("azure"), 10, yline( 12+joyAxis))


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

        common Class... which has a set of states
        which is only half the number of real states
        each real state has a pre-state where it is waiting for the button
        and the real state where it is waiting for the button release


        '''
        if elevatorMode.isEdge ( joystick.get_button(6)):
            elevatorMode.advanceCyclic()

        if rotationMode.isEdge ( joystick.get_button(2)):
            rotationMode.advanceCyclic()

        #change player colour with buttons
        if joystick.get_button(0):
            playerColor = "royalblue"
        if joystick.get_button(1):
            playerColor = "crimson"
        if joystick.get_button(2):
            playerColor = "fuchsia"
        if joystick.get_button(3):
            playerColor = "forestgreen"

        #player movement with hat
        move = joystick.get_hat( 0)
        x += move[0] * 5
        y -= move[1] * 5
        horiz_move = move[0]
        vert_move =  move[1]
        h_move = move[0]
        v_move = move[1]

        #player orientation with left analog stick
        horiz_move = joystick.get_axis(0)
        vert_move = joystick.get_axis(1)
        if abs(vert_move) > 0.05:
            y += vert_move * 5
        if abs(horiz_move) > 0.05:
            x += horiz_move * 5
        if abs(vert_move) > 0.05 or abs(horiz_move) > 0.05: #over ride the previous
            h_move = horiz_move
            v_move = vert_move

        #player movement with right analog stick
        horiz_move = joystick.get_axis(3)
        vert_move = joystick.get_axis(4)
        if abs(vert_move) > 0.05:
            y += vert_move * 5
        if abs(horiz_move) > 0.05:
            x += horiz_move * 5
        if abs(vert_move) > 0.05 or abs(horiz_move) > 0.05: #over ride the previous
            h_move = horiz_move
            v_move = vert_move

        #calculate the playerVector
        playerVector = atan360 ( h_move, v_move)
        #if v_move < 0 and h_move < 0:
        #    playerVector -= 180
        #if v_move < 0 and h_move > 0:
        #    playerVector += 180

        #rotate player with paddles or A-B buttons
        if joystick.get_button(0): # A or right paddle, clockwise
            playerAngle += 1
            rotationMode.mode = 0 # turn off auto rotation
        if joystick.get_button(1): # B or left paddle, counter clockwise
            playerAngle -= 1
            rotationMode.mode = 0 # turn off auto rotation

        #rotate player to player vector
        if rotationMode.mode == 1 and abs( horiz_move) > 0.00005 and abs( vert_move) > 0.00005: # only when moving...
            diff = constrain360( playerAngle - playerVector)
            if abs( diff ) > 3:
                if diff > 0 and diff <180:
                    playerAngle = constrain360( playerAngle - 3)
                else:
                    playerAngle = constrain360( playerAngle + 3)
            else:
                playerAngle = constrain360( playerVector)

        if rotationMode.mode == 2 and abs( horiz_move) > 0.00005 and abs( vert_move) > 0.00005: # only when moving...
            playerAngle = constrain360( playerAngle - 3) # rotate clockwise

        if rotationMode.mode == 3 and abs( horiz_move) > 0.00005 and abs( vert_move) > 0.00005: # only when moving...
            playerAngle = constrain360( playerAngle + 3) # rotate counter clockwise

    # keep the player on the field
    player.position = pygame.math.Vector2()
    if x < 0:
        x = 0
    if x > SCREEN_WIDTH:
        x = SCREEN_WIDTH
    if y < 0:
        y = 0
    if y > SCREEN_HEIGHT:
        y = SCREEN_HEIGHT
    player.position.xy = x, y

    player.update()
    screen.blit(player.image, player.rect)
    pygame.display.update()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
        #quit program
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
