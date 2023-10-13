'''Mode Class for creating modal controls'''

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

    def reset( self):
        self.mode = 0

    def current( self):
        return self.modes [self.mode]
