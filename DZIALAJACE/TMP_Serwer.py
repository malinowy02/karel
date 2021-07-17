from os import access
import socket
import sys
import time
import timeit
import PySimpleGUI as sg

# SERVER CONFIGURATION
server_address = ('',8000)
HOST = '127.0.0.1'
PORT = 8000
message = ''

class LimitsException(Exception):
    pass

class QuitException(Exception):
    pass

INPUT_KEYS = ["X_in", "Y_in", "Z_in", "W_in", "P_in", "R_in"]
AXES_LIMITS = [(-900, 900), (-900, 900), (-900, 900), (-180, 180), (-180, 180), (-180, 180)]


# MAIN FUNCTIONALITIES
def move(conn, **kwargs):
    
    # getting from kwargs
    values = kwargs.get("values", [0,0,0, 0, 0,0])
    input_vals = [values[k] for k in INPUT_KEYS]

    # ensure we don't exceed limits
    for value, limit, axis in zip(input_vals, AXES_LIMITS, INPUT_KEYS):
        _value = float(value)
        if _value <= limit[0] or _value >= limit[1]:
            raise LimitsException(f"Axis {axis} value is out of range!")

    conn.send(bytes("p" + 125 * " ", encoding="utf-8"))

    out_str = "".join([str(s) + (9 - len(str(s))) * ' ' for s in input_vals])
    out_bytes = bytes(out_str + (126-len(out_str)) * ' ', 'utf-8')
    conn.send(out_bytes)
    pass

def quit(conn, **kwargs):
    conn.send(bytes("0" + 125 * " ", encoding="utf-8"))
    raise QuitException("QUIT")
    
def dummy(conn, **kwargs):
    print("Method not implemented yet!")
    pass


def decode_coords(coords: bytes, separator: str=" "):
    """
    Decode a message from Karel
    """   
    decoded_coords = [float(i) for i in coords.decode().split(separator) if i != '']

    return tuple(decoded_coords)

# FUNCTIONS USED TO INVOKE BEHAVIOUR AFTER BUTTON CLICK IN GUI
event_functions = {"Move": move, "Quit": quit, "Ok": dummy}


# LAYOUT
sg.theme('DarkAmber')
layout = [  [sg.Text('Obecna pozycja robota')],
            [sg.Text('X'), sg.Text(size=(40,1), key='X')],
            [sg.Text('Y'), sg.Text(size=(40,1), key='Y')],
            [sg.Text('Z'), sg.Text(size=(40,1), key='Z')],
            [sg.Text('W'), sg.Text(size=(40,1), key='W')],
            [sg.Text('P'), sg.Text(size=(40,1), key='P')],
            [sg.Text('R'), sg.Text(size=(40,1), key='R')],
            [sg.Text('Docelowa pozycja')],
            [sg.Text('X'), sg.Input(key="X_in")],
            [sg.Text('Y'), sg.Input(key="Y_in")],
            [sg.Text('Z'), sg.Input(key="Z_in")],
            [sg.Text('W'), sg.Input(key='W_in')],
            [sg.Text('P'), sg.Input(key='P_in')],
            [sg.Text('R'), sg.Input(key='R_in')],
            [sg.Checkbox('Checkbox', default=True, k='-CB-')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Quit'), sg.Button("Move")] 
            ]

# Create the Window

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
        
        # Glowna petla programu
        while True:
            
            # Otrzymywanie koordynatów            
            data = conn.recv(126)       # 126 bajtów, bo tyle przesyła Karel
            x,y,z,w,p,r = decode_coords(data)

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
            
            event, values = window.read()

            try:
                event_functions[str(event)](conn, values=values)
            
            except QuitException as e:
                print(f"Exception occured while invoking function {event}: {e}")
                break
            
            except LimitsException as e:
                print(e)
                conn.send(bytes(126 * ' ', encoding="utf-8"))

        print("Zakonczono dzialanie serwera")
        f.close()
