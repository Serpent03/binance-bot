trade = False
buyClamp = False
sellClamp = False

# MACD indicator
# SuperTrend indicator
# STOCH indicator
# RSI indicator
# Bollinger Band indicator
# IchiMoku Cloud

buyVote = [0, 0]
sellVote = [0, 0]

purchaseAmount = 0
purchasePrice = 0
init = True
lastMacd = 0
lastE = 0
lastTime = 0

import numpy as np
from talipp.indicators import EMA, RSI, ROC, ADX, SuperTrend, BB, Stoch, OBV, StochRSI, MACD
from talipp.ohlcv import OHLCVFactory

buyOrder = {
  "symbol": "",
  "side": "BUY",
  "type": "MARKET",
  "quoteOrderQty": 11
}
sellOrder = {
  "symbol": "",
  "side": "SELL",
  "type": "MARKET",
  "quoteOrderQty": 11
}

def rAvg(w, e):
  ''' window, element '''
  rA = 0
  if len(e) >= w:
    for i in range(w):
      rA += float(e[-(i+1)])
  return rA / w

def eAvg(w, e, smoothing = 2):
  ''' window, element, smoothing(default 2) '''
  eA = 0
  if len(e) >= w:
    eA = EMA(w, e)[-1]
  return eA

def getMACD(f, s, sig, e):
  r = MACD(f, s, sig, e)[-1].histogram
  return r

def getADX(w, e, w_di = 14):
  e = OHLCVFactory.from_matrix2(e)
  try:
    adx = ADX(w_di, w, e)[-1]
    return adx.adx
  except:
    return 0

def getSTOCHRSI(w, e, smoothing_k=3):
  w_s = w
  smoothing_d = smoothing_k
  r = StochRSI(w, w_s, smoothing_k, smoothing_d, e)[-1]
  return r

def superT(w, f, e):
  e = OHLCVFactory.from_matrix2(e)
  try:
    s = SuperTrend(w, f, e)
    return f"{s[-1].trend}" == "Trend.UP"
  except:
    return False

def bollinger(w, f, e):
  try:
    bbRet = BB(w, f, e)[-1]
    return bbRet
  except:
    return e[-1]

def getSTOCH(w, s, e):
  e = OHLCVFactory.from_matrix2(e)
  try:
    s = Stoch(w, s, e)[-1]
    return s
  except:
    pass
  return 0


def deltaRate(w, e):
  rc = 0
  try:
    rc = ROC(w, e)[-1]
  except:
    rc = 0
  return rc


def crossover(realPriceClose, EMA12, EMA26, EMA12Delta, EMA26Delta, macd, bb, EMA50, EMA200):
  global trade, purchasePrice, buyVote, sellVote

  if not trade:
    if realPriceClose[-1] / bb.lb <= 1.00001:
      buyVote = [1, 1]
    if buyVote == [1, 1]:
      buyVote = [0, 0]
      trade = True
      return 1

  if trade:
    if realPriceClose[-1] > bb.cb:
      sellVote = [1, 1]
    if sellVote == [1, 1]:
      sellVote = [0, 0]
      trade = False
      return -1
  return 0

def buySell(wallet, signal, real, tp):
  ''' wallet balance, signal, current price '''
  order = {}
  signal = int(signal)
  real = float(real)
  wb = float(wallet)
  global purchasePrice, purchaseAmount, trade
  if signal == 1:
    purchaseAmount = wallet * 0.9
    wb -= purchaseAmount
    purchasePrice = real
    buyOrder["symbol"] = tp
    buyOrder["quoteOrderQty"] = purchaseAmount
    order = buyOrder
  if signal == -1:
    sellOrder["symbol"] = tp
    sellOrder["quoteOrderQty"] = purchaseAmount
    order = sellOrder
    net = float((real - purchasePrice) / purchasePrice)
    wb += purchaseAmount + (purchaseAmount * net)
    # print(net)
    purchaseAmount = 0
    purchasePrice = 0
    maxHoldPrice = 0
  return [wb, order]