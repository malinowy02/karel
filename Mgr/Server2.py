import socket
import sys
import time
import timeit

server_address = ('127.0.0.1',8000)
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
        #print ("Connection from ", c_addr)
        t0 = time.time()
        licznik=0
        f = open("dane.txt", "w")   #tworzy nowy plik lub nadpisuje
        #Glowna petla programu
        while True:
            data=conn.recv(126)    #otrzymanie wiadomosci od Karela
            #print(repr(data))   #wypisanie otrzymanej wiadomosci
            #print("licznik:", licznik)
            message = str(data) + '\n'  #formatowanie do pliku z nastepna linia
            f.write(message)    #zapisanie pozycji w pliku
            licznik+=1
            if not data:        #gdy nic nie zostalo otrzymane, zamknij serwer
                break
            conn.sendall(data)  #wiadomosc Echo wysylana do Karela
        t1 = time.time()
        total = t1-t0
        print("czas:", total)   #czas wykonywania programu od momentu polaczenia
        print("licznik:", licznik)    #ilosc otrzymanych paczek z danymi (6x wiecej niz wyslanych)
        f.close()
