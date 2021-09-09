from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
from os import fork

def main():
    bufferSize = 1024
    host = ''
    if len(argv) > 1: port = int(argv[1])
    else: port = 5000
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    origem = (host, port)
    tcpSocket.bind(origem)
    tcpSocket.listen(0)
    print("Servidor pronto")
    while(True):
        con, cliente = tcpSocket.accept()
        pid = fork()
        if pid == 0:
            tcpSocket.close()
            print("Servidor conectado com ", cliente)
            while True:
                msg = con.recv(bufferSize)
                if not msg: break
                print(cliente, msg)
            print("Conexão terminada com ", cliente)
            con.close()
            exit()
        else:
            con.close()
    return

if __name__ == "__main__":
    main()
    
# Tenho que começar a olhar dos slides 261
