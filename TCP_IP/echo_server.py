import socket

HOST = '127.0.0.1'  #Standard localhost
PORT = 65432        #Port to listen on (non-privileged ports >1023)

#when using 'with' there's no need to call s.close()
#AF_INET is IPv4 address, SOCK_STREAM is TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))         #associate socket with network interface and port number
    s.listen()                  #waiting for client connection

    conn, addr = s.accept()     #connecting with client
    with conn:
        print('Connected by', addr) #connected

        while True:             #echo loop
            data=conn.recv(1024)
            print(repr(data))
            if not data:
                break
            conn.sendall(data)