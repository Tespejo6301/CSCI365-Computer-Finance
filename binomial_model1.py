'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Trisha Espejo

@Date          : June 2021


'''

import datetime
from math import log, exp, sqrt

from stock import Stock
from option import *

class BinomialModel(object):
    '''
    OptionPricer
    '''

    def __init__(self, pricing_date, risk_free_rate):
        self.pricing_date = pricing_date
        self.risk_free_rate = risk_free_rate

    def _binomial_european_call(self, S_0, K, T, r, sigma, q, N):
        '''
        Calculate the price of an European call using Binomial Tree
        S_0 - stock price today
        K - strike price of the option
        T - time to expiry in unit of years
        r - risk-free interest rate
        sigma - the volatility of the stock
        q - the continous dividend yield of the stock
        N - number of periods in the tree
        '''
        dt = T/N
        u =  exp(sigma * sqrt(dt))
        d = 1/u
        prob = (exp((r-q) * dt) - d)/(u - d)
        
        # call price dictionary with (k, m) as the key
        C = {}
        # TODO: implement details here
        for m in range(0, N + 1):
            C[(N, m)] = max(S_0 * (u ** (m)) * (d ** (N-m)) - K, 0)
        for k in range(N-1, -1, -1):
            for m in range(0,k+1):
                C[(k, m)] = math.exp(-r * dt) * (prob * C[(k+1, m+1)] + (1-prob) * C[(k+1, m)])
        # end TODO
        return C[(0,0)]

    def _binomial_european_put(self, S_0, K, T, r, sigma, q, N):
        '''
        Calculate the price of an European put using Binomial Tree
        S_0 - stock price today
        K - strike price of the option
        T - time to expiry in unit of years
        r - risk-free interest rate
        sigma - the volatility of the stock
        q - the continous dividend yield of the stock
        N - number of steps in the model
        '''
        dt = T/N
        u =  exp(sigma * sqrt(dt))
        d = 1/u
        prob = (exp((r - q) * dt) - d)/(u - d)
        # put price dictionary with (k, m) as the key
        P = {}

        # TODO: implement details here
        for m in range(0, N + 1):
            P[(N, m)] = max( K - (S_0 * (u ** (m)) * (d ** (N-m))), 0)
        for k in range(N-1, -1, -1):
            for m in range(0,k+1):
                P[(k, m)] = math.exp(-r * dt) * (prob * C[(k + 1, m + 1)] + (1 - prob) * C[(k + 1, m)])
        # end TODO
        return P[(0,0)]        

    def _binomial_american_call(self, S_0, K, T, r, sigma, q, N):
        '''
        Calculate the price of an American call using Binomial Tree
        S_0 - stock price today
        K - strike price of the option
        T - time until expiry of the option
        r - risk-free interest rate
        sigma - the volatility of the stock
        q - the continous dividend yield of the stock
        N - number of steps in the model
        '''
        dt = T/N
        u =  exp(sigma * sqrt(dt))
        d = 1/u
        prob = (exp( (r-q) * dt) - d)/(u - d)
        C = {}
        for m in range(0, N+1):
            S_T = S_0 * (u ** (2*m - N))
            C[(N, m)] = max(S_T - K, 0)
        for k in range(N-1, -1, -1):
            for m in range(0,k+1):
                S_t = S_0 * (u ** (2*m - k))
                # TODO: fill in the blank here
                c_t = exp(-r * dt) * (prob * C[(k+1, m+1)] + (1-prob) * C[(k+1, m)])
                C[(k, m)] = max(S_t - K, c_t)
                # end TODO
        return C[(0,0)]        

    def _binomial_american_put(self, S_0, K, T, r, sigma, q, N):
        '''
        Calculate the price of an American put using Binomial Tree
        S_0 - stock price today
        K - strike price of the option
        T - time to expiry in unit of years
        r - risk-free interest rate
        sigma - the volatility of the stock
        N - number of steps in the model
        '''
        dt = T/N
        u =  exp(sigma * sqrt(dt))
        d = 1/u
        prob = (exp((r-q) * dt) - d)/(u - d)
        P = {}

        # TODO: implement details here
        for m in range(0, N+1):
            S_T = S_0 * (u ** (2*m - N))
            P[(N, m)] = max(K - S_T  , 0)
        for k in range(N-1, -1, -1): 
            for m in range(0,k+1):  
                S_t = S_0 * (u ** (2*m - k))
                p_t = exp(-r * dt) * (prob * P[(k+1, m+1)] + (1-prob) * P[(k+1, m)])
                P[(k, m)] = max(K - S_t, _t)
        # end TODO
        return P[(0,0)]        


    def calc_model_price(self, option, num_of_period):
        '''
        Calculate the price of the option using num_of_period Binomial Model 
        '''
        if option.option_type == Option.Type.CALL and option.option_style == Option.Style.EUROPEAN:
            px = self._binomial_european_call(option.underlying.spot_price, option.strike, option.time_to_expiry,
                                              self.risk_free_rate, option.underlying.sigma, option.underlying.dividend_yield,
                                              num_of_period)
            
        elif option.option_type == Option.Type.PUT and option.option_style == Option.Style.EUROPEAN:
            px = self._binomial_european_put(option.underlying.spot_price, option.strike, option.time_to_expiry,
                                             self.risk_free_rate, option.underlying.sigma, option.underlying.dividend_yield,
                                             num_of_period)
            
        elif option.option_type == Option.Type.CALL and option.option_style == Option.Style.AMERICAN:
            px = self._binomial_american_call(option.underlying.spot_price, option.strike, option.time_to_expiry,
                                              self.risk_free_rate, option.underlying.sigma, option.underlying.dividend_yield,
                                              num_of_period)
            
        elif option.option_type == Option.Type.PUT and option.option_style == Option.Style.AMERICAN:
            px = self._binomial_american_put(option.underlying.spot_price, option.strike, option.time_to_expiry,
                                             self.risk_free_rate, option.underlying.sigma, option.underlying.dividend_yield,
                                             num_of_period)

        return(px)


    def calc_parity_price(self, option, option_price):
        '''
        return the put price from Put-Call Parity if input option is a call
        else return the call price from Put-Call Parity if input option is a put
        '''
        result = None
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("Price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            T = option.time_to_expiry
            S = option.underlying.spot_price
            K = option.strike
            r = self.risk_free_rate
            if option.option_type == Option.Type.CALL:
                result = option_price + (K * math.exp( -r * T)) - S
            elif option.option_type == Option.Type.PUT:
                result = option_price + S - (K * math.exp( -r * T))
        else:
            raise Exception("Unsupported option type")
            
        return(result)



def _test():

    symbol = 'AAPL'
    pricing_date = datetime.date(2021, 6, 1)

    risk_free_rate = 0.08
    model = BinomialModel(pricing_date, risk_free_rate)

    # .... use this as your unit test

    # calculate a 3-month ATM call using a 2-period Binomial model


    S0 = 100
    K = 100
    u = 1.1
    num_period = 2
    T = 6/12
    
    '''
    num_period = 1
    S_0 = 20
    u =1.1
    d = 0.90
    K = 21
    T = 0.25
    r = 0.04
    '''
    dt = T / num_period
     # calculate sigma from u if u is given
   
    sigma = log(u) / sqrt(dt)
    stock = Stock(symbol, S0, sigma)
    call = EuropeanCallOption(stock, T, K)
    
    model_price = model.calc_model_price(call, num_period)
    print(model_price)
    #put = EuropeanPutOption(stock, T, K)

    parity = model.calc_parity_price(call, num_period)
    print("parity for given call: ",parity)
   # model_price = model.calc_model_price(put, num_period)
    #print("european put price:", model_price)
    #parity = model.calc_parity_price(put, num_period)
   # print("parity price for given put: ", parity)

if __name__ == "__main__":
    _test()
