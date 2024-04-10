import sys
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1',5001))

server.listen()
'V1 1 0 5'
while True:
    client,address = server.accept()

    print('Connected')

    val = client.recv(1024).decode('utf-8')

    if val == 'compute':
        client.close()
        sys.exit()
    else:
        
        if val[0] == 'V':
            print('Voltage')
            print(val)

        elif val[0] == 'R':
            print('Resistor')
            print(val)
            
        elif val[0] == 'C':
            print('Capacitor')
            print(val)

        else:
            print('Not a valid component')