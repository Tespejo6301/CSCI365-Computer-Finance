'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Trisha Espejo

@Date          : June 2021


'''

import datetime
from scipy.stats import norm
from math import log, exp, sqrt

from stock import Stock
from option import *

class BlackScholesModel(object):
    '''
    OptionPricer
    '''

    def __init__(self, pricing_date, risk_free_rate):
        self.pricing_date = pricing_date
        self.risk_free_rate = risk_free_rate

    def calc_parity_price(self, option, option_price):
        '''
        return the put price from Put-Call Parity if input option is a call
        else return the call price from Put-Call Parity if input option is a put
        '''
        result = None
        # TODO: implement details here
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("Price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            if option.option_type == Option.Type.CALL:
                result = option_price + (option.strike * exp(-self.risk_free_rate * option.time_to_expiry)) - option.underlying.spot_price
            elif option.option_type == Option.Type.PUT:
                result = option_price + option.underlying.spot_price - (option.strike * exp(-self.risk_free_rate * option.time_to_expiry))
        else:
            raise Exception("Unsupported option type")
        # end TODO
        return(result)

    def calc_model_price(self, option):
        '''
        Calculate the price of the option using Black-Scholes model
        '''
        px = None
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
            
            #TODO:
            d1 = (log(S0/K) + ((r - q) + sigma ** 2 / 2) * T ) / (sigma * sqrt (T))
            d2 = d1 - (sigma * sqrt(T))
            if option.option_type == Option.Type.CALL:
                N1 = norm.cdf(d1)
                N2 = norm.cdf(d2)
                px = (S0 * exp( -q * T) *  N1) - (K * exp (-r * T) * N2)
            elif option.option_type == Option.Type.PUT:
                N1 = norm.cdf(-d1)
                N2 = norm.cdf(-d2)
                px = (K * exp(-r * T) * N2) - (S0 * exp( -q * T) * N1) 
            #end TODO
        else:
            raise Exception("Unsupported option type")        
        return(px)

    def calc_delta(self, option):
        result = None
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
           
            d1 = (log(S0/K) + ((r - q) + sigma ** 2 / 2) * T ) / (sigma * sqrt (T))
            N = norm.cdf(d1)
            if option.option_type == Option.Type.CALL:
                result = exp ( - q * T) * N
            elif option.option_type == Option.Type.PUT:
                result = exp ( - q * T) * (N - 1)

            # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_gamma(self, option):
        result = None
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
            
            d1 = (log(S0/K) + ((r - q) + sigma ** 2 / 2) * T ) / (sigma * sqrt (T))
            result = (norm.pdf(d1)* exp( - q * T)) / (S0 * sigma * sqrt (T))

            # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_theta(self, option):
        result = None
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
            d1 = (log(S0/K) + ((r - q) + sigma ** 2 / 2) * T ) / (sigma * sqrt (T))
            d2 = d1 - (sigma * sqrt(T))
            if option.option_type == Option.Type.CALL:
                N1 = norm.cdf(d1)
                N2 = norm.cdf(d2)
                N1_prime = norm.pdf(d1)
                result = (-S0 * N1_prime * sigma * exp ( - q * T))/ (2 * sqrt(T)) + ((q * S0 * N1 * exp( -q * T)) - (r * K * exp( -r * T ) * N2))
            elif option.option_type == Option.Type.PUT:  
                N1 = norm.cdf(-d1)
                N2 = norm.cdf(-d2)
                N1_prime = norm.pdf(d1)
                result = (-S0 * N1_prime * sigma * exp ( - q * T))/ (2 * sqrt(T)) - ((q * S0 * N1 * exp( -q * T)) + (r * K * exp( -r * T ) * N2))
            # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_vega(self, option):
        result = None
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
            d1 = (log(S0/K) + ((r - q) + sigma ** 2 / 2) * T ) / (sigma * sqrt (T))
            N = norm.pdf(d1)
            result = S0 * sqrt(T) * N * exp( -q * T)


            # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_rho(self, option):
        result = None
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
            d1 = (log(S0/K) + ((r - q) + sigma ** 2 / 2) * T ) / (sigma * sqrt (T))
            d2 = d1 - sigma * sqrt(T)
            if option.option_type == Option.Type.CALL:
                N2 = norm.cdf(d2)
                result = K * T * exp( -r * T) * N2
            elif option.option_type == Option.Type.PUT:
                N2 = norm.cdf(-d2)
                result = -K * T * exp( -r * T) * N2
            # end TODO
        else:
            raise Exception("Unsupported option type")
            
        return result


def _test():

    symbol = 'AAPL'
    pricing_date = datetime.date(2021, 6, 1)

    risk_free_rate = 0.04
    model = BlackScholesModel(pricing_date, risk_free_rate)

    # .... use this as your unit test
    # calculate the B/S model price for a 3-month ATM call
    T = 3/12
    num_period = 2

    dt = T / num_period
    S0 = 130
    K = 130

    sigma = 0.3
    
    stock = Stock(symbol, S0, sigma)
    
    option = EuropeanCallOption(stock, T, K)
    
    model_price = model.calc_model_price(option)
    parity = model.calc_parity_price(option, model_price)
    delta = model.calc_delta(option)
    gamma = model.calc_gamma(option)
    theta = model.calc_theta(option)
    vega = model.calc_vega(option)
    rho = model.calc_rho(option)
    
    print("Euro call: ", model_price)
    print("parity", parity)
    print ("delta:", delta)
    print("gamma:", gamma)
    print("theta:", theta)
    print("vega:", vega)
    print("rho:", rho)

if __name__ == "__main__":
    _test()
    
