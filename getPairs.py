import getData
from numpy import corrcoef
import pandas
import warnings
from statsmodels.tsa.stattools import coint


def check_correlation(stock_a, stock_b):  # given two stocks return a correlation coefficient between their history
    if len(stock_a) > len(stock_b):
        stock_a = stock_a[(len(stock_a) - len(stock_b)):]
    elif len(stock_b) > len(stock_a):
        stock_b = stock_b[(len(stock_b) - len(stock_a)):]
    matrix = corrcoef(stock_a, stock_b)
    if matrix[0][1] == matrix[1][0]:
        return matrix[0][1]  # corrcoef returns a matrix, [0][1] and [1][0] contain the same value
    else:
        return -1


def check_cointegration(stock_a, stock_b):
    if len(stock_a) > len(stock_b):
        stock_a = stock_a[(len(stock_a) - len(stock_b)):]
    elif len(stock_b) > len(stock_a):
        stock_b = stock_b[(len(stock_b) - len(stock_a)):]
    return coint(stock_a, stock_b)[1]


def get_pairs():
    pairs = []
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    stocks = open("stockLists/sp500.txt").readlines()
    for i in range(len(stocks)):
        for j in range(i + 1, len(stocks)):
            stock_i = getData.get_stock_history(stocks[i].rstrip())
            stock_j = getData.get_stock_history(stocks[j].rstrip())
            if check_correlation(stock_i, stock_j) > .8:
                if check_cointegration(stock_i, stock_j) < .02:
                    pairs.append([stocks[i].rstrip(), stocks[j].rstrip()])
    return pairs


def read_pkl(file):
    print(pandas.read_pickle(file))


if __name__ == "__main__":
    data = pandas.Series(get_pairs())
    data.to_pickle("pairs/pairs.pkl")
