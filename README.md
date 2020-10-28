# pairsTrading
A python bot to pairs trade

Stock data is pulled from yahoo finance's API and converted to a .pkl file, which is then analyzed in pairs. If the price of one of the stocks in the pair deviates more than 2 standard deviations from the mean the bot issues either a buy or sell command. Currently it is not configured to use any live trading API, but backtesting scripts are included
