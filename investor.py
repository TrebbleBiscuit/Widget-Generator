import assets as a

class Investor:
    def __init__(self):
        self.portfolio = a.AssetPortfolio()
        self.production = {name: 0 for name, asset in self.portfolio.productive_assets.items() if asset.recipe}
        self.prod_queue = []
    
    def produce_asset(self, asset_name: str, qty: int):
        """produce a particular asset, consuming stockpiled resources
        TODO: buy them at current market price, maybe every resource has an autobuy setting?
        """
        if qty == 0:
            return
        recipe = self.portfolio.productive_assets[asset_name].recipe
        if not recipe:
            raise a.NoRecipe(f"No recipe for {asset_name}")
        # check to ensure we have sufficient material to produce
        # we need to check all resources before spending any of them
        for ingredient in recipe.ingredients:
            asset = self.portfolio.productive_assets[ingredient.name]
            if asset.qty < (ingredient.qty * qty):
                raise a.InsufficientResources(f"Insufficient {ingredient.name} to produce {asset_name}")
        # then spend
        for ingredient in recipe.ingredients:
            self.portfolio.productive_assets[ingredient.name].qty -= ingredient.qty
        # finally queue up production
        self.prod_queue.append(recipe)
    
    def increment_prod_queue(self):
        if not self.prod_queue:
            return
        recipe = self.prod_queue[0]
        if recipe.time <= 0:
            self.prod_queue.pop(0)
            self.portfolio.productive_assets[recipe.product].qty += 1
            self.increment_prod_queue()
        elif recipe.time == 1:
            self.prod_queue.pop(0)
            self.portfolio.productive_assets[recipe.product].qty += 1
        else:
            recipe.time -= 1
    
    def get_prod_queue(self):
        return str(self.prod_queue)
    
    def mass_produce(self):
        """Produces items in quantities specified by self.production"""
        for asset_name, qty in self.production.items():
            try:
                # TODO: need this to fn differently, not take time?
                self.produce_asset(asset_name=asset_name, qty=qty)
            except a.InsufficientResources as exc:
                print(exc)
    
    def net_worth(self):
        total = self.portfolio.money
        for name, asset in self.portfolio.productive_assets.items():
            total += (asset.qty * asset.get_price())
        return total
    
    def income(self) -> dict[str, dict[str, float]]:
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
            if not recipe:
                continue
            for ingredient in recipe.ingredients:
                price = self.productive_assets[ingredient.name].get_price()
                cost = price * ingredient.qty * prod_qty
                income_info[name]["cost"] = cost
        return income_info
