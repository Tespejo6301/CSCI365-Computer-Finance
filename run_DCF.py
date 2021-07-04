'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : Trisha Espejo

'''

import pandas as pd
import datetime

from stock import Stock
from discount_cf_model import DiscountedCashFlowModel

def run():
    input_fname = "StockUniverse.csv"
    output_fname = "StockUniverseWithDCF.csv"

    as_of_date = datetime.date(2021, 6, 15)
    df = pd.read_csv(input_fname)
    
    # TODO
    results = {'Symbol': [], 'EPS Next 5Y': [], 'DCF': []}
    count = 0
    for row in df.iterrows():
        ##print(row[1]['Symbol'])
        symbol =row[1]['Symbol']
        stock = Stock(symbol, 'annual')
        model = DiscountedCashFlowModel(stock, as_of_date)
        results['Symbol'].append(symbol)
        EPS = row[1]['EPS Next 5Y']
        count = count + 1
        results['EPS Next 5Y'].append(EPS)
        
        try:
            x = float(EPS.strip('%'))
            x = x / 100
            short_term_growth_rate = x
            medium_term_growth_rate = short_term_growth_rate/2
            long_term_growth_rate = 0.04
            model.set_FCC_growth_rate(short_term_growth_rate, medium_term_growth_rate, long_term_growth_rate)
            
            fair_value = model.calc_fair_value() 
            
        except AttributeError as e:
            
            fair_value = None
        print("number of calculation completed: ", count )       
        results['DCF'].append(fair_value)

    df1 = pd.DataFrame(results)
    print("calculation completed") 
    print(df1)  
    df1.to_csv(output_fname, index = False)
    # ....
    
    # end TODO

    
if __name__ == "__main__":
    run()
