import yfinance as yf
import pickle
import pandas


def get_data(stock):  # pull the year to date data for stock from yfinance and save only the closing price to a pkl file
    stock.upper()
    ticker = yf.Ticker(stock)
    data = ticker.history(period='1y')
    data = data['Close']
    data.to_pickle("data/" + stock + ".pkl")


def get_latest_close(stock):  # given a pandas dataframe of a stock's closing price values print the most up to date one
    print(stock[stock.size - 1])


def get_stock_history(stock): # returns the dataframe of the stock's historical closing prices
    return pandas.read_pickle("data/" + stock.rstrip() + ".pkl")


if __name__ == "__main__":  # main function pulls the most up to date data for all s&p 500 stocks
    file = open("stockLists/sp500.txt")  # todo: add nasdaq, dow, etc
    for line in file.readlines():
        try:
            get_data(line.rstrip())
        except OSError:
            print(line + " is invalid")
    file.close()
