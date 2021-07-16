import socket
import sys
import time
import timeit




out_str=input("Enter X,Y,Z,W,P,R: ")
temp=out_str.split(',')
print(temp)
out_str=''
for i in range(len(temp)):
    g=float("{:.3f}".format(float(temp[i])))
    #print('liczba=',g)
    s=str(g)
    out_str=out_str+s+(9-len(s))*' '
print(out_str)
