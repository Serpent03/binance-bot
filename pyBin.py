from time import sleep
from masterVariables import *
from binance.spot import Spot
from kalmanfilter import KalmanFilter
import csv

kf = KalmanFilter()

currency = "BTC"
quoteCurrency = "USDT"
tradingPair = tP
client = Spot(apiKey, secretKey)

from smath import *

# kLines have a range of 500 units. =>> 500 seconds, 500 minutes,..
# data position =>> [1, 2, 3, 4, 5, 6] =>> OHLCVT

api_query = client.klines(tradingPair, '1s')[-1]

openPriceHistory = []
highPriceHistory = []
lowPriceHistory = []
closePriceHistory = []
volumeHistory = []
EMA26History = []
EMA12History = []
EMA50History = []
EMA200History = []
timeHistory = []

openPriceHistory.append(float(api_query[1]))
highPriceHistory.append(float(api_query[2]))
lowPriceHistory.append(float(api_query[3]))
closePriceHistory.append(float(api_query[4]))
volumeHistory.append(float(api_query[5]))
timeHistory.append(float(api_query[6]/1000))

ADXHeight = []
stochRSI = []
roc = 0

signalAttr = {
  -1: {
    "color": "red",
    "marker": "v",
    "alpha": 1
  },
  0: {
    "color": "white",
    "marker" : "^",
    "alpha": 0
  },
  1: {
    "color": "green",
    "marker": "^",
    "alpha": 1
  },
}

walletBalance = 25
fieldnames = [time, liveOpen, liveClose, exponentialAverageLong, exponentialAverageShort, exponentialAverageMedium, sColor, sAlpha, wallet, ADXIndex, rsi]

EMA12 = 9
EMA26 = 12
EMA50 = 50
EMA200 = 200

api_query = client.klines(tradingPair, '1s')
# api_query = client.klines(tradingPair, '1s')[-1]

for i in range(500):
  openPriceHistory.append(float(api_query[-(i+1)][1]))
  highPriceHistory.append(float(api_query[-(i+1)][2]))
  lowPriceHistory.append(float(api_query[-(i+1)][3]))
  closePriceHistory.append(float(api_query[-(i+1)][4]))
  volumeHistory.append(float(api_query[-(i+1)][5]))
  timeHistory.append(float(api_query[-(i+1)][6]/1000))

  EMA12History.append(eAvg(EMA12, closePriceHistory))
  EMA26History.append(eAvg(EMA26, closePriceHistory))
  EMA50History.append(eAvg(EMA50, closePriceHistory))
  EMA200History.append(eAvg(EMA200, closePriceHistory))

with open(f'{tradingPair}.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
  # if client.klines(tradingPair, '1s')[-1][6]/1000 != timeHistory[-1]:
  apiQuery = client.klines(tradingPair, '1s')[-1]
  openPriceHistory.append(float(apiQuery[1]))
  highPriceHistory.append(float(apiQuery[2]))
  lowPriceHistory.append(float(apiQuery[3]))
  closePriceHistory.append(float(apiQuery[4]))
  volumeHistory.append(float(apiQuery[5]))
  timeHistory.append(float(apiQuery[6]/1000))

  ohlcvList = [openPriceHistory, highPriceHistory, lowPriceHistory, closePriceHistory, volumeHistory]

  EMA12History.append(eAvg(EMA12, closePriceHistory))
  EMA26History.append(eAvg(EMA26, closePriceHistory))
  EMA50History.append(eAvg(EMA50, closePriceHistory))
  EMA200History.append(eAvg(EMA200, closePriceHistory))

  EMA12rate = deltaRate(12, EMA12History)
  EMA26rate = deltaRate(26, EMA26History)

  bollingerBand = bollinger(20, 1, closePriceHistory)
  MACDIndex = getMACD(12, 26, 9, closePriceHistory)

  signalVal = crossover(closePriceHistory, EMA12History[-1], EMA26History[-1], EMA12rate, EMA26rate, MACDIndex, bollingerBand, EMA50History[-1], EMA200History[-1])
  sigColor = signalAttr[signalVal]['color']
  sigAlpha = signalAttr[signalVal]['alpha']

  walletBalance, clientOrder = buySell(walletBalance, signalVal, closePriceHistory[-1], tradingPair)
  if clientOrder != {}:
    # client.new_order(clientOrder)
    pass

  with open(f'{tradingPair}.csv', 'a') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    info = {
      time: timeHistory[-1],
      liveClose: closePriceHistory[-1],
      liveOpen: openPriceHistory[-1],
      exponentialAverageShort: EMA12History[-1],
      exponentialAverageLong: EMA26History[-1],
      exponentialAverageMedium: EMA50History[-1],
      sColor: sigColor,
      sAlpha: sigAlpha,
      wallet: walletBalance,
    }
    csv_writer.writerow(info)

  sleep(1)

# predicted = kf.predict(24, priceHistory[-2])
# priceHistory.append((client.ticker_price(tradingPair)['price']))
# print(priceHistory[-2], predicted[1], priceHistory[-1], predicted[1] - float(priceHistory[-1]))
  
