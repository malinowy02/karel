import matplotlib.pyplot as m
import plotly

f = open('PomiarPC.txt', 'r')
data = []
for line in f.readlines():
    tmp = line.split()
    new = []
    for str in tmp:
        str.split('=')
        new = new + str.strip(';').split('=')
    data.append([new[3], new[5]])
fd = open('Wyniki.txt', 'w')

x=[]
y=[]
for i in range(len(data)):
    x.append(float(data[i][0]))
    y.append(float(data[i][1]))
    
m.plot(x,y, 'bo')
m.plot(x,x)

m.show()

f.close()
