from investor import Investor
from assets import RawResource, IntermediateProduct, FinalGood

class Game:
    def __init__(self):
        self.current_period = 0
        self.assets = {
            'Raw': {
                'Obtanium': RawResource(init_value = 100, b = 0.25, c = 0.2),
                'Eludium': RawResource(init_value = 500, b = 0.35, c = 0.25),
                'Unobtanium': RawResource(init_value = 20000, b = 0.4, c = 0.4),
            },
            'Intermediate': {
                'Widget': IntermediateProduct(),
                'Gizmo': IntermediateProduct(),
            },
            'Final': {
                'Doohickey': FinalGood(),
                'Gadget': FinalGood(),
            },
        }
        self.investor = Investor()
    
    def increment_time(self):
        pass
