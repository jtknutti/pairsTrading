import getData
import pandas
import alpaca_trade_api as tradeapi
import os

def check_ratios(pairs):
    for i in range(len(pairs)):
        stock_a = getData.get_latest_close((pairs[i])[0])
        stock_b = getData.get_latest_close((pairs[i])[1])
        ratio = (pairs[i])[2]
        st_dev = (pairs[i])[3]
        if stock_a > stock_b:
            if stock_a / stock_b > (ratio + (2 * st_dev)):
                print("buying " + pairs[i][1] + " and selling " + pairs[i][0])
                pass  # buy stock b, sell stock a
            elif stock_a / stock_b < (ratio - (2 * st_dev)):
                print("buying " + pairs[i][0] + " and selling " + pairs[i][1])
                pass  # buy stock a, sell stock b
        else:
            if stock_b / stock_a > (ratio + (2 * st_dev)):
                print("buying " + pairs[i][0] + " and selling " + pairs[i][1])
                pass  # buy stock a, sell stock b
            elif stock_b / stock_a < (ratio - (2 * st_dev)):
                print("buying " + pairs[i][1] + " and selling " + pairs[i][0])
                pass  # buy stock b, sell stock a


if __name__ == "__main__":
    api = tradeapi.REST()
    account = api.get_account()
    check_ratios(pandas.read_pickle("pairs/pairs.pkl"))
