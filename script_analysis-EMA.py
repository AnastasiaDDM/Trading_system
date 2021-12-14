import pandas
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

### Данные ###
# Открытие файла с данными
# eth_usd = pandas.read_csv("content/ETH_USD.csv", skiprows=6)
eth_usd = pandas.read_excel("content/ETH-USD.xlsx")

ema1 = int(input('Введите длину периода первой средней (число)'))
ema2 = int(input('Введите длину периода второй средней (число)'))

### Настройки графика ###
# Создание графика
fig, ax = plt.subplots()
x = pandas.to_datetime(eth_usd["<DATE>"])
y = eth_usd["<CLOSE>"]

#  Устанавливаем интервалы для шкал:
ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(30))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
ax.yaxis.set_major_locator(ticker.MultipleLocator(500))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(100))

#  Линии сетки
ax.grid(which='major', color = 'k')
ax.minorticks_on()
ax.grid(which='minor', color = 'gray', linestyle = ':')

# Размер графика
fig.set_figwidth(16)
fig.set_figheight(12)

### Доп. информация ###
print(eth_usd["<CLOSE>"].describe())

### Индикаторы ###
# EMA - Экспоненциальные скользящие средние
# Экспоненциальные скользящие средние используют тогда, когда хотят снизить запаздывание, традиционно присущее Moving Average.
eth_usd['EMA'+ str(ema1)] = eth_usd['<CLOSE>'].ewm(com=ema1, min_periods=1).mean()
eth_usd['EMA'+ str(ema2)] = eth_usd['<CLOSE>'].ewm(com=ema2, min_periods=1).mean()

# Построение графиков
ax.plot(x, y, label="График цен")
ax.plot(x, eth_usd['EMA'+ str(ema1)], label = "EMA"+str(ema1), color='yellow', linewidth=2)
ax.plot(x, eth_usd['EMA'+ str(ema2)], label = "EMA"+str(ema2), color='red', linewidth=2)
ax.legend(fontsize = 'xx-large')

# Точки пересечения
idx = np.argwhere(np.diff(np.sign(eth_usd['EMA'+str(ema1)] - eth_usd['EMA'+str(ema2)]))).flatten()
plt.plot(x[idx], eth_usd['EMA'+str(ema1)][idx], 'go', linewidth=2)

# Отображение графика
# plt.savefig('saved_figure.png')
plt.show()

