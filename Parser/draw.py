import matplotlib.pyplot as plt
from drawnow import drawnow
import numpy as np
import json
import time





plt.title("Зависимости: y1 = x, y2 = x^2") # заголовок
plt.xlabel("x")         # ось абсцисс
plt.ylabel("y1, y2")    # ось ординат
plt.grid()              # включение отображение сетки
plt.ion()
i = 1
x = [0]
y = [0]
y2 = [0]
temp_y = 1


def read_json(path='jsonDB.json'):
    with open(path, 'r') as file:
        return json.load(file)


def make_fig():
    plt.plot(x, y, x, y2)


def draw(id):
    a = read_json()
    current = a[id]
    for i in current.keys():
        price1 = current[i]['prices'][0]
        price2 = current[i]['prices'][1]
        price1 = (price1 + 100) / 100 if price1 > 0 \
            else (-price1 + 100) / -price1
        price2 = (price2 + 100) / 100 if price2 > 0\
            else (-price2 + 100) / -price2
        print(f"name: {current[i]['names'][0]}, price: {round(price1, 3)}"
              f" |  name: {current[i]['names'][1]}, price: {round(price2, 3)}")
        # temp_y += 1
        # x.append(temp_y)
        # y.append(price1)
        # y2.append(price2)
        # drawnow(make_fig)