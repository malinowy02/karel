from os import access, write
import socket
import sys
import time
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import B

class LimitsException(Exception):
    pass

class QuitException(Exception):
    pass

class BadFormatException(Exception):
    pass

INPUT_KEYS = ["X_in", "Y_in", "Z_in", "W_in", "P_in", "R_in"]
AXES_LIMITS = [(-900, 900), (-900, 900), (-900, 900), (-180, 180), (-180, 180), (-180, 180)]
PR_LIMITS = (1,100)


# MAIN FUNCTIONALITIES
def writepos (conn, **kwargs):
    # getting from kwargs
    values = kwargs.get("values", [0,0,0, 0, 0,0])
    input_vals = [values[k] for k in INPUT_KEYS]

    register=values["PR_in"]
    if register.isnumeric():
        # ensure we don't exceed limits
        for value, limit, axis in zip(input_vals, AXES_LIMITS, INPUT_KEYS):
            _value = float(value)
            if _value < limit[0] or _value > limit[1]:
                window['War'].update(f'Wartosc {axis} jest poza zakresem!')
                raise LimitsException(f"Axis {axis} value is out of range!")
        window['War'].update('')
        conn.send(bytes("p" + 125 * " ", encoding="utf-8"))

        out_str = "".join([str(s) + (9 - len(str(s))) * ' ' for s in input_vals])
        out_bytes = bytes(out_str + (126-len(out_str)) * ' ', 'utf-8')
        conn.send(out_bytes)
        print('sent: ',out_bytes)
        register=values["PR_in"]
        out_str = "".join(register)
        out_bytes = bytes(out_str + (126-len(out_str)) * ' ', 'utf-8')
        conn.send(out_bytes)
        print('sent: ',out_bytes)
        pass
    raise BadFormatException

def quit(conn, **kwargs):
    conn.send(bytes("0" + 125 * " ", encoding="utf-8"))
    raise QuitException("QUIT")
    
def dummy(conn, **kwargs):
    print("Method not implemented yet!")

def readpos(conn, **kwargs):
    conn.send(bytes("r" + 125 * " ", encoding="utf-8"))
    data = conn.recv(126)       # 126 bajtów, bo tyle przesyła Karel
    x,y,z,w,p,r = decode_coords(data)
    window['X'].update(x)
    window['Y'].update(y)
    window['Z'].update(z)
    window['W'].update(w)
    window['P'].update(p)
    window['R'].update(r)
    pass

def readpr(conn, **kwargs):
    register=values["PR_read"]
    if register.isnumeric():
        conn.send(bytes("e" + 125 * " ", encoding="utf-8"))
        register=values["PR_read"]
        out_str = "".join(register)
        conn.send(bytes(out_str + (126-len(out_str)) * ' ', 'utf-8'))
        data = conn.recv(126)       # 126 bajtów, bo tyle przesyła Karel
        x,y,z,w,p,r = decode_coords(data)
        window['X'].update(x)
        window['Y'].update(y)
        window['Z'].update(z)
        window['W'].update(w)
        window['P'].update(p)
        window['R'].update(r)
        pass
    raise BadFormatException

def move(conn, **kwargs):
    register=values["PR_go"]
    if register.isnumeric():
        conn.send(bytes("m" + 125 * " ", encoding="utf-8"))
        target=values["PR_go"]
        out_str = "".join(target)
        out_bytes = bytes(out_str + (126-len(out_str)) * ' ', 'utf-8')
        conn.send(out_bytes)

        data = conn.recv(126)       # 126 bajtów, bo tyle przesyła Karel
        if int(data) == 1:
            print('Pozycja osiagalna')
            window['War'].update('')
        else:
            print('Nieosiagalna pozycja')
            window['War'].update('Nieosiagalna pozycja!')
        pass
    raise BadFormatException

def decode_coords(coords: bytes, separator: str=" "):
    """
    Decode a message from Karel
    """   
    decoded_coords = [float(i) for i in coords.decode().split(separator) if i != '']

    return tuple(decoded_coords)

# FUNCTIONS USED TO INVOKE BEHAVIOUR AFTER BUTTON CLICK IN GUI
event_functions = {"Write Pos": writepos, "Quit": quit, "None":quit, "Read CurPos": readpos, "Read PR":readpr, "Move":move, "Dummy":dummy}


# LAYOUT
sg.theme('DarkAmber')
layout = [  [sg.Text('Obecna pozycja robota')],
            [sg.Text('X'), sg.Text(size=(40,1), key='X')],
            [sg.Text('Y'), sg.Text(size=(40,1), key='Y'), sg.Button('Read CurPos')],
            [sg.Text('Z'), sg.Text(size=(40,1), key='Z')],
            [sg.Text('W'), sg.Text(size=(40,1), key='W')],
            [sg.Text('P'), sg.Text(size=(40,1), key='P'), sg.Text('Wczytaj PR'), sg.Input(key="PR_read")],
            [sg.Text('R'), sg.Text(size=(40,1), key='R'), sg.Button("Read PR"), sg.Text('(nie dziala na niezainicjowane')],
            [sg.Text('Docelowa pozycja')],
            [sg.Text('X'), sg.Input(key="X_in")],
            [sg.Text('Y'), sg.Input(key="Y_in")],
            [sg.Text('Z'), sg.Input(key="Z_in"), sg.Text('Wpisz w rejestr PR'), sg.Input(key="PR_in")],
            [sg.Text('W'), sg.Input(key='W_in'), sg.Button("Write Pos")],
            [sg.Text('P'), sg.Input(key='P_in')],
            [sg.Text('R'), sg.Input(key='R_in')],
            [sg.Text('Ruch Robota'), sg.Text('Cel PR'), sg.Input(key="PR_go"), sg.Button("Move")],
            [sg.Button('Quit'), sg.Text('Warnings: '), sg.Text(size=(40,1), key='War')],
            [sg.Button('Dummy')]
            ]

# SERVER CONFIGURATION
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
        print("Connection from ", c_addr)
        t0 = time.time()
        licznik = 0
        f = open("dane.txt", "w")   #tworzy nowy plik lub nadpisuje

        # Odpal okienko
        window = sg.Window('Fanuc TCP', layout, finalize=True)
        
        first=True
        # Glowna petla programu
        while True:
            
            # Otrzymywanie koordynatów            
            data = conn.recv(126)       # 126 bajtów, bo tyle przesyła Karel
            x,y,z,w,p,r = decode_coords(data)

            if first == True:
                # Update GUI coordswindow['X_in'].update(x)
                window['X'].update(x)
                window['Y'].update(y)
                window['Z'].update(z)
                window['W'].update(w)
                window['P'].update(p)
                window['R'].update(r)

                window['X_in'].update(x)
                window['Y_in'].update(y)
                window['Z_in'].update(z)
                window['W_in'].update(w)
                window['P_in'].update(p)
                window['R_in'].update(r)

                window['PR_in'].update('1')
                window['PR_go'].update('1')
                window['PR_read'].update('1')
                first=False
            
            event, values = window.read()

            try:
                # print(f'Event: {str(event)}') #wypisanie jaki event wystapil
                event_functions[str(event)](conn, values=values)
            
            except QuitException as e:
                print(f"Exception occured while invoking function {event}: {e}")
                break
            
            except LimitsException as e:
                print(e)
                conn.send(bytes(126 * ' ', encoding="utf-8"))
            except BadFormatException as e:
                print(e)
                conn.send(bytes(126 * ' ', encoding="utf-8"))

        print("Zakonczono dzialanie serwera")
        f.close()
