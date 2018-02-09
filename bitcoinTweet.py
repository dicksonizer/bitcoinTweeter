from twython import Twython
import ccxt
import time

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

binance			= ccxt.binance() 
bitfinex 		= ccxt.bitfinex()
gemini 			= ccxt.gemini()
gdax  			= ccxt.gdax()
bittrex 		= ccxt.bittrex() 
exchanges 		= [binance,bitfinex,gemini,gdax,bittrex]
hourlyPrice		= []



def tweet():
	if len(hourlyPrice) <= 1:
		message = "The current price of Bitcoin is: " + str(averagePrice)
	elif len(hourlyPrice) > 1 and len(hourlyPrice) <= 23 :
		message = "The current price of Bitcoin is: " + str(averagePrice) + "\n" + "Last Hour: " + hourDifference
	elif len(hourlyPrice) > 23:
		message = "The current price of Bitcoin is: " + str(averagePrice) + "\n" + "Last Hour: " + hourDifference + "\n" + "Last 24 Hours: " + dayDifference
	twitter.update_status(status=message)
	print("Tweeted: %s" % message)


def getPrices():
	prices = []
	for i in exchanges:
		if i == binance or i == bittrex:
			iBTC = i.fetch_ticker('BTC/USDT')
		else:
			iBTC = i.fetch_ticker('BTC/USD')
		iBTCPrice = iBTC['last']
		prices.append(iBTCPrice)
	global averagePrice
	averagePrice = round(sum(prices)/len(prices), 2)
	hourlyPrice.append(averagePrice)
	print(averagePrice)	

def percentageDiff():	
	if len(hourlyPrice) > 1:
		global hourDifference
		hourDifference = str(round(((hourlyPrice[-1]/hourlyPrice[-2] -1 )*100),2)) + "%"
		if len(hourlyPrice) % 24 == 0:
			global dayDifference
			dayDifference = str(round(((hourlyPrice[-24]/hourlyPrice[-1] -1 )*100),2)) + "%"
			if dayDifference == "-0.0%":
				dayDifference = "0.00%"

		

while True:
	getPrices()
	percentageDiff()
	tweet()
	time.sleep(3)
	print(len(hourlyPrice))
	if len(hourlyPrice) % 24 == 0:
		print(dayDifference)
		print(hourlyPrice)




