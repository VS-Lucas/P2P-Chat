import socket 
from threading import Thread
from datetime import date
from datetime import datetime
import random

# O peer2 se conecta ao servidor e recebe a uma resposta contendo a porta do peer1.
# Posteriormente, o peer2 aceita a conexão do peer1 e dá início ao chat, através de threads para receber e enviar mensagens.
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
            socket.sendall(bytes(f'{newCont()}: User_2, {date.today()}, {datetime.now().hour}:{datetime.now().minute}: {msg}', 'utf-8'))
            print('Mensagem enviada com sucesso')
        except:
            print('Algo de errado aconteceu')
            socket.close()

    
def main():

    randAux = random.randint(60001, 65535)

    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.bind(('localhost', randAux))
    sck.connect(('localhost', 50001))

    data = sck.recv(1024).decode() 
    print(data)
    sck.close()


    sec_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sec_sck.bind(('localhost', randAux))
    sec_sck.listen(1)

    conn, addr = sec_sck.accept()
    conn.sendto(bytes(f'Connected', 'utf-8'), addr)
    print('Connected')

    rec = Thread(target=receive, args=(conn,))
    s = Thread(target=send, args=(conn,))

    rec.start()
    s.start()


main()