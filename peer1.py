import socket 
from threading import Thread
from datetime import date
from datetime import datetime
import random

# O peer1 se conecta ao servidor e recebe a uma resposta contendo a porta do peer2.
# Posteriormente, o peer1 se conecta ao peer2 e dá início ao chat, através de threads para receber e enviar mensagens.
# As mensagens contém um número de sequência, o nome do usuário, data atual e horário atual.

intNum = 0

def newCont():
    global intNum
    intNum += 1
    return intNum

def receive(socket):
    while True:
        data = socket.recv(1024).decode()
        print(data)


def send(socket):
    while True:
        try:
            msg = input()
            socket.sendall(bytes(f'{newCont()}: User_1, {date.today()}, {datetime.now().hour}:{datetime.now().minute}: {msg}', 'utf-8'))
            print('Mensagem enviada com sucesso')
        except:
            print('Algo de errado aconteceu')
            socket.close()


def main():

    randAux = random.randint(32000, 40000)
    
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.bind(('localhost', randAux))
    sck.connect(('localhost', 50001))

    data = sck.recv(1024).decode() 
    print(data)
    sck.close()

    aux = data.split()
    destPort = aux[3]

    sec_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sec_sck.bind(('localhost', randAux))
    sec_sck.connect(('localhost', int(destPort)))

    data = sec_sck.recv(1024).decode() 

    if data == 'Connected':
        print('Connected')

    rec = Thread(target=receive, args=(sec_sck,))
    s = Thread(target=send, args=(sec_sck,))

    rec.start()
    s.start()

main()



