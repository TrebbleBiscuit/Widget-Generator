class Factory:
    def __init__(self):
        pass

class Refinery(Factory):
    def __init__(self):
        """ Refineries refine Raw Resources into Intermediate Products. """
        super().__init__()

class Processor(Factory):
    def __init__(self):
        """ Processor processes Intermediate Products into Final Goods. """
        super().__init__() 


