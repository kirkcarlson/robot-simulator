'''Chord class for detecting single button and button group presses'''

#### CONSTANTS ####
BUTTON_A     = 0
BUTTON_B     = 1
BUTTON_X     = 2
BUTTON_Y     = 3

LEFT_PADDLE  = 0
RIGHT_PADDLE = 1

LEFT_BUTTON  = 4
RIGHT_BUTTON = 5
PAGE_BUTTON  = 6
LIST_BUTTON  = 7
XBOX_BUTTON  = 8

LEFT_JOY_BUTTON  =  9
RIGHT_JOY_BUTTON = 10

IDLE       = 0
PRESSED    = 1
OVERRIDDEN = 2

#### CLASSES ####
class Chord (): # this whole thing is tied to a controller...
    # a chord is a set of one or more buttons)
    def __init__( self):
        self.buttons = {}           # dictionary of button being monitored and state (IDLE, PRESSED)
        self.chordActions = {}      # dictionary of chord actions and states
                                    # { (chord) : {'state': state,'press:': action, 'release': action, 'while':action}}
                                    #               state can be: idle, overridden, pressed

    def onPress (self, chord, action): # add button-action to chordActions
        # chord can be a single button or a tuple of buttons
        if type( chord) is list:
            chord = set( chord )
        elif type( chord) is not set:
            chord = set( [ chord] )
        chord = frozenset( chord)
        for button in chord:
            if button not in self.buttons:
                if controller.get_button(button):
                    self.buttons[button] = PRESSED
                else:
                    self.buttons[button] = IDLE
        if self.chordActions == {} or chord not in self.chordActions:
            self.chordActions[chord] = {'state':IDLE, 'press': action}
        else:
            self.chordActions[ chord]['press'] = action

    def onRelease (self, chord, action): # add button-action to chordActions
        if type( chord) is list:
            chord = set( chord )
        elif type( chord) is not set:
            chord = set( [ chord] )
        chord = frozenset( chord)
        for button in chord:
            if button not in self.buttons:
                if controller.get_button(button):
                    self.buttons[button] = PRESSED
                else:
                    self.buttons[button] = IDLE
        if chord not in self.chordActions:
            self.chordActions[chord] = {'state':IDLE, 'release': action}
        else:
            self.chordActions[ chord]['release'] = action

    def whilePressed (self, chord, action): # add button-action to chordActions
        if type( chord) is list:
            chord = set( chord )
        elif type( chord) is not set:
            chord = set( [ chord] )
        chord = frozenset( chord)
        for button in chord:
            if button not in self.buttons:
                if controller.get_button(button):
                    self.buttons[button] = PRESSED
                else:
                    self.buttons[button] = IDLE
        if chord not in self.chordActions:
            self.chordActions[chord] = {'state':IDLE, 'while': action}
        else:
            self.chordActions[ chord]['while'] = action


    def removeOnPress( self, button):
        self.chordActions[chord].pop( "press")
        if len(self.chordActions[chord]) == 1: # just the state left
            self.chordActions.remove (chord)
            self._resetButtons()

    def removeOnRelease( self, chord):
        self.chordActions[chord].pop( "release")
        if len(self.chordActions[chord]) == 1: # just the state left
            self.chordActions.remove (chord)
            self._resetButtons()

    def removeWhile( self, chord):
        self.chordActions[chord].pop( "while")
        if len(self.chordActions[chord]) == 1: # just the state left
            self.chordActions.remove (chord)
            self._resetButtons()

    def removeAll( self, chord):
        self.chordActions.remove( chord)
        self._resetButtons()

    def _resetButtons( self):
        self.buttons = {}           # dictionary of active button indices
        for chord in self.chordActions.keys:
            for button in chord:
                if button not in self.buttons:
                    if controller.get_button(button):
                        self.buttons[button] = PRESSED
                    else:
                        self.buttons[button] = IDLE


    def _overrideSubsets( self, chord):
        for key, chordAction in self.chordActions.items():
            allKeyButtonsInChord = True
            for button in key:
                if button not in chord:
                    allKeyButtonsInChord = False
            if allKeyButtonsInChord:
                if chordAction['state'] == PRESSED:
                    if 'press' in chordAction:
                        chordAction[ 'press'] ()
                self.chordActions[key]['state'] = OVERRIDDEN


    def _releaseSubsetOverrides( self, chord):
        for key in self.chordActions:
            allKeyButtonsInChord = True
            for button in key:
                if button not in chord:
                    allKeyButtonsInChord = False
            if allKeyButtonsInChord:
                self.chordActions[key]['state'] = IDLE


    def check( self):
        print (f"check called")
        buttonStates = [] # reset the list
        for button in self.buttons:
            if controller.get_button( button):
                buttonStates.append (button) # buttons not on list are idle
        for key, chordAction in self.chordActions.items():
            print (f"check key= {key} buttonStates= {buttonStates}")
            released = True
            pressed = True
            for button in key:  #all buttons have to be same to alter chord state
                released &= button not in buttonStates   # any pressed button will make False
                pressed &= button in buttonStates    # any released button will make False
            print (f"check key= {key} released = {released} pressed = {pressed}")
            if pressed:
                print (f"a chord {key} : {chordAction} is pressed")
                if chordAction['state'] == IDLE: # PRESSED is true
                    if 'pressed' in chordAction:
                        chordAction[ 'pressed'] ()
                        print (f"pressed action fired {chordAction['pressed']}")
                    self.chordActions[key]['state'] = PRESSED
                    self._overrideSubsets( key)
                else: # chord is being held, so WHILE is True
                    if 'while' in chordAction:
                        chordAction[ 'while'] ()
            elif released: #RELEASE IS TRUE
                print (f"a chord {key} is released")
                if chordAction['state'] == PRESSED: # PRESSED is true
                    if 'released' in chordAction:
                        chordAction[ 'release'] ()
                    self.chordActions[key]['state'] = IDLE
                    self._releaseSubsetOverride( key)
            else:
                pass
                #was pressed, so holding the override until all released



'''
onButton... could add entries to the buttonActionDictionary and the list of buttons

Start small and then build up... start with the paddles and maybe the tank mode switch
  eventually get rid of the isEdge function out of the Mode module

  Modes are part of a robot, and switch and chord states are part of a robot
  These are connected only by assignment... this button controls that mode:

  robot
   + joystick
   + visual thing on screen
   + state
     + position, heading, pointing...
     * modes
     * chords
'''
################################test code


class Tester ():
    def __init__(self):
        self. buttonList = []

    def setButtonList( self, list):
        self.buttonList = list
        print (f"**buttonList Changed**** {list}")

    def get_button (self, number):
        if number in self.buttonList:
            return True
        else:
            return False

count = 0

def progress (start=None):
    global count
    if start is not None:
        count = start
    print (f"Step {count}")
    count += 1

keyManager = Chord()
controller = Tester()
progress()
keyManager.onPress(       5, lambda : print("    button 5 pressed"))
keyManager.onRelease(     5, lambda : print("    button 5 released"))
keyManager.onPress(       4, lambda : print("    button 4 pressed"))
keyManager.onRelease(     4, lambda : print("    button 4 released"))
keyManager.onPress(   (4,5), lambda : print("    chord 4 5 pressed"))
keyManager.onRelease( (4,5), lambda : print("    chord 4 5 released"))
print (f"active buttons {keyManager.buttons}")
print (f"active actions {keyManager.chordActions}")
progress()
controller.setButtonList( [4])
keyManager.check()                     # should see "button 4 pressed"
progress()
keyManager.check()
progress()
controller.setButtonList( [5])
progress()
keyManager.check()                     # should see "button 5 pressed"
progress()
keyManager.check()
progress()
controller.setButtonList( [4, 5])
progress()
keyManager.check()                     # should see "chord 4 5 pressed", "button 5 released"
progress()
keyManager.check()
controller.setButtonList( [4])
keyManager.check()                     # should see "chord 4 5 release"
progress()
keyManager.check()
controller.setButtonList( [])
keyManager.check()                     # should see "button 4 released"

