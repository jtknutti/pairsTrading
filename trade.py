import getData
import pandas
import alpaca_trade_api as tradeapi


def check_ratios(pairs):
    api = tradeapi.REST()
    for i in range(len(pairs)):
        pair = pairs[i]
        stock_a = getData.get_latest_close(pair[0])
        stock_b = getData.get_latest_close(pair[1])
        ratio = pair[2]
        st_dev = pair[3]
        account = api.get_account()
        # TODO: add the actual buying and selling calls from the alpaca api

        if stock_a > stock_b:
            if stock_a / stock_b > (ratio + (2 * st_dev)):

                print("buying " + pair[1] + " and selling " + pair[0])
                pass  # buy stock b, sell stock a
            elif stock_a / stock_b < (ratio - (2 * st_dev)):
                print("buying " + pair[0] + " and selling " + pair[1])
                pass  # buy stock a, sell stock b
        else:
            if stock_b / stock_a > (ratio + (2 * st_dev)):
                print("buying " + pair[0] + " and selling " + pair[1])
                pass  # buy stock a, sell stock b
            elif stock_b / stock_a < (ratio - (2 * st_dev)):
                print("buying " + pair[1] + " and selling " + pair[0])
                pass  # buy stock b, sell stock a


def backtest(stock_a, stock_b):
    start_cash = cash = 10000
    pairs = pandas.read_pickle("pairs/pairs.pkl")
    temp_pair = None
    for pair in pairs:
        if pair[0] == stock_a and pair[1] == stock_b:
            temp_pair = pair
            break
    if temp_pair is not None:
        ratio = temp_pair[2]
        st_dev = temp_pair[3]
        stock_a = pandas.read_pickle("data/" + stock_a + ".pkl")
        stock_b = pandas.read_pickle("data/" + stock_b + ".pkl")
        if len(stock_a) > len(stock_b):
            stock_a = stock_a[(len(stock_a) - len(stock_b)):]
        elif len(stock_b) > len(stock_a):
            stock_b = stock_b[(len(stock_b) - len(stock_a)):]
        owned = {temp_pair[0]: 0, temp_pair[1]: 0}
        test_buy(temp_pair[0], stock_a[0], cash, owned, 10)
        test_buy(temp_pair[1], stock_b[0], cash, owned, 10)
        for day in range(len(stock_a)):
            price_a = stock_a[day]
            price_b = stock_b[day]
            if price_a > price_b:
                if price_a / price_b > (ratio + (2 * st_dev)):
                    cash = test_sell(temp_pair[0], price_a, cash, owned, 5)
                    cash = test_buy(temp_pair[1], price_b, cash, owned, 5)
                elif stock_a[day] / stock_b[day] < (ratio - (2 * st_dev)):
                    cash = test_sell(temp_pair[1], stock_b[day], cash, owned, 5)
                    cash = test_buy(temp_pair[0], stock_a[day], cash, owned, 5)
                else:
                    if owned[temp_pair[0]] < 10:
                        cash = test_buy(temp_pair[0], price_a, cash, owned, 10 - owned[temp_pair[0]])
                    else:
                        cash = test_sell(temp_pair[0], price_a, cash, owned, owned[temp_pair[0]] - 10)
                    if owned[temp_pair[1]] < 10:
                        cash = test_buy(temp_pair[1], price_b, cash, owned, 10 - owned[temp_pair[1]])
                    else:
                        cash = test_sell(temp_pair[1], price_b, cash, owned, owned[temp_pair[1]] - 10)
            else:
                if stock_b[day] / stock_a[day] > (ratio + (2 * st_dev)):
                    cash = test_sell(temp_pair[1], stock_b[day], cash, owned, 5)
                    cash = test_buy(temp_pair[0], stock_a[day], cash, owned, 5)
                elif stock_b[day] / stock_a[day] < (ratio - (2 * st_dev)):
                    cash = test_sell(temp_pair[0], stock_a[day], cash, owned, 5)
                    cash = test_buy(temp_pair[1], stock_b[day], cash, owned, 5)
                else:
                    if owned[temp_pair[0]] < 10:
                        cash = test_buy(temp_pair[0], price_a, cash, owned, 10 - owned[temp_pair[0]])
                    else:
                        cash = test_sell(temp_pair[0], price_a, cash, owned, owned[temp_pair[0]] - 10)
                    if owned[temp_pair[1]] < 10:
                        cash = test_buy(temp_pair[1], price_b, cash, owned, 10 - owned[temp_pair[1]])
                    else:
                        cash = test_sell(temp_pair[1], price_b, cash, owned, owned[temp_pair[1]] - 10)
        cash = test_sell(temp_pair[0], stock_a[len(stock_a) - 1], cash, owned, owned[temp_pair[0]])
        cash = test_sell(temp_pair[1], stock_b[len(stock_b) - 1], cash, owned, owned[temp_pair[1]])
    else:
        print("Pair not found")
    percent_change = (cash - start_cash) / start_cash
    print("Starting cash: " + str(start_cash))
    print("Ending cash: " + str(cash))
    print("Percent change: " + str(percent_change))
    return percent_change


def test_buy(stock, price, cash, owned, amt):
    total = 0
    for i in range(amt):
        if price > cash:
            break
        cash = cash - price
        owned[stock] = owned[stock] + 1
        total = i + 1
    if total > 0:
        print("Buying " + str(total) + " shares of " + stock + " at " + str(price))
    return cash


def test_sell(stock, price, cash, owned, amt):
    total = 0
    for i in range(amt):
        if owned[stock] <= 0:
            break
        cash = cash + price
        owned[stock] = owned[stock] - 1
        total = i + 1
    if total > 0:
        print("Selling " + str(total) + " shares of " + stock + " at " + str(price))
    return cash


def calculate_value(owned, stock, price):
    return owned[stock] * price


def do_backtest():
    pairs = pandas.read_pickle("pairs/pairs.pkl")
    percents = []
    for pair in pairs:
        percents.append([backtest(pair[0], pair[1]), pair])
        print('\n')
    percents.sort()
    avg = 0
    for percent in percents:
        avg = avg + percent[0]
        print(percent)
    avg = avg / len(percents)
    print("Average return: " + str(avg))


if __name__ == "__main__":
    check_ratios(pandas.read_pickle("pairs/pairs.pkl"))
