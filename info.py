import pygame

'''This module displays robot information overlayed on the screen'''

### CONSTANTS
TEXT_COLOR = 'azure'
LINE_SIZE = 15


class Info(): 
    def __init__(self, screen, upper_left, font, robot, line_size=LINE_SIZE, color=TEXT_COLOR):
        self.screen = screen
        self.robot = robot
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
        self.screen.blit(img, (self.upper_left[0], self.upper_left[1] + self.line_number * self.line_size))
        self.line_number += 1


    def update ( self):
        '''Print the information for a robot
        controller is the joystick controller object
        '''
        # Print Raw Joystick Controller Information
        self.drawln (f"Controller number: {self.robot.joystickManager.joystick.get_instance_id()}", 1)
        self.drawln (f"Battery Level: {self.robot.joystickManager.joystick.get_power_level()}")
        self.drawln (f"Controller Type: {self.robot.joystickManager.joystick.get_name()}")
        numAxes = self.robot.joystickManager.joystick.get_numaxes()

        self.drawln (f"Number of axes: {numAxes}")
        self.drawln (f"Number of buttons: {self.robot.joystickManager.joystick.get_numbuttons()}")
        self.drawln (f"Number of hats: {self.robot.joystickManager.joystick.get_numhats()}")

        # report button numbers
        numButtons = self.robot.joystickManager.joystick.get_numbuttons()
        buttonString = ""
        for joyButton in range (numButtons):
            if self.robot.joystickManager.joystick.get_button(joyButton):
                buttonString += " " + str(joyButton)
        self.drawln (f"Button: {buttonString}")
        for joyAxis in range (numAxes):
            self.drawln (f"Raw Axis {joyAxis}: {self.robot.joystickManager.joystick.get_axis( joyAxis):> 0.2f}")

        numHats = self.robot.joystickManager.joystick.get_numhats()
        for hat in range(numHats):
            self.drawln (f"Hat {hat}: {self.robot.joystickManager.joystick.get_hat( hat)}")

        self.drawln( "") # Print normalized Joystick Inion
        self.drawln( f"Right Joy Angle:        {self.robot.joystickManager.rightJoy.angle: 7.2f}")
        self.drawln( f"Right Joy Magnitude:    {self.robot.joystickManager.rightJoy.magnitude: 7.2f}")
        self.drawln( f"Left Joy Angle:         {self.robot.joystickManager.leftJoy.angle: 7.2f}")
        self.drawln( f"Left Joy Magnitude:     {self.robot.joystickManager.leftJoy.magnitude: 7.2f}")
        self.drawln( f"Hat Angle:              {self.robot.joystickManager.hat.angle: 7.2f}")
        self.drawln( f"Hat Magnitude:          {self.robot.joystickManager.hat.magnitude: 7.2f}")
        self.drawln( f"Combined Joy Angle:     {self.robot.joystickManager.combinedJoy.angle: 7.2f}")
        self.drawln( f"Combined Joy Magnitude: {self.robot.joystickManager.combinedJoy.magnitude: 7.2f}")
            
        self.drawln( "") # Display Robot Modes and Information
        self.drawln( f"Special:        {self.robot.special}")
        self.drawln( f"Rotation Mode:  {self.robot.rotationMode.current()}")
        self.drawln( f"Elevator Mode:  {self.robot.elevatorMode.current()}")
        self.drawln( f"Rotation Speed: {self.robot.spinSpeedMode.current()}")
        self.drawln( f"Pointing Angle: {self.robot.pointing: 7.2f}")
        self.drawln( f"Heading Angle:  {self.robot.heading: 7.2f}")