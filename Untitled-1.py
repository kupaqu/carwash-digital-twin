from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
from enum import Enum
import random
import time
import matplotlib.pyplot as plt

class Place():
    def __init__(self):
        self.queue = []
    
    def addCarToQueue(self, car):
        self.queue.append(car)
    
    def pop(self):
        self.queue.pop(0)

    def calc(self):
        self.queue[0].minutesLeft -= 1
        if self.queue[0].minutesLeft == 0:
            self.pop()

class Carwash(QtWidgets.QMainWindow):
    def __init__(self, probs=0.05, *args, **kwargs):
        super(Carwash, self).__init__(*args, **kwargs)
        self.time = 0
        self.probs = probs
        self.costs = Costs()
        self.places = []

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = [0]
        self.y = [0]

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.calcMinute()

        self.x.append(self.time)  # Add a new value 1 higher than the last.

        self.y.append(self.costs.income-self.costs.costs)

        self.data_line.setData(self.x, self.y)

        time.sleep(0.1)

    def calcMinute(self):
        self.time += 1
        if random.random() < self.probs:
            car = Car()
            self.carToPlace(car)
            self.costs.calcCosts(car)
        print(f'============\n{self.time} MINUTE\n{self.costs}\n============\n')

    def addPlaces(self, number=1):
        for i in range(number):
            self.places.append(Place())

    # добавить машины в очередь
    def carToPlace(self, car):
        min = 0
        for i in range(len(self.places)):
            if len(self.places[min].queue) > len(self.places[i].queue):
                min = i
        self.places[min].addCarToQueue  (car)

class Costs():
    def __init__(self):
        self.water = 0
        self.foam = 0
        self.wax = 0
        self.electricity = 0

        self.income = 0
        self.costs = 0

    def calcCosts(self, car):
        for wash in car.washes:
            if wash == WashType.WATER:
                self.water += car.type.value * 4
                self.electricity += car.type.value * 2
            elif wash == WashType.FOAM:
                self.water += car.type.value * 1
                self.electricity += car.type.value * 2
                self.foam += car.type.value * 2
            elif wash == WashType.WAX:
                self.water += car.type.value * 2
                self.electricity += car.type.value * 2
                self.wax += car.type.value * 2
            elif wash == WashType.VACUUM:
                self.electricity += car.type.value * 4
            
            self.income += car.type.value * wash.value
            self.costs += car.type.value * wash.value * 0.5

    def __repr__(self):
        return f'WATER: {self.water} L\nFOAM: {self.foam} L\nWAX: {self.wax} L\nELECTRICITY: {self.electricity}\n\nINCOME:{self.income}\nCOSTS:{self.costs}\n'

class CarType(Enum):
    MICRO = 2
    SEDAN = 3
    WAGON = 4
    SUV = 6
    VAN = 8 

class WashType(Enum):
    WATER = 10
    FOAM = 50
    WAX = 40
    VACUUM = 20

class Car():
    def __init__(self):
        self.type = random.choice(list(CarType)) # случайный тип генерируемой машины
        washes = []
        for i in range(random.randint(2, 5)):
            washes.append(random.choice(list(WashType)))
        self.washes = washes
        self.minutesLeft = self.type.value * len(self.washes)
    def __repr__(self):
        return f'\nTYPE: {self.type}\nWASHES: {self.washes}\n'
    def __str__(self):
        return f'\nTYPE: {self.type}\nWASHES: {self.washes}\n'

app = QtWidgets.QApplication(sys.argv)
w = Carwash()
w.addPlaces(4)
w.show()
sys.exit(app.exec_())