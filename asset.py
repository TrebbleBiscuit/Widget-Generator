import numpy as np
import plotly.graph_objects as go
import pandas as pd
import random
from loguru import logger
from tqdm import tqdm

DEBUG = True
RETURN_RAND_CENTER = 0  # 0.005  # 0 for unbiased epsilon each period (std. dev of 1)

class GARCH:
    """
    Asset price simulated with a Generalized Auto-Regressive Conditional Heteroskedasticity (GARCH) model.
    """
    def __init__(self, init_value: int, b: float = 0.3, c: float = 0.3):
        self.init_value = init_value
        self.par_value = init_value
        self.b = b  # ARCH coefficient
        self.c = c  # GARCH coefficient
        self.sigma0 = 0.0002
        self.a = 0.0000002  # 0.0000002
        self.eps = np.random.normal(RETURN_RAND_CENTER, 1, 2)  # init sims to length 2, later runs fn to sim to len 10
        self.r = np.zeros(2)
        self.cr = np.zeros(2)
        self.sigma = np.ones(2) * self.sigma0
        self._price_history = np.ones(2) * self.init_value
        self.total_bias_generated = 0
        self.get_price_at_period(50)  # sim to period 50
        self.get_price_at_period(100)  # sim to period 100
    
    def _get_return_drift(self, price):
        """ Input cumulative return, output drifted price """
        # c_ret = 1 + c_ret
        # price = c_ret * self.init_value
        bias_threshold = 0.05
        bias_ratio = 1/(random.randint(3000, 4000))  # ratio of the % from par_value to bias
        percent_diff = (price - self.par_value) / self.par_value
        if abs(percent_diff) > bias_threshold:
            # print(f"Biasing price {price} return: {(-percent_diff * bias_ratio)}")
            bias = (-percent_diff * bias_ratio)
            if random.randint(0, 1):
                bias = bias * np.random.normal(2)  # add some fun :)
            if abs(percent_diff) > 3 * bias_threshold and random.randint(0, 499) == 0:
                bias = bias * 60
            if abs(percent_diff) > 6 * bias_threshold and random.randint(0, 2499) == 0:
                bias = bias * 300  # wheeeee
                # bias = (-percent_diff * (0.1 + (0.1 * random.random())))
                print(f"bias greatly increased to {bias}")
            if abs(percent_diff) > 8 * bias_threshold and random.randint(0, 99) == 0:
                bias = bias * 20  # wheeeee
            self.total_bias_generated += abs(bias)
            return bias
        else:
            return 0

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

    def par_value_set_trigger(self, period):
        """ Override this function """
        print("Override this function")

    def _sim_to_period(self, period) -> float:
        """ Generate self.r and self.sigma values up to period """
        try:
            self.sigma[period]
            self.r[period]
            self.cr[period]
        except IndexError:
            self._get_eps_at_period(period)
            new_n = 1 + period - len(self.sigma)
            old_sigma = self.sigma
            self.sigma = np.concatenate((old_sigma, np.ones(new_n)*self.sigma0))

            old_len = len(self.r)
            old_r = self.r
            old_cr = self.cr
            old_price_history = self._price_history
            self.r = np.concatenate((old_r, np.zeros(new_n)))
            self.cr = np.concatenate((old_cr, np.zeros(new_n)))
            self._price_history = np.concatenate((old_price_history, np.ones(new_n)))

            for i in range(old_len-1, period):
                if i % 1000 == 0:
                    pv = self.par_value_set_trigger(period)
                    if pv:
                        self.par_value = pv
                        # logger.warning(f"DEBUG: Setting par value to {self.par_value} at pd {i}")
                    # self.par_value = self.init_value + (i/1000)
                self.sigma[i] = np.sqrt(self.a + self.b * self.r[i-1] ** 2 + self.c * self.sigma[i-1] ** 2)
                # self.eps[i] += return drift
                if i % 2250 == 0:  # each week
                    self.sigma[i] = self.sigma[i] * 8
                self.r[i] = self.sigma[i] * self.eps[i]
                self.cr[i] = self.cr[i-1] + self.r[i]
                last_price = self._price_history[i-1]
                bias = self._get_return_drift(last_price)
                self.r[i] += bias
                self.cr[i] += bias
                self._price_history[i] = last_price * (1 + self.r[i])
                # self.r[i] += self._get_return_drift(self.r)
            return self.r[period]

    def get_price_at_period(self, period: int) -> float:
        try:
            return self._price_history[period]
        except IndexError:
            self._sim_to_period(period)
            return self._price_history[period]
        

    def gen_price_figure(self, period: int) -> go.Figure:
        self.get_price_at_period(period)  # make sure we've got the data up to that period
        fig = go.Figure(
            data=go.Scatter(
                x=[i for i in range(period)],
                y=[p for p in self._price_history],
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
            bias = self._get_return_drift(self.init_value * cr[i])
            if i % 1000 == 0 and bias > 0.01:
                logger.warning(f"warn: bias is {round(bias, 4)}; cr[i] is {round(cr[i], 4)}, r[i] was {round(r[i], 4)}")
            r[i] += bias
            cr[i] += bias
        # cr = np.cumsum(r) + 1  # cumulative returns
        return cr[n-1]
    
    def monte_carlo(self, it: int = 100, n: int = 3600) -> dict:
        logger.info(f"Simulating {it} outcomes of length {n} - {n*it} total periods...")
        cr_list = []
        for i in tqdm(range(it)):  # tqdm() to make a loading bar
            # if i%25 == 0 and DEBUG:
            #     logger.info(f"{i}/{it} done")
            cr_list.append(self.simulate_price(n=n))
        logger.success("Done!")
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

    b, c = 0.35, 0.2
    print(f"b={b}; c={c}")
    my_asset = GARCH(100, b=b, c=c)
    # print(my_asset.monte_carlo(it=100, n=86400))  # 14400 seconds is 4 hours, 86400 seconds is 1 day, 432000 seconds is 5 days
    # 14400 minutes is 10 days tho, 13680 in 2 months
    # 450 trading minutes per day, 2250 per week, 9000 per month, 36000 per quarter
    # for period=5min; 90 for 1 trading day, 450/wk, 1800/month, 21600/yr
    # ma_mc = my_asset.monte_carlo(it=100, n=9000)
    # print(ma_mc)

    # b, c = 0.25, 0.2
    # print(f"b={b}; c={c}")
    # another_asset = GARCH(100, b=b, c=c)
    # print(another_asset.monte_carlo(it=100, n=9000))

    # b, c = 0.15, 0.2
    # print(f"b={b}; c={c}")
    # yet_another_asset = GARCH(100, b=b, c=c)
    # print(yet_another_asset.monte_carlo(it=100, n=9000))