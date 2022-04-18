from dataclasses import dataclass
from GARCH import GARCH

class InsufficientResources(Exception):
    pass

class NoRecipe(Exception)

@dataclass()
class AssetQty:
    name: str
    qty: int

class AssetPortfolio():
    """Container for a bunch of assets"""
    def __init__(self):
        productive_asset_names = ["obtainium", "eludium", "unobtainium", "widget", "gizmo", "doohickey", "gadget"]
        self.money = 1000
        self.productive_assets = {
            "obtainium": RawResource(init_value = 100, b = 0.25, c = 0.2),
            "eludium": RawResource(init_value = 500, b = 0.35, c = 0.25),
            "unobtainium": RawResource(init_value = 20000, b = 0.4, c = 0.4),
            "widget": IntermediateProduct(),
            "gizmo": IntermediateProduct(),
            "doohickey": FinalGood(),
            "gadget": FinalGood()
        }
    
    
    def purchase_asset(self, asset_name: str, qty: int):
        """Purchase a number of assets at the current market price"""
        asset = self.productive_assets[asset_name]
        price = asset.get_price_at_period(period=len(asset._price_history))
        if self.money < price * qty:
            raise InsufficientResources("Not enough money to purchase {qty}x {asset_name}")
        self.money -= (price * qty)
        self.productive_assets[asset_name].qty -= qty

    def produce_asset(asset_name: str, qty: int):
        """produce a particular asset, consuming stockpiled resources
        TODO: buy them at current market price, maybe every resource has an autobuy setting?
        """
        recipe = self.productive_assets[asset_name].recipe
        if not recipe:
            raise NoRecipe("No recipe for {asset_name}")
        # check to ensure we have sufficient material to produce
        # we need to check all resources before spending any of them
        for ingredient in recipe:
            asset = self.productive_assets[ingredient.name]
            if asset.qty < (ingredient.qty * qty):
                raise InsufficientResources("Insufficient {ingredient.name} to produce {asset_name}")
        # then produce
        for ingredient in recipe:
            self.productive_assets[ingredient.name].qty -= ingredient.qty
        self.productive_assets[asset_name].qty += qty

        



class ProductiveAsset(GARCH):
    """Productive assets are assets used in the production of other assets, or produced themselves
    
    They inheret from GARCH to simulate a market you can buy/sell them on"""

    def __init__(self):
        super().__init__()
        self.recipe = None
        self._qty = 0
    
    @property
    def qty(self):
        return self._qty
    
    @qty.setter
    def qty(self, value):
        if (self.qty - value) < 0:
            raise InsufficientResources("Can not reduce asset quantity below zero")
        self._qty = value
    
    def par_value_set_trigger(self, period):
        # is called every 1000 intervals
        pass
        # self.par_value = self._price_history[period-1]


class RawResource(ProductiveAsset):
    """Raw resources are consumed to produce other products"""
    def __init__(self):
        super().__init__()

class Obtainium(RawResource):
    def __init__(self):
        super().__init__(init_value = 100, b = 0.25, c = 0.2)

class Eludium(RawResource):
    def __init__(self):
        super().__init__(init_value = 500, b = 0.35, c = 0.25)

# class Unobtainium(RawResource):
#     def __init__(self):
#         super().__init__(init_value = 20000, b = 0.4, c = 0.4)


class IntermediateProduct(ProductiveAsset):
    """Intermediate products are created from some products and consumed by others"""
    def __init__(self):
        super().__init__()

class Widget(IntermediateProduct):
    def __init__(self):
        super().__init__()
        self.recipe = [AssetQty("obtanium", 2), AssetQty("eludium", 1)]

# class Gizmo(IntermediateProduct):
#     def __init__(self):
#         super().__init__()


class FinalGood(ProductiveAsset):
    """Final goods are consuemd """
    def __init__(self):
        super().__init__()

# class Doohickey(FinalGood):
#     def __init__(self):
#         super().__init__()

# class Gadget(FinalGood):
#     def __init__(self):
#         super().__init__()

my_asset = ProductiveAsset(b = 0.25, c = 0.2)
my_asset.gen_price_figure(0, 21600)

obtanium = RawResource()
