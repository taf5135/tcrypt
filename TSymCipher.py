class TSymCipher:

    def __init__(self, state):
        self.initial_state = state
        self.state = 0

    def reset(self):
        self.state = self.initial_state

    def getbytes(self, n):
        return [255 for _ in range(n)]

    def getbyte(self):
        return 255
    
    