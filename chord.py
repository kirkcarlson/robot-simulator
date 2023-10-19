'''Chord class for detecting single button and button group presses'''
class Chord (): # this whole thing is tied to a controller...
    def __init__():
        buttons = []           # list of active button indices
        buttonStates = {}      # dictionary of button states 
        lastChordStates = {}   # dictionary of last button/chord states 
        pressChordActions = {} # dictionary of chord actions

    def onPress (buttonIndices, action):
        for buttonIndex in buttonIndices
            if buttonIndex not in self.buttons:
                add it to self.buttons
                add idle cord state for buttonIndices
        if buttonIndices is in chordActions:
            remove the old entry
        add buttonIndices to the chordActions
        add lastChordState  = idle
    
    def check():
        self.buttonStates = [] # reset the list
        for button in range (self.buttons):
            if controller.get_button( button):
                self.buttonStates.append (button) # buttons not on list are idle
        for chordAction in chordActions
            released = true
            pressed = true
            for button in chordAction[0]:  #all buttons have to be same to alter chord state
                released &= !self.buttonStates[ button]   # any pressed button will make false
                pressed &= self.buttonStates[ button]    # any released button will make false
            if pressed:
                if !self.lastChordStates( chordAction[0]):
                    #perform the action for the chord
                    action = chordAction[1]
                    action()
                    self.lastChordStates( chordAction[0]) = True
            elif released:
                self.lastChordStates( chordAction[0]) = False

chord = Chord()            

chord.onPress(5, ()->print("button 5 pressed"))
chord.onPress(4, ()->print("button 4 pressed"))
chord.onPress((4,5), ()->print("buttons 4 and 5 pressed"))

'''
Also need to have a configuration to map buttons, hats and axes to functions
Play around with chords for a while

class Chord ():
    data
        list of Buttons (like: 0,1,2,3,01,23,02,13)
        current button state
        last button state
        buttons action dictionary
    def __init__:
        create chord
        create empty list of buttons
        create empty button-action dictionary
    def checkChords():
        read the list of buttons
        determine which have just been pressed
        do the action for the button/buttons pressed
    def onButton (button, action): ... one time action
        add button to scan list
        add (button, action) to buttons action dictionary
    def while (button, action): ... repeated action
        add button
        add (button, action) to buttons action dictionary

This has state... for the buttonActionDictionary and the last state of the list of buttons
onButton... could add entries to the buttonActionDictionary and the list of buttons

Start small and then build up... start with the paddles and maybe the tank mode switch
  eventually get rid of the isEdge function out of the Mode module

  Modes are part of a robot, and switch and chord states is part of a robot
  These are connected only by assignment... this button controls that mode:

'''



# this should be a database if other types of controller are allowed
# button indices
BUTTON_A_INDEX = 0
BUTTON_B_INDEX = 1
BUTTON_X_INDEX = 2
BUTTON_Y_INDEX = 3

RIGHT_PADDLE = 0
LEFT_PADDLE = 1


#class Controller (pygame.joystick.Joystick):
#    """ A class for a generic XBOX joystick and its current state"""
#    def id_check( self):
#        print (f"Id for controller is {self.device_index}")
        
'''
    def __init__(self, device_index):
        super().__init__( device_index)
        #super.device_index = device_index
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

        # past button and chord states
        buttonAlast = False
        buttonBlast = False 
        buttonXlast = False
        buttonYlast = False
        buttonABlast = False
        buttonXYlast = False
        buttonAXlast = False
        buttonBYlast = False
'''
'''
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


