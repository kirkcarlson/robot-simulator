import rmath
import pygame
import mode


'''Robot class for robots in simulator'''
class Robot(pygame.sprite.Sprite):
    def __init__(self, position=(0, 0), color= "white"):
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
        self.position = pygame.math.Vector2(*position)
        self.pointing = 0
        self.heading = 0
        self.spinSpeedMode = mode.Mode ([ 5, 2.5, 1, 0.5])

    def update(self):
        # Create the rotated copy.
        # py image has y down and 0 to the right, hence 90-angle
        self.image = pygame.transform.rotate(self.original_image, rmath.constrain360( 90-self.pointing)).convert()  # Angle is absolute value!

        # Make sure your rect represent the actual Surface.
        self.rect = self.image.get_rect()

        # Since the dimension probably changed you should move its center back to where it was.
        self.rect.center = self.position.x, self.position.y
            
    def turnTo( self, angle):
        diff = rmath.constrain360( self.pointing - angle)
        if abs( diff ) > 3:
            if diff > 0 and diff <180:
                self.pointing = rmath.constrain360( self.pointing - self.spinSpeedMode.current())
            else:
                self.pointing = rmath.constrain360( self.pointing + self.spinSpeedMode.current())
        else:
            self.pointing = angle
            
    def turnCW():
        robot.turnTo( robot.pointing + self.spinSpeedMode.current())
            
    def turnCCW():
        robot.turnTo( robot.pointing - self.spinSpeedMode.current())