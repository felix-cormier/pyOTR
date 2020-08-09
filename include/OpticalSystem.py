class OpticalSystem():
    def __init__(self):
        self.components = []

    def AddComponent(self, component):
        self.components.append(component)

    def TraceRays(self, X, V, O):
        if len(self.components) == 0:
            print('ERROR! No optical components were declared.\nExiting...')
            return 0, 0
        for comp in self.components:
            X, V, O = comp.RaysTransport(X, V, O)
        return X, V, O
