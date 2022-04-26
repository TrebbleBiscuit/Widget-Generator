from investor import Investor

class Game:
    def __init__(self):
        self.current_period = 0
        self.investor = Investor()
    
    def increment_time(self, by = 1):
        for x in range(by):
            # much less efficient but allows production (eventually auto sales) each period at accurate prices
            self.current_period += 1
            for name, asset in self.investor.portfolio.productive_assets.items():
                # update all asset prices to current period
                asset.get_price(period = self.current_period)
            self.investor.mass_produce()

if __name__ == "__main__":
    print("hello world")
    game = Game()
    game.increment_time(10)
    print(f"Money: {game.investor.portfolio.money}")
    game.investor.portfolio.buy_asset("obtainium", 2)
    game.investor.portfolio.buy_asset("eludium", 1)
    game.investor.portfolio.produce_asset("widget", 1)
    game.investor.portfolio.sell_asset("widget", 1)
    print(f"Money: {game.investor.portfolio.money}")
