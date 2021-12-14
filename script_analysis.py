import pandas
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from datetime import datetime, timedelta


def optimization(ax, eth_usd, x):
    # Переменная для максимума прибыли 0 - прибыль, 1 - MA1, 2 - MA2
    max = [0, [0, 0]]
    # Создаем цикл перебора разных длин средних
    for ma1 in range(5, 8):
        for ma2 in range(40, 80):

            ### Индикаторы ###
            # MA - Скользящие средние
            eth_usd['MA'+str(ma1)] = eth_usd['<CLOSE>'].rolling(int(ma1)).mean()
            eth_usd['MA'+str(ma2)] = eth_usd['<CLOSE>'].rolling(int(ma2)).mean()

            # Точки пересечения средних
            idx = np.argwhere(np.diff(np.sign(eth_usd['MA'+str(ma1)] - eth_usd['MA'+str(ma2)]))).flatten()

            # Подсчет прибыли от сделок, основанных на данных двух средних
            profit = cal_profit(eth_usd, x, idx, ma1, ma2)

            # Поиск максимального
            if profit > max[0]:
                max[0] = profit
                max[1] = [ma1, ma2]

    print('''
    Максимальная прибыль= %d
    MA1 = %d
    MA2 = %d
    ''' % (max[0], max[1][0], max[1][1]))

    # Построение графиков
    eth_usd['MA' + str(max[1][0])] = eth_usd['<CLOSE>'].rolling(int(max[1][0])).mean()
    eth_usd['MA' + str(max[1][1])] = eth_usd['<CLOSE>'].rolling(int(max[1][1])).mean()

    ax.plot(x, eth_usd['MA' + str(max[1][0])], label='MA' + str(max[1][0]), color='yellow', linewidth=2)
    ax.plot(x, eth_usd['MA' + str(max[1][1])], label='MA' + str(max[1][1]), color='red', linewidth=2)

    # Точки пересечения
    idx = np.argwhere(np.diff(np.sign(eth_usd['MA' + str(max[1][0])] - eth_usd['MA' + str(max[1][1])]))).flatten()
    plt.plot(x[idx], eth_usd['MA'+str(max[1][1])][idx], 'go', label = "Точки пересечения")
    ax.legend(fontsize='xx-large')
    # Отображение графика
    plt.show()


# Подсчет прибыли за операции на бирже
def cal_profit(eth_usd, x, idx, ma1, ma2):

    global m
    m=0
    profit = 0
    # Проходим по точкам пересечения и считаем в них прибыль
    for i in idx:
        new_date = x[i] - timedelta(days=1)
        if m==0:
            m=1
        else:
            # Правила стратегии
            # Сигнал на покупку возникает тогда, когда линия с меньшим периодом пересекает длинную снизу вверх.
            # Сигнал на продажу возникает тогда, когда линия с меньшим периодом пересекает длинную сверху вниз.

            short = eth_usd[(eth_usd['<DATE>'] == new_date)]['MA' + str(ma1)][i-1]
            long = eth_usd[(eth_usd['<DATE>'] == new_date)]['MA' + str(ma2)][i-1]

            # Провека на None значения
            if (pandas.notnull(short) & pandas.notnull(long)):

                # Проверяем, какая средняя находится выше
                if (short < long):
                    # Покупаем
                    # Уменьшаем сумму, так как покупаем
                    profit -= eth_usd[(eth_usd['<DATE>'] == x[i])]['<CLOSE>'][i]
                else:
                    # Продаем
                    # Увеличиваем сумму, так как продаем
                    profit += eth_usd[(eth_usd['<DATE>'] == x[i])]['<CLOSE>'][i]

    return profit


def start():
    ### Данные ###
    # Открытие файла с данными
    eth_usd = pandas.read_excel("content/ETH-USD.xlsx")

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

    # Построение графиков
    ax.plot(x, y, label="График цен")
    ax.legend(fontsize = 'xx-large')

    ### Доп. информация ###
    print(eth_usd["<CLOSE>"].describe())

    # Вызов функции оптимизации и основных расчетов
    optimization(ax, eth_usd, x)


# Входная функция
start()
