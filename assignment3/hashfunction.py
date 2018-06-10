class hashfunction(object):

    def __init__(self, _a, _b, _mod):
        self.a = _a
        self.b = _b
        self.mod = _mod

    def compute(self, x):
        return (self.a*x + self.b) % self.mod