'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Trisha Espejo 

@Date          : June 2021


'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

import datetime 
from scipy.stats import norm

from math import log, exp, sqrt

from utils import MyYahooFinancials 



class Stock(object):
    '''
    Stock class for getting financial statements as well as pricing data
    '''
    ## need to fix
    def __init__(self, symbol, spot_price = None, sigma = None, dividend_yield = 0, freq = 'annual'):
        self.symbol = symbol
        self.spot_price = spot_price
        self.sigma = sigma
        self.dividend_yield = dividend_yield
        self.yfinancial = MyYahooFinancials(symbol, freq)
        self.ohlcv_df = None
    





    def get_daily_hist_price(self, start_date, end_date):
        '''
        Get historical OHLCV pricing dataframe
        '''
        time_interval= 'daily'
        self.ohlcv_df = self.yfinancial.get_historical_price_data(start_date, end_date, time_interval)
        return (self.ohlcv_df)
  
    def calc_returns(self):
        '''
        '''
        self.ohlcv_df['prev_close'] = self.ohlcv_df['close'].shift(1)
        self.ohlcv_df['returns'] = (self.ohlcv_df['close'] - self.ohlcv_df['prev_close'])/ \
                                        self.ohlcv_df['prev_close']


    # financial statements related methods
    ##here
    def get_total_debt(self):
        '''
        compute total_debt as long term debt + current debt 
        current debt = total current liabilities - accounts payables - other current liabilities (ignoring current deferred liabilities)
        '''
        try:
            long_term_debt = self.yfinancial.get_long_term_debt()
            total_curr_liab = self.yfinancial.get_total_current_liabilities()
            account_payable = self.yfinancial.get_account_payable()
            other_liability = self.yfinancial.get_other_current_liabilities()
            curr_term_debt = total_curr_liab - account_payable - other_liability
            result = long_term_debt + curr_term_debt
        except KeyError as e:
            result = None   
        return(result)

    def get_free_cashflow(self):
        '''
        get free cash flow as operating cashflow + capital expenditures (which will be negative)
        '''
        try:
            result = self.yfinancial.get_operating_cashflow() + self.yfinancial.get_capital_expenditures()
        except KeyError as e:
            result = None     
        return(result)

    def get_cash_and_cash_equivalent(self):
        '''
        Return cash plus short term investment 
        '''
        try:
            result = self.yfinancial.get_cash() + self.yfinancial.get_short_term_investments()
        except KeyError as e:
            result = None         
        return(result)

    def get_num_shares_outstanding(self):
        '''
        get current number of shares outstanding from Yahoo financial library
        '''
        
        result = self.yfinancial.get_num_shares_outstanding() 
        return(result)

    def get_beta(self):
        '''
        get beta from Yahoo financial
        '''
        result = self.yfinancial.get_beta()
        return(result)

##need to do 
    def lookup_wacc_by_beta(self, beta):
        '''
        lookup wacc by using the table in Slide 15 of the DiscountedCashFlowModel lecture powerpoint
        '''
        result = None
        result = None
        if (beta < 0.80):
            result = 5
        elif (beta <= 0.8 and beta > 1.0):
            result = 6
        elif (beta <= 1.0 and beta < 1.1):
            result = 6.5
        elif (beta <= 1.1 and beta < 1.2):
            result = 7
        elif (beta <= 1.2 and beta < 1.3):
            result = 7.5
        elif (beta <= 1.3 and beta < 1.5):
            result = 8
        elif (beta <= 1.5 and beta < 1.6):
            result = 8.5
        elif (beta > 1.6):
            result = 9.0   
        return(result)
        
     
def _test():
    symbol = 'AAPL'
    stock = Stock(symbol, 'annual')
    current_time = datetime.datetime.now()
    dd = current_time.day
    mm = current_time.month
    yyyy = current_time.year
    start_date = datetime.date(yyyy, mm , dd - 1).strftime("%Y-%m-%d")
    end_date = datetime.date(yyyy, mm , dd).strftime("%Y-%m-%d")
    print (stock.symbol)
    
    stock.get_daily_hist_price(start_date, end_date)
    print("daily history price: ", stock.ohlcv_df )
    print("Total Debt: ", stock.get_total_debt())
    print("Free Cash Flow: ", stock.get_free_cashflow())
    print("Cash and Cash Equivalence: ", stock.get_cash_and_cash_equivalent())
    print("Total Number of Outstanding Shares : ", stock.get_num_shares_outstanding())
    print("Beta : ", stock.get_beta())






if __name__ == "__main__":
    _test()

