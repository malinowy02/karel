import matplotlib.pyplot as m
import plotly.graph_objects as go
import numpy as np

def dane(file):
    data = []
    for line in file.readlines():
        tmp = line.split()
        new = []
        for str in tmp:
            str.split('=')
            new = new + str.strip(';').split('=')
        data.append([new[3], new[5]])
    x=[]
    y=[]
    for i in range(len(data)):
        x.append(float(data[i][0]))
        y.append(float(data[i][1]))
    return x,y

f = open('PomiarPC.txt', 'r')
fm = open('PomiarMAC.txt', 'r')


x,y = dane(f)
xm,ym = dane (fm)
    
m.style.use('seaborn')
m.plot(x, y, 'ko', label='Pomiary na jednym komputerze')
m.plot(xm, ym, 'r^', label='Pomiary na dwóch komputerach')
m.plot(x, x, label = 'Wartość teoretyczna')
m.suptitle('Wykres okresu w komunikacji symulowanej', fontsize=14)
m.xlabel('Ustawiony okres [ms]', fontsize=14)
m.ylabel('Okres rzeczywisty [ms]', fontsize=14)
m.legend()
m.show()



fr = open('PomiarROB.txt', 'r')

xr,yr = dane(fr)

m.figure(2)
m.style.use('seaborn')
m.plot(xr, yr, 'g^', label='Pomiary rzeczywisty robot - mac')
m.plot(x, y, 'ko', label='Pomiary na jednym komputerze')
m.plot(xm, ym, 'r^', label='Pomiary na dwóch komputerach')
m.plot(x, x, label = 'Wartość teoretyczna')
m.suptitle('Wykres zestawiający badania okresu', fontsize=14)
m.xlabel('Ustawiony okres [ms]', fontsize=14)
m.ylabel('Okres rzeczywisty [ms]',fontsize=14)
m.legend(fontsize=12)
m.show()


f.close()
