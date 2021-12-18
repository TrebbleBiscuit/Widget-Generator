import numpy as np
import plotly.graph_objects as go
import pandas as pd

DEBUG = True
RETURN_RAND_CENTER = 0  # 0.005  # 0 for unbiased epsilon each period (std. dev of 1)

class GARCH:
    """
    Asset price simulated with a Generalized Auto-Regressive Conditional Heteroskedasticity (GARCH) model.
    """
    def __init__(self, init_value: int, b: float = 0.4, c: float = 0.4):
        self.init_value = init_value
        self.par_value = 110
        self.b = b  # ARCH coefficient
        self.c = c  # GARCH coefficient
        self.sigma0 = 0.0002
        self.a = 0.0000002  # 0.0000002
        self.eps = np.random.normal(RETURN_RAND_CENTER, 1, 5)  # init sims to length 5, later runs fn to sim to len 10
        self.r = np.zeros(5)
        self.cr = np.zeros(1)
        self.sigma = np.ones(5) * self.sigma0
        self._price_history = [self.init_value]
        self.total_bias_generated = 0
        self.get_price_at_period(50)  # sim to period 50
        self.get_price_at_period(100)  # sim to period 100
    
    def get_return_drift(self, c_ret):
        """ Input cumulative return, output drifted price """
        c_ret = 1 + c_ret
        price = c_ret * self.init_value
        bias_threshold = 0.05
        bias_ratio = 1/100  # ratio of the % from par_value to bias
        percent_diff = (price - self.par_value) / self.par_value
        if abs(percent_diff) > bias_threshold:
            # print(f"Biasing price {price} return: {(-percent_diff * bias_ratio)}")
            bias = (-percent_diff * bias_ratio)
            self.total_bias_generated += abs(bias)
            return bias
        else:
            return 0
    
    # def _bias_price(self, price):
    #     """ Slightly bias price towards equilibrium """
    #     bias_threshold = 0.05
    #     bias_ratio = 1/100  # ratio of the % from par_value to bias
    #     percent_diff = (price - self.par_value) / self.par_value
    #     if abs(percent_diff) > bias_threshold:
    #         # price pressure towards equlibrium
    #         return price * (1 - (percent_diff * bias_ratio))
    #     else:
    #         return price
    
    # def get_r_from_last(self, r: float, sig: float) -> tuple([float, float]):
    #     last_r = r
    #     last_sig = sig
    #     new_sig = np.sqrt(self.a + self.b * last_r ** 2 + self.c * last_sig ** 2)
    #     new_r = new_sig * np.random.normal(0, 1, 1)[0]
    #     return new_r, new_sig

    def _get_eps_at_period(self, period) -> float:
        """ Generate self.eps values up to period """
        try:
            return self.eps[period]
        except IndexError:
            new_n = 1 + period - len(self.eps)  # number of new values we need to generate
            new_eps = np.random.normal(RETURN_RAND_CENTER, 1, new_n)
            old_eps = self.eps
            self.eps = np.concatenate((old_eps, new_eps))
            return self.eps[period]

    def _get_r_at_period(self, period) -> float:
        """ Generate self.r and self.sigma values up to period """
        try:
            self.sigma[period]
            return self.r[period]
        except IndexError:
            self._get_eps_at_period(period)
            new_n = 1 + period - len(self.sigma)
            old_sigma = self.sigma
            self.sigma = np.concatenate((old_sigma, np.ones(new_n)*self.sigma0))

            old_len = len(self.r)
            old_r = self.r
            self.r = np.concatenate((old_r, np.zeros(new_n)))

            for i in range(old_len, period):
                self.sigma[i] = np.sqrt(self.a + self.b * self.r[i-1] ** 2 + self.c * self.sigma[i-1] ** 2)
                # self.eps[i] += return drift
                self.r[i] = self.sigma[i] * self.eps[i]
                # self.r[i] += self.get_return_drift(self.r)
            return self.r[period]

    def _get_cr_at_period(self, period) -> float:
        """ TODO: Make this only calculate values it hasn't already """
        try:
            return self.cr[period]
        except IndexError:
            self._get_r_at_period(period)
            self.cr = np.cumsum(self.r[:period+1]) + 1
            return self.cr[period]

    def get_price_at_period(self, period: int) -> float:
        """ TODO: Make this only calculate values it hasn't already """
        try:
            return self._price_history[period]
        except IndexError:
            self._get_r_at_period(period)
            for r in self.r:
                self._price_history.append(r * self._price_history[-1])
            # Generate values up to period
            # self._get_r_at_period(period)
            # self._get_cr_at_period(period)
            # self._price_history = self.cr * self.init_value
            return self._price_history[period]
        

    def gen_price_figure(self, period: int) -> go.Figure:
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
        eps = np.random.normal(RETURN_RAND_CENTER, 1, n)
        sigma = np.ones(n) * self.sigma0
        r = np.zeros(n)
        cr = np.zeros(n)
        for i in range(1,n):
            #print(i)
            # a + b*(y^2)_(t-1) + c*(sig^2)_(t-1)
            sigma[i] = np.sqrt(self.a + self.b * r[i-1] ** 2 + self.c * sigma[i-1] ** 2)
            #print(f"sigma is {sigma[i]}")
            r[i] = sigma[i] * eps[i]  # this period return
            cr[i] = cr[i-1] + r[i]
            bias = self.get_return_drift(cr[i])
            if i % 400 == 0 and bias > 0:
                print(f"info: bias is {round(bias, 4)}; cr[i] is {round(cr[i], 4)}, r[i] was {round(r[i], 4)}")
            r[i] += bias
            cr[i] += bias
        # cr = np.cumsum(r) + 1  # cumulative returns
        return cr[n-1]
    
    def monte_carlo(self, it: int = 100, n: int = 3600) -> dict:
        print(f"Simulating {it} outcomes of length {n} - {n*it} total periods")
        cr_list = []
        for i in range(it):
            if i%25 == 0 and DEBUG:
                print(i)
            cr_list.append(self.simulate_price(n=n))
        cr_list = [(x)*100 for x in cr_list]
        returns = {
            'iterations': it,
            'length': n,
            'max': round(max(cr_list), 2),
            'avg': round(sum(cr_list)/len(cr_list), 2),
            'min': round(min(cr_list), 2),
            'bias': self.total_bias_generated,
            'quint': pd.qcut(cr_list, 4, retbins=True)[1]
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
    my_asset = GARCH(100, b=b, c=c)
    # print(my_asset.monte_carlo(it=100, n=86400))  # 14400 seconds is 4 hours, 86400 seconds is 1 day, 432000 seconds is 5 days
    # 14400 minutes is 10 days tho, 13680 in 2 months
    # 450 trading minutes per day, 2250 per week, 9000 per month, 36000 per quarter
    # for period=5min; 90 for 1 trading day, 450/wk, 1800/month, 21600/yr
    ma_mc = my_asset.monte_carlo(it=100, n=9000)
    print(ma_mc)

    b, c = 0.25, 0.2
    print(f"b={b}; c={c}")
    another_asset = GARCH(100, b=b, c=c)
    print(another_asset.monte_carlo(it=100, n=9000))

    b, c = 0.15, 0.2
    print(f"b={b}; c={c}")
    yet_another_asset = GARCH(100, b=b, c=c)
    print(yet_another_asset.monte_carlo(it=100, n=9000))