from dataclasses import dataclass
from GARCH import GARCH

class InsufficientResources(Exception):
    pass

class NoRecipe(Exception):
    pass

@dataclass()
class AssetQty:
    name: str
    qty: int

class AssetPortfolio():
    """Container for a bunch of assets"""
    def __init__(self):
        self.money = 1000
        self.productive_assets = {
            "obtainium": Obtainium(),
            "eludium": Eludium(),
            "unobtainium": Unobtainium(),
            "widget": Widget(),
            "gizmo": Gizmo(),
            "doohickey": Doohickey(),
            "gadget": Gadget()
        }
    
    def get_portfolio_info(self) -> dict:
        pi = {label: asset.qty for label, asset in self.productive_assets.items()}
        pi["money"] = self.money
        return pi
    
    def buy_asset(self, asset_name: str, qty: int):
        """Purchase a number of assets at the current market price"""
        if qty == 0:
            return
        asset = self.productive_assets[asset_name]
        price = asset.get_price()
        if self.money < price * qty:
            raise InsufficientResources(f"Not enough money to purchase {qty}x {asset_name}")
        self.money -= (price * qty)
        self.productive_assets[asset_name].qty += qty
    
    def sell_asset(self, asset_name: str, qty: int):
        """Sell a number of assets at the current market price"""
        if qty == 0:
            return
        asset = self.productive_assets[asset_name]
        if qty > asset.qty:
            raise InsufficientResources(f"Not enough {asset_name} to sell {qty}")
        self.money += (asset.get_price() * qty)
        self.productive_assets[asset_name].qty -= qty

        



class ProductiveAsset(GARCH):
    """Productive assets are assets used in the production of other assets, or produced themselves
    
    They inheret from GARCH to simulate a market you can buy/sell them on"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recipe: list = []
        self._qty: int = 0
    
    @property
    def qty(self):
        return self._qty
    
    @qty.setter
    def qty(self, value):
        if (value) < 0:
            raise InsufficientResources("Can not reduce asset quantity below zero")
        self._qty = value
    
    def par_value_set_trigger(self, period):
        # is called every 1000 intervals
        pass
        # self.par_value = self._price_history[period-1]

class Recipe:
    def __init__(self, product:str, ingredients: list, time: int):
        self.product = product
        self.ingredients = ingredients
        self.time = time

class RawResource(ProductiveAsset):
    """Raw resources are consumed to produce other products"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Obtainium(RawResource):
    def __init__(self):
        super().__init__(init_value = 100, b = 0.25, c = 0.2)

class Eludium(RawResource):
    def __init__(self):
        super().__init__(init_value = 500, b = 0.35, c = 0.25)

class Unobtainium(RawResource):
    def __init__(self):
        super().__init__(init_value = 20000, b = 0.4, c = 0.4)


class IntermediateProduct(ProductiveAsset):
    """Intermediate products are created from some products and consumed by others"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Widget(IntermediateProduct):
    def __init__(self):
        super().__init__(init_value = 1000, b = 0.25, c = 0.2)
        # base cost = 200 + 500 = 700
        self.recipe = Recipe("widget", [AssetQty("obtainium", 2), AssetQty("eludium", 1)], 5)

class Gizmo(IntermediateProduct):
    def __init__(self):
        super().__init__(init_value = 3500, b = 0.35, c = 0.25)
        # base cost = 1100 + 1500 = 2600
        self.recipe = Recipe("gizmo", [AssetQty("obtainium", 11), AssetQty("eludium", 3)], 15)


class FinalGood(ProductiveAsset):
    """Final goods are consuemd """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Doohickey(FinalGood):
    def __init__(self):
        super().__init__(init_value = 10000, b = 0.25, c = 0.2)
        # base cost = 2000 + 2000 + 3500 = 7500
        self.recipe = Recipe("doohickey", [AssetQty("obtainium", 20), AssetQty("eludium", 4), AssetQty("widget", 1)], 60)

class Gadget(FinalGood):
    def __init__(self):
        super().__init__(init_value = 50000, b = 0.35, c = 0.25)
        # base cost = 5500 + 20000 + 6000 + 7000 = 38500
        self.recipe = Recipe("gadget", [AssetQty("eludium", 11), AssetQty("unobtainium", 1), AssetQty("widget", 6), AssetQty("gizmo", 2)], 300)

if __name__ == "__main__":
    my_asset = ProductiveAsset(b = 0.25, c = 0.2)
    my_asset.gen_price_figure(0, 21600)

