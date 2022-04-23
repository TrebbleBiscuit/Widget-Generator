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
