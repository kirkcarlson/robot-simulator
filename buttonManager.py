'''buttonManager class for detecting single button and button group presses'''

#### CONSTANTS ####
DEBUG = False

A_BUTTON = 0
B_BUTTON = 1
X_BUTTON = 2
Y_BUTTON = 3
LEFT_BUTTON = 4 # above left trigger
RIGHT_BUTTON = 5 # above right trigger
VIEW_BUTTON = 6 # overlapped squares
MENU_BUTTON = 7 # hamburger strips
XBOX_BUTTON = 8 # X-Box logo
LEFT_JOY_BUTTON  =  9
RIGHT_JOY_BUTTON = 10

#possible states within chordCommands.state
IDLE       = 0
PRESSED    = 1
OVERRIDDEN = 2

#### CLASSES ####
def dprint( string):
    if DEBUG:
        print( string)

class ButtonManager (): # this whole thing is tied to a joystick...
    # a chord is a list of one or more buttons
    def __init__( self, joystick):
        self.joystick = joystick
        self.monitoredButtons = []  # list of buttons being monitored
        self.chordCommands = []      # list of chordCommand dictionaries
                                    # [ {'chord': chord,    ... sorted list of keys
                                    #     'state': state,    ...can be: IDLE, PRESSED, OVERRIDDEN
                                    #     'press:': command,   ...command is reference to a function or method
                                    #     'release': command,
                                    #     'while': command}]()
                                    # list is in order of precedence (longer before shorter)

    def _addCommandToChordCommands (self, chord, command, commandType): # add button-command to chordCommands
        # chord is a list of one or more buttons
        if isinstance(chord, set) or isinstance(chord,tuple):
            chord = list(chord)
        if not isinstance(chord, list):
            chord = [chord]
        chord.sort()
        for button in chord:
            if button not in self.monitoredButtons:
                self.monitoredButtons.append( button)
                self.monitoredButtons.sort()

        # add chord{} to chordCommand or command to chordCommands[chord]
        found = False
        for i in range (len(self.chordCommands)):
            dprint(f"--checking {type(chord)}:{chord} against {type(self.chordCommands[i]['chord'])}{self.chordCommands[i]['chord']}")
            if self.chordCommands[i]['chord'] == chord:
                dprint("----modifying chordCommands")
                found = True
                self.chordCommands[i][commandType]= command
                break
        if not found:        
            dprint(f"adding chord{chord} to self.chordCommands")
            self.chordCommands.append ({'chord': chord, 'state': self._getChordActivity( chord), commandType: command})
            # sort the chordCommands by precedence: longer chords higher than shorter chords
            self.chordCommands = (sorted( self.chordCommands, key=lambda chordCommand: len(chordCommand['chord']), reverse=True))

        
    def onPress (self, chord, command): # add press button-command to chordCommands
        self._addCommandToChordCommands( chord, command, 'press')

    
    def onRelease (self, chord, command): # add release button-command to chordCommands
        self._addCommandToChordCommands( chord, command, 'release')

    
    def onWhile (self, chord, command): # add while button-command to chordCommands
        self._addCommandToChordCommands( chord, command, 'while')


    def _removeCommandFromChordCommands (self, chord, commandType): # remove button-command from chordCommands
        chord.sort() # to make sure buttons in same order for compare to work
        for i in range (len(self.chordCommands)):
            if self.chordCommands[i]['chord'] == chord:
                if self.chordCommands[i][commandType] is not None:
                    self.chordCommands[i].pop(commandType)
                if len(self.chordCommands[i]) == 2: # just the chord and state left
                    self.chordCommands.pop(i)
                    self._resetButtons()
                break

    
    def removeOnPress( self, chord):
        self._removeCommandFromChordCommands (chord, 'press') # remove button-command from chordCommands


    def removeOnRelease( self, chord):
        self._removeCommandFromChordCommands (chord, 'release') # remove button-command from chordCommands


    def removeWhile( self, chord):
        self._removeCommandFromChordCommands (chord, 'while') # remove button-command from chordCommands


    def removeChord( self, chord):
        chord.sort() # to make sure buttons in same order for compare to work
        for i in range (len(self.chordCommands)):
            if self.chordCommands[i]['chord'] == chord:
                self.chordCommands.pop(i)
                self._resetButtons()
                break


    def _getChordActivity( self, chord):
        activity = PRESSED
        for button in chord:
            if not self.joystick.get_button( button):
                activity = IDLE
                break
        return activity


    def _resetButtons( self):
        self.monitoredButtons = {}           # dictionary of active button indices
        for i in range (len(self.chordCommands)):
            for button in self.chordCommands[i]['chord']:
                if button not in self.monitoredButtons:
                    self.monitoredButtons.append(button)


    def _overrideSubsets( self, chord):
        for i in range (len(self.chordCommands)):
            allKeyButtonsInChord = True
            key = self.chordCommands[i]['chord']
            for button in key:
                if button not in chord:   
                    allKeyButtonsInChord = False
                    break
            if allKeyButtonsInChord and len(key) != len( chord): #chord is a proper subset of key
                self.chordCommands[i]['state'] = OVERRIDDEN
                dprint (f"   overriding key:{key}")


    def _releaseSubsetOverrides( self, chord): # release all key subsets of chord
        for i in range (len(self.chordCommands)):
            allKeyButtonsInChord = True
            key = self.chordCommands[i]['chord']
            for button in key:
                if button not in chord:
                    allKeyButtonsInChord = False
                    break
            if allKeyButtonsInChord and len(key) != len( chord): #chord is a proper subset of key
                self.chordCommands[i]['state'] = IDLE


    def getActiveButtons( self):
        buttonActivity = []
        for button in self.monitoredButtons:
            if self.joystick.get_button( button):
                buttonActivity.append (button) # only active buttons are on list
        return buttonActivity


    def update( self, activeButtons):
        dprint (f"    update called, monitoring:{self.monitoredButtons} active:{activeButtons}")

        for i in range( len( self.chordCommands)):
            key = self.chordCommands[i]['chord']
            dprint (f"        updating chord:{key}")
            released = True
            pressed = True
            for button in key:  #all buttons have to be same to alter chord state
                released &= button not in activeButtons   # any pressed button will make False
                pressed &= button in activeButtons    # any released button will make False
            if pressed:
                dprint (f"            active chord:{key} : {self.chordCommands[i]}")
                if self.chordCommands[i]['state'] == IDLE: # making inactive to active transition
                    if 'press' in self.chordCommands[i]:
                        self.chordCommands[i][ 'press'] ()
                        dprint (f"            press command fired")
                    self.chordCommands[i]['state'] = PRESSED
                    self._overrideSubsets( key)
                    dprint(f"        double check on chordCommands:{self.chordCommands[i]}")
                elif self.chordCommands[i]['state'] == OVERRIDDEN: # button is part of another chord
                    pass
                else: # chord is being held, so WHILE is True
                    if 'while' in self.chordCommands[i]:
                        self.chordCommands[i][ 'while'] ()
                        dprint (f"            while command fired")
            elif released: #RELEASE IS TRUE
                dprint (f"            inactive chord {key} : {self.chordCommands[i]}")
                if self.chordCommands[i]['state'] == PRESSED: # making active to inactive transition
                    if 'release' in self.chordCommands[i]:
                        self.chordCommands[i][ 'release'] ()
                        dprint (f"            release command fired")
                    self.chordCommands[i]['state'] = IDLE
                    self._releaseSubsetOverrides( key)
            else:
                pass
                #was pressed, so holding the override until all released



'''
onButton... could add entries to the buttonCommandDictionary and the list of buttons

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

''' DEBUG CODE
class Tester ():
    def __init__(self):
        self. buttonList = []

    def setButtonList( self, list):
        self.buttonList = list
        dprint (f"**buttonList Changed**** {list}")

    def get_button (self, number):
        if number in self.buttonList:
            return True
        else:
            return False

count = 0

def progress (comment, start=None):
    global count
    if start is not None:
        count = start
    dprint (f"Step {count}: {comment}")
    count += 1

controller = Tester()
keyManager = ButtonManager( controller)
progress("\n\nStarting up")
keyManager.onPress(       5, lambda : print("button 5 pressed"))
keyManager.onRelease(     5, lambda : print("button 5 released"))
keyManager.onPress(       4, lambda : print("button 4 pressed"))
keyManager.onRelease(     4, lambda : print("button 4 released"))
keyManager.onPress(   [4,5], lambda : print("chord 4 5 pressed"))
keyManager.onRelease( [4,5], lambda : print("chord 4 5 released"))
progress('')
print (f"active buttons {keyManager.monitoredButtons}")
print (f"active commands {keyManager.chordCommands}")
progress( 'should see "button 4 pressed"')
keyManager.update( [4])
progress('')
keyManager.update( [4])

progress( 'should see "button 4 released"')
keyManager.update( [])
progress('')
keyManager.update( [])

progress( 'should see "button 5 pressed"')
keyManager.update( [5])
progress('')
keyManager.update( [5])

progress( 'should see "chord 4 5 pressed"')
keyManager.update( [4, 5])
progress('')
keyManager.update( [4, 5])

progress( 'chord 4 5 is holding until all released"')
keyManager.update( [4])
progress('')
keyManager.update( [4])

progress('should see "button 4 5 released"')
keyManager.update( [])
keyManager.update( [])

progress('should not see anything')
keyManager.onPress( (5,4), lambda : print("chord 5 4 pressed"))
keyManager.update( [])
print(f"chord commands: {keyManager.chordCommands}")

progress('should see "button 4 5 pressed"')
keyManager.update( [5,4])

progress('should see "button 4 5 released"')
keyManager.update( [])


#'''