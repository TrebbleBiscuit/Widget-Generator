import numpy as np

RETURN_BIAS = 0.01

class Asset:
    """
    Asset price simulated with a Generalized Auto-Regressive Conditional Heteroskedasticity (GARCH) model.
    """
    def __init__(self, init_value: int, b: float = 0.4, c: float = 0.4):
        self.init_value = init_value
        self.b = b  # ARCH coefficient
        self.c = c  # GARCH coefficient
        self.sigma0 = 0.0002
        self.a = 0.0000002
        self.eps = np.random.normal(0, 1, 5)  # init sims to length 5, later runs fn to sim to len 10
        self.r = np.zeros(5)
        self.sigma = np.ones(5) * self.sigma0
        self.get_price_at_period(100)  # sim to period 100
    
    def get_r_from_last(self, r: float, sig: float) -> tuple([float, float]):
        last_r = r
        last_sig = sig
        new_sig = np.sqrt(self.a + self.b * last_r ** 2 + self.c * last_sig ** 2)
        new_r = new_sig * np.random.normal(0, 1, 1)[0]
        return new_r, new_sig
    
    def get_price_at_period(self, period: int):
        try:
            self.eps[period]
        except IndexError:
            new_n = period - len(self.eps)  # number of new values we need to generate
            new_eps = np.random.normal(0, 1, new_n)
            old_eps = self.eps
            self.eps = np.concatenate((old_eps, new_eps))
        try:
            self.sigma[period]
            self.r[period]
        except IndexError:
            # should be able to combine these two try/except parts if 
            assert new_n == (period - len(self.sigma))
            old_sigma = self.sigma
            self.sigma = np.concatenate((old_sigma, np.ones(new_n)*self.sigma0))

            old_len = len(self.r)
            assert new_n == (period - len(self.r))
            old_r = self.r
            self.r = np.concatenate((old_r, np.zeros(new_n)))

            for i in range(old_len, period):
                self.sigma[i] = np.sqrt(self.a + self.b * self.r[i-1] ** 2 + self.c * self.sigma[i-1] ** 2)
                self.r[i] = self.sigma[i] * self.eps[i]
                self.r[i] += RETURN_BIAS
        
        self.cr = np.cumsum(self.r[:period]) + 1
        return self.cr[period-1] * self.init_value
    
    def gen_price_figure(self, period: int):
        self.get_price_at_period(period)  # make sure we've got the data up to that period
        fig = go.Figure(
            data=go.Scatter(
                x=[i for i in range(period)],
                y=[p for p in self.cr],
                mode='lines',
                line_shape='spline'
            )
        )
        return fig

    def simulate_price(self, n: int = 3600) -> float:
        eps = np.random.normal(0, 1, n)
        sigma = np.ones(n) * self.sigma0
        r = np.zeros(n)

        for i in range(1,n):
            #print(i)
            # a + b*(y^2)_(t-1) + c*(sig^2)_(t-1)
            sigma[i] = np.sqrt(self.a + self.b * r[i-1] ** 2 + self.c * sigma[i-1] ** 2)
            #print(f"sigma is {sigma[i]}")
            r[i] = sigma[i] * eps[i]  # this period returns
            r[i] += RETURN_BIAS
        cr = np.cumsum(r) + 1  # cumulative returns
        # print(f"total return is {cr[n-1]}")
        return cr[n-1]
    
    def monte_carlo(self, it: int = 100, n: int = 3600) -> dict:
        print(f"Simulating {it} outcomes of length {n} - {n*it} total periods")
        cr_list = []
        for i in range(it):
            if i%50 == 0 and DEBUG:
                print(i)
            cr_list.append(self.simulate_price(n=n))
        cr_list = [(x-1)*100 for x in cr_list]
        returns = {
            'max': round(max(cr_list), 2),
            'avg': round(sum(cr_list)/len(cr_list), 2),
            'min': round(min(cr_list), 2)
        }
        return returns
        # print(f"maximum return is {round(max(cr_list), 2)} %")
        # print(f"average return is {round(sum(cr_list)/len(cr_list), 2)} %")
        # print(f"minimum return is {round(min(cr_list), 2)} %")


if __name__ == '__main__':

    # rh = RobinhoodAPIHelper()
    # aapl_json = rh.get_info_by_symbol('AAPL')

    b, c = 0.25, 0.3
    print(f"b={b}; c={c}")
    my_asset = Asset(100, b=b, c=c)
    # print(my_asset.monte_carlo(it=100, n=86400))  # 14400 seconds is 4 hours, 86400 seconds is 1 day, 432000 seconds is 5 days
    print(my_asset.monte_carlo(it=100, n=86400))

    b, c = 0.15, 0.4
    print(f"b={b}; c={c}")
    another_asset = Asset(100, b=b, c=c)
    print(another_asset.monte_carlo(it=100, n=86400))

    b, c = 0.35, 0.3
    print(f"b={b}; c={c}")
    yet_another_asset = Asset(100, b=b, c=c)
    print(yet_another_asset.monte_carlo(it=100, n=86400))