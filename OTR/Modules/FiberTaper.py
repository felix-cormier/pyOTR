from OTR.include.OpticalComponent import OpticalComponent

class FiberTaper(OpticalComponent):
    def __init__(self, isGenerator=False, name=None):
        super().__init__(isGenerator, name)
