from typing import Union


class Asset():
    def __init__(self, init_price: Union[float, int] = 100):
        self.init_price = init_price  # initial price
        self.eq_price = init_price  # equilibrium price
        self._price = [init_price]  # _price is a list of prices

    def get_price(self, period):
        try:
            return self._price[period]
        except IndexError:
            for x in range(len(self._price), period + 1):
                self._price[period] = self._price[period - 1] + 0.0001
            return self._price[period]

    def _bias_price(self, price):
        """ Slightly bias price towards equilibrium """
        bias_threshold = 0.08
        bias_ratio = 1/100  # ratio of the % from eq_price to bias
        percent_diff = (price - self.eq_price) / self.eq_price
        if abs(percent_diff) > bias_threshold:
            # price pressure towards equlibrium
            return price * (1 - (percent_diff * bias_ratio))
        else:
            return price

    def get_eq_price(self):
        pass

    @property
    def eq_price(self):
        """ Equilibrium price """ 
        return self._eq_price






class RawResource(Asset):
    def __init__(self):
        super().__init__()

class Obtainium(RawResource):
    def __init__(self):
        super().__init__()

class Eludium(RawResource):
    def __init__(self):
        super().__init__()

class Unobtainium(RawResource):
    def __init__(self):
        super().__init__()


class IntermediateProduct(Asset):
    def __init__(self):
        super().__init__()

class Widget(IntermediateProduct):
    def __init__(self):
        super().__init__()

class Gizmo(IntermediateProduct):
    def __init__(self):
        super().__init__()


class FinalGood(Asset):
    def __init__(self):
        super().__init__()

class Doohickey(FinalGood):
    def __init__(self):
        super().__init__()

class Gadget(FinalGood):
    def __init__(self):
        super().__init__()

