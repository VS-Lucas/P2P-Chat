import socket 

# Servidor que vai suportar duas conexões TCP.
# Após o estabelecimento das duas, o servidor envia para o peer1 a porta do peer2, e para o peer2 a porta do peer1,
# posteriormente usadas para conectar os dois peers.

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.bind(('localhost', 50001))
sck.listen(2)

peers = 0
portArray = []

while True:
    while peers < 2:
        conn, addr = sck.accept()
        if peers == 0:
            aux_addr = addr
            aux_conn = conn
        peers += 1
        print(f'Server connected with {addr[0]} {addr[1]}')
        portArray.append(addr[1])
    
    aux_conn.sendto(bytes(f'Your destination port {portArray[1]}', 'utf-8'), aux_addr)
    conn.sendto(bytes(f'Your destination port {portArray[0]}', 'utf-8'), addr)
    conn.close()
    aux_conn.close()
    peers = 0
    portArray.clear()