from typing import Union
from GARCH import GARCH


class Asset(GARCH):
    def __init__(self, init_value: Union[float, int] = 100, b: float = 0.3, c = 0.2):
        super().__init__(init_value, b = 0.3, c = 0.2)
        # self.init_value = init_value  # initial price
        # self.eq_price = init_value  # equilibrium price
        # self._price = [init_value]  # _price is a list of prices
    
    def par_value_set_trigger(self, period):
        pass
        # return 100
        # if period % 1000 == 0:
        #     return self.init_value + (period/1000)


    # def get_price(self, period):
    #     try:
    #         return self._price[period]
    #     except IndexError:
    #         for x in range(len(self._price), period + 1):
    #             self._price[period] = self._price[period - 1] + 0.0001
    #         return self._price[period]

    # def _bias_price(self, price):
    #     """ Slightly bias price towards equilibrium """
    #     bias_threshold = 0.08
    #     bias_ratio = 1/100  # ratio of the % from eq_price to bias
    #     percent_diff = (price - self.eq_price) / self.eq_price
    #     if abs(percent_diff) > bias_threshold:
    #         # price pressure towards equlibrium
    #         return price * (1 - (percent_diff * bias_ratio))
    #     else:
    #         return price

    # def get_eq_price(self):
    #     pass

    # @property
    # def eq_price(self):
    #     """ Equilibrium price """ 
    #     return self._eq_price


class RawResource(Asset):
    def __init__(self):
        super().__init__()

# class Obtainium(RawResource):
#     def __init__(self):
#         super().__init__(init_value = 100, b = 0.25, c = 0.2)

# class Eludium(RawResource):
#     def __init__(self):
#         super().__init__(init_value = 500, b = 0.35, c = 0.25)

# class Unobtainium(RawResource):
#     def __init__(self):
#         super().__init__(init_value = 20000, b = 0.4, c = 0.4)


class IntermediateProduct(Asset):
    def __init__(self):
        super().__init__()

# class Widget(IntermediateProduct):
#     def __init__(self):
#         super().__init__()

# class Gizmo(IntermediateProduct):
#     def __init__(self):
#         super().__init__()


class FinalGood(Asset):
    def __init__(self):
        super().__init__()

# class Doohickey(FinalGood):
#     def __init__(self):
#         super().__init__()

# class Gadget(FinalGood):
#     def __init__(self):
#         super().__init__()

my_asset = Asset(b = 0.25, c = 0.2)
my_asset.gen_price_figure(21600)
