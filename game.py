from investor import Investor

class Game:
    def __init__(self):
        self.current_period = 0
        self.investor = Investor()
    
    def increment_time(self, by = 1):
        self.current_period += by
        for name, asset in self.investor.portfolio.productive_assets.items():
            # update all asset prices to current period
            asset.get_price(period = self.current_period)

if __name__ == "__main__":
    print("hello world")
    game = Game()
    game.increment_time(1000)
