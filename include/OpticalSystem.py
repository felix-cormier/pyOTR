class OpticalSystem():
    def __init__(self):
        self.components = []

    def AddComponent(self, component):
        self.components.append(component)

    def TraceRays(self, X, V):
        if len(self.components) == 0:
           # print('ERROR! No optical components were declared.\nExiting...')
           # return 0, 0 #original
            return X, V
        for comp in self.components:
            X, V = comp.RaysTransport(X, V)
        return X, V
