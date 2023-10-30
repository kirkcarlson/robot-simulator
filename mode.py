'''Mode Class for creating modal controls'''

class Mode:  # class for simple modal controls
    def __init__( self, modes): #modes has to be a dictionary of key, value pairs, keys are numeric, values are strings
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


    def setMode( self, mode):
        self.mode = mode


    def reset( self):
        self.mode = 0


    def current( self):
        return self.modes [self.mode]


class CommandMode:  # class for modal controls of a command function
    def __init__( self, modes, commands): #modes has to be a dictionary of key, value pairs, keys are numeric, values are strings
        self.modes = modes
        self.commands = commands
        self.mode = 0
        self.lastTrigger = 0
        self.command = lambda  : 0 # a command function associated with the modal control


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
        self.command = self.commands[ self.mode]


    def advanceCyclic( self):
        self.mode += 1
        if self.mode >= len(self.modes):
            self.mode = 0
        self.command = self.commands[ self.mode]
    
    
    def setMode( self, mode):
        self.mode = mode
        self.command = self.commands[ mode]


    def reset( self):
        self.mode = 0


    def current( self):
        return self.modes [self.mode]
