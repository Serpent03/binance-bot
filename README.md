
# BinanceBot

BinanceBot is an automated trading bot that uses Python and TA algorithms to attempt automated trading of bitcoin on Binance.

## Pre-Requisites

- Python
- Python Binance wrapper(`pip install python-binance`)

## Installation

Clone the repository onto your local machine using git:

```bash
git clone https://github.com/Serpent03/binance-bot.git
```

To run the trading bot, open the folder and do `python3 pyBin.py`.

## How does it work?

The binance bot uses several technical analysis algorithms - EMA, Bollinger Bands, MACD, .. which all vote together if there is a time for an entry or exit in the trade. This ensures that the start of the trade is made with as much discipline as possible, and the exit of the trade is made with safe margins.

Running this bot during October 2022 on BTCUSDT yielded a profit of about $10 on a $30 investment.  
