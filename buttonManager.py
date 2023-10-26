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

#possible states within chordActions.state
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
        self.chordActions = []      # list of chordAction dictionaries
                                    # [ {'chord': chord,    ... sorted list of keys
                                    #     'state': state,    ...can be: IDLE, PRESSED, OVERRIDDEN
                                    #     'press:': action,   ...action is reference to a function or method
                                    #     'release': action,
                                    #     'while':action}]()
                                    # list is in order of precedence (longer before shorter)

    def _addActionToChordActions (self, chord, action, actionType): # add button-action to chordActions
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

        # add chord{} to chordActions or action to chordActions[chord]
        found = False
        for i in range (len(self.chordActions)):
            dprint(f"--checking {type(chord)}:{chord} against {type(self.chordActions[i]['chord'])}{self.chordActions[i]['chord']}")
            if self.chordActions[i]['chord'] == chord:
                dprint("----modifying chordActions")
                found = True
                self.chordActions[i][actionType]= action
                break
        if not found:        
            dprint(f"adding chord{chord} to self.chordActions")
            self.chordActions.append ({'chord': chord, 'state': self._getChordActivity( chord), actionType: action})
            # sort the chordActions by precedence: longer chords higher than shorter chords
            self.chordActions = (sorted( self.chordActions, key=lambda chordAction: len(chordAction['chord']), reverse=True))

        
    def onPress (self, chord, action): # add press button-action to chordActions
        self._addActionToChordActions( chord, action, 'press')

    
    def onRelease (self, chord, action): # add release button-action to chordActions
        self._addActionToChordActions( chord, action, 'release')

    
    def onWhile (self, chord, action): # add while button-action to chordActions
        self._addActionToChordActions( chord, action, 'while')


    def _removeActionFromChordActions (self, chord, actionType): # remove button-action from chordActions
        chord.sort() # to make sure buttons in same order for compare to work
        for i in range (len(self.chordActions)):
            if self.chordActions[i]['chord'] == chord:
                if self.chordActions[i][actionType] is not None:
                    self.chordActions[i].pop(actionType)
                if len(self.chordActions[i]) == 2: # just the chord and state left
                    self.chordActions.pop(i)
                    self._resetButtons()
                break

    
    def removeOnPress( self, chord):
        self._removeActionFromChordActions (chord, 'press') # remove button-action from chordActions


    def removeOnRelease( self, chord):
        self._removeActionFromChordActions (chord, 'release') # remove button-action from chordActions


    def removeWhile( self, chord):
        self._removeActionFromChordActions (chord, 'while') # remove button-action from chordActions


    def removeChord( self, chord):
        chord.sort() # to make sure buttons in same order for compare to work
        for i in range (len(self.chordActions)):
            if self.chordActions[i]['chord'] == chord:
                self.chordActions.pop(i)
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
        for i in range (len(self.chordActions)):
            for button in self.chordActions[i]['chord']:
                if button not in self.monitoredButtons:
                    self.monitoredButtons.append(button)


    def _overrideSubsets( self, chord):
        for i in range (len(self.chordActions)):
            allKeyButtonsInChord = True
            key = self.chordActions[i]['chord']
            for button in key:
                if button not in chord:   
                    allKeyButtonsInChord = False
                    break
            if allKeyButtonsInChord and len(key) != len( chord): #chord is a proper subset of key
                self.chordActions[i]['state'] = OVERRIDDEN
                dprint (f"   overriding key:{key}")


    def _releaseSubsetOverrides( self, chord): # release all key subsets of chord
        for i in range (len(self.chordActions)):
            allKeyButtonsInChord = True
            key = self.chordActions[i]['chord']
            for button in key:
                if button not in chord:
                    allKeyButtonsInChord = False
                    break
            if allKeyButtonsInChord and len(key) != len( chord): #chord is a proper subset of key
                self.chordActions[i]['state'] = IDLE


    def getActiveButtons( self):
        buttonActivity = []
        for button in self.monitoredButtons:
            if self.joystick.get_button( button):
                buttonActivity.append (button) # only active buttons are on list
        return buttonActivity


    def check( self, activeButtons):
        dprint (f"    check called, monitoring:{self.monitoredButtons} active:{activeButtons}")

        for i in range( len( self.chordActions)):
            key = self.chordActions[i]['chord']
            dprint (f"        checking chord:{key}")
            released = True
            pressed = True
            for button in key:  #all buttons have to be same to alter chord state
                released &= button not in activeButtons   # any pressed button will make False
                pressed &= button in activeButtons    # any released button will make False
            if pressed:
                dprint (f"            active chord:{key} : {self.chordActions[i]}")
                if self.chordActions[i]['state'] == IDLE: # making inactive to active transition
                    if 'press' in self.chordActions[i]:
                        self.chordActions[i][ 'press'] ()
                        dprint (f"            press action fired")
                    self.chordActions[i]['state'] = PRESSED
                    self._overrideSubsets( key)
                    dprint(f"        double check on chordActions:{self.chordActions[i]}")
                elif self.chordActions[i]['state'] == OVERRIDDEN: # button is part of another chord
                    pass
                else: # chord is being held, so WHILE is True
                    if 'while' in self.chordActions[i]:
                        self.chordActions[i][ 'while'] ()
                        dprint (f"            while action fired")
            elif released: #RELEASE IS TRUE
                dprint (f"            inactive chord {key} : {self.chordActions[i]}")
                if self.chordActions[i]['state'] == PRESSED: # making active to inactive transition
                    if 'release' in self.chordActions[i]:
                        self.chordActions[i][ 'release'] ()
                        dprint (f"            release action fired")
                    self.chordActions[i]['state'] = IDLE
                    self._releaseSubsetOverrides( key)
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
print (f"active actions {keyManager.chordActions}")
progress( 'should see "button 4 pressed"')
keyManager.check( [4])
progress('')
keyManager.check( [4])

progress( 'should see "button 4 released"')
keyManager.check( [])
progress('')
keyManager.check( [])

progress( 'should see "button 5 pressed"')
keyManager.check( [5])
progress('')
keyManager.check( [5])

progress( 'should see "chord 4 5 pressed"')
keyManager.check( [4, 5])
progress('')
keyManager.check( [4, 5])

progress( 'chord 4 5 is holding until all released"')
keyManager.check( [4])
progress('')
keyManager.check( [4])

progress('should see "button 4 5 released"')
keyManager.check( [])
keyManager.check( [])

progress('should not see anything')
keyManager.onPress( (5,4), lambda : print("chord 5 4 pressed"))
keyManager.check( [])
print(f"chord actions: {keyManager.chordActions}")

progress('should see "button 4 5 pressed"')
keyManager.check( [5,4])

progress('should see "button 4 5 released"')
keyManager.check( [])


#'''