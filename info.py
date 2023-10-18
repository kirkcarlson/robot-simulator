import pygame

'''This module displays information overlayed on the pygame screen'''

### CONSTANTS
TEXT_COLOR = 'azure'
FONT_SIZE = 16
LINE_SIZE = 15


class Info():
    def __init__(self, screen, upper_left, font, line_size, color=TEXT_COLOR):
        self.screen = screen
        self.color = color
        self.font = font
        self.upper_left = upper_left # dictionary with x and y
        self.line_size = line_size
        self.line_number = 0
        print( "initing info {self.upper_left['x']} {self.upper_left['y']}")


#function for outputting text onto the screen
    def drawln( self, text, lineNumber=-1):
        if lineNumber != -1:
            self.line_number = lineNumber
        img = self.font.render(text, True, self.color)
        self.screen.blit(img, (self.upper_left['x'], self.upper_left['y'] + self.line_number * self.line_size))
        self.line_number += 1
