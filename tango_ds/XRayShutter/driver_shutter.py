# coding=utf-8
__author__ = 'arlen'
import serial
import sys


class Shutter:
    port = serial.Serial()
    timeout = int()

    def open_port(self):
        # инициализировать порт
        self.port = serial.Serial(4, timeout=self.timeout)

        # проверить работоспособность модуля
        self.port.write('$KE\r\n')
        if self.port.readline() != '#OK\r\n':
            sys.stderr.write("Module isn't in workable state")

    def __init__(self, timeout=1):
        self.timeout = timeout
        # открыть порт
        self.open_port()

        for i in xrange(1, 3):
            # настроить линию i в качестве выходной
            self.port.write("$KE,IO,SET," + str(i) + ",0,S\r\n")
            # проверить, что настройки применились верно
            if self.port.readline() != '#IO,SET,OK\r\n':
                sys.stderr.write("Module can't set the line " + str(i) + " for output")
            # установить на линию i высокий уровень напряжения
            self.port.write("$KE,WR," + str(i) + ",1\r\n")
            # проверить, что установилось верно
            if self.port.readline() == '#WR,WRONGLINE\r\n':
                sys.stderr.write("The line " + str(i) + " is configured for input, module can't write to it")
            elif self.port.readline() != '#WR,OK\r\n':
                sys.stderr.write("Module can't access to the line " + str(i) + " (didn't set value)")

        # настроить линию 4 в качестве входной
        self.port.write("$KE,IO,SET,4,1,S\r\n")
        if self.port.readline() != '#IO,SET,OK\r\n':
            sys.stderr.write("Module can't set the line 4 for input")

        # закрыть порт
        self.port.close()

    def check_state(self):
        # открыть порт
        self.open_port()

        # лямбда-функция для переворачивания значения: 0->1, 1->0
        inverse = lambda x: (1, 0)[int(x)]

        # послать запрос на считывание данных с 4 линии
        self.port.write("$KE,RD,4\r\n")

        # считать данные
        data = self.port.readline()

        # проверка на корректность
        if data == "#RD,WRONGLINE\r\n":
            sys.stderr.write("The line 4 is configured for output, module can't read from it")
        #TODO: проверка на корректность строки регулярным выражением (формат #RD,<LineNumber>,<Value>)

        # взять значение из строчки, перевернуть на обратное
        data = inverse(data.split(',')[2].replace('\r\n', ''))

        # записать перевернутое значение на 1 линию
        self.port.write("$KE,WR,1," + str(data) + "\r\n")
        # проверить, что записалось
        if self.port.readline() == '#WR,WRONGLINE\r\n':
            sys.stderr.write("The line 1 is configured for input, module can't write to it")
        elif self.port.readline() != '#WR,OK\r\n':
            sys.stderr.write("Module can't access to the line 1 (didn't set value)")

        # закрыть порт
        self.port.close()
        return [True, False][int(data)]

    def set_value(self, val):
        # открыть порт
        self.open_port()

        if not val in [0, 1]:
            sys.stderr.write("Trying to set incorrect value to shutter: expected 0 or 1, got " + str(val))

        # установить значение на реле (1 замкнуть, 0 разомкнуть)
        self.port.write("$KE,REL,1," + str(val) + "\r\n")

        # проверить, что значение установилось
        if self.port.readline() != "#REL,OK\r\n":
            sys.stderr.write("Can't set value " + str(val) + " to relay")

        # закрыть порт
        self.port.close()

