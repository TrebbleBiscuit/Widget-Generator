from investor import Investor

class Game:
    def __init__(self):
        self.current_period = 0
        self._investors = {}
        # self.investor = Investor()
    
    def get_investor(self, username: str):
        try:
            return self._investors[username]
        except KeyError:
            self._investors[username] = Investor()
            return self._investors[username]
    
    def increment_time(self, by = 1):
        for x in range(by):
            # much less efficient but allows production (eventually auto sales) each period at accurate prices
            self.current_period += 1
            for name, investor in self._investors.items():
                for name, asset in investor.portfolio.productive_assets.items():
                    # update all asset prices to current period
                    asset.get_price(period = self.current_period)
                investor.mass_produce()
                investor.increment_prod_queue()

if __name__ == "__main__":
    print("hello world")
    game = Game()
    game.increment_time(10)
    investor = game.get_investor("test user")
    print(f"Money: {investor.portfolio.money}")
    investor.portfolio.buy_asset("obtainium", 2)
    investor.portfolio.buy_asset("eludium", 1)
    investor.produce_asset("widget", 1)
    print(f"Queue: {investor.prod_queue}")
    game.increment_time(5)
    print(f"Queue: {investor.prod_queue}")
    investor.portfolio.sell_asset("widget", 10)
    print(f"Money: {investor.portfolio.money}")
    print(investor.portfolio.get_portfolio_info())

