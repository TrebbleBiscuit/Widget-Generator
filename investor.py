import assets as a

class Investor:
    def __init__(self):
        self.portfolio = a.AssetPortfolio()
        self.production = {name: 0 for name in self.portfolio.productive_assets}
    
    def mass_produce(self):
        """Produces items in quantities specified by self.production"""
        for asset_name in self.portfolio.productive_assets:
            qty = self.production[asset_name]
            try:
                self.portfolio.purchase_asset(asset_name=asset_name, qty=qty)
            except a.InsufficientResources as exc:
                print(exc)
    
    def net_worth(self):
        total = self.portfolio.money
        for name, asset in self.portfolio.productive_assets.items():
            total += (asset.qty * asset.get_price())
        return total
    
    def income(self) -> dict(str, dict(str, float)):
        """Income from mass_produce() based on current prices"""
        income_info = {}
        # {
        #     name: {
        #         "revenue": 10,
        #         "cost": 5,
        #     }
        # }
        for name, prod_qty in self.production.items():
            asset = self.portfolio[name]
            recipe = asset.recipe
            revenue = asset.get_price() * prod_qty
            income_info[name] = {"revenue": revenue}
            if recipe is None:
                continue
            for ingredient in recipe:
                price = self.productive_assets[ingredient.name].get_price()
                cost = price * ingredient.qty * prod_qty
                income_info[name]["cost"] = cost
        return income_info
