from masterVariables import *
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('ggplot')
# plt.subplot(2, 1, 1)
plt.subplots_adjust(0.114, 0.07, 0.962, 0.962)

xTitle = time
y1Title = liveClose
y2Title = exponentialAverageShort
y3Title = exponentialAverageLong
y4Title = exponentialAverageMedium
y5Title = liveOpen
signalBuy = signal

h1Title = ADXIndex
h2Title = rsi

# binance window duration
duration = -360

index = count()

def animate(i):
  tp = tP
  data = pd.read_csv(f'{tp}.csv')
  x = data[xTitle]
  y1 = data[y1Title]
  y2 = data[y2Title]
  y3 = data[y3Title]
  y4 = data[y4Title]
  y5 = data[y5Title]

  signalAlpha = data[sAlpha]
  signalColor = data[sColor]

  x = x[duration:]
  y1 = y1[duration:]
  y2 = y2[duration:]
  y3 = y3[duration:]
  y4 = y4[duration:]
  y5 = y5[duration:]

  wb = round(list(data[wallet])[-1], 5)

  signalColor = signalColor[duration:]
  signalAlpha = signalAlpha[duration:]

  plt.cla()
  plt.plot(x, y1, color = 'black', linewidth = 2, label=y1Title)
  # plt.plot(x, y5, color = 'green', linewidth = 2, label=y5Title)
  plt.plot(x, y2, color = 'purple', linewidth = 1.5, label=y2Title)
  plt.plot(x, y3, color = 'blue', linewidth = 1.5, label=y3Title)
  plt.plot(x, y4, color = 'red', linewidth = 1.5, label=y4Title)

  plt.scatter(x, y1, c = signalColor, marker = "D", alpha = (signalAlpha), label=wb)
  plt.legend(loc='lower left')

ani = FuncAnimation(plt.gcf(), animate, interval=500)
plt.show()