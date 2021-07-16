import socket
import sys
import time
import timeit

server_address = ('',8000)
HOST = '127.0.0.1'
PORT = 8000
message = ''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind(server_address)       #uruchomienie socketu z podanym adresem 
    print ("Starting up on %s port %s" %server_address)
    #print ("Waiting for connection...")
    s.listen()                  #oczekiwanie na polaczenie
    conn, c_addr = s.accept()   #start polaczenia z clientem
    
    with conn:
        print ("Connection from ", c_addr)
        t0 = time.time()
        licznik=0
        f = open("dane.txt", "w")   #tworzy nowy plik lub nadpisuje
        #Glowna petla programu
        while True:
            data=conn.recv(126)    #otrzymanie wiadomosci od Karela
            print('Otrzymano: ',data)   #wypisanie otrzymanej wiadomosci


            out_str=input("Wpisz wiadomosc: ")      #wpisanie polecenia z klawiatury     
            out_str=out_str + (126-len(out_str))*' '    #formatowanie wiadomosci do dlugosci jakiej oczekuje karel
            out_byt=bytes(out_str,'utf-8')  #zakodowanie wiadomosci na bity
            conn.send(out_byt)  #wiadomosc wysylana do Karela
            if out_str[:1] == '0':        #gdy wpiszesz 0 zamknij serwer
                break
            
            if out_str[:1] == 'p':
                out_str=input("Enter X,Y,Z,W,P,R: ")
                temp=out_str.split(',')
                out_str=''
                for i in range(len(temp)):
                    g=float("{:.3f}".format(float(temp[i])))
                    #print('liczba=',g)
                    s=str(g)
                    out_str=out_str+s+(9-len(s))*' '
                out_str=out_str + (126-len(out_str))*' '    #formatowanie wiadomosci do dlugosci jakiej oczekuje karel
                out_byt=bytes(out_str,'utf-8')  #zakodowanie wiadomosci na bity
                print('Wysylam: ',out_byt)
                conn.send(out_byt)  #wiadomosc wysylana do Karela

            message = str(data) + '\n'  #formatowanie do pliku z nastepna linia
            f.write(message)

        print("Zakonczono dzialanie serwera")
        f.close()
