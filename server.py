from os import write
import socket
import threading

HOST = ''
PORT = 20000

users = {}
nomes = []
arqNome = ''

def conecta():
    udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    orig = (HOST,PORT)
    udp.bind(orig)

    tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    tcp.bind(orig)
    tcp.listen(1)

    while True:
        msg,cliente = udp.recvfrom(1024)

        if 'USER' in msg.decode():
            usuario = msg.decode()[5:]
            for i in users:
                udp.sendto(('INFO:' + usuario + ' entrou').encode(),i)
            
            users[cliente] = usuario
            nomes.append(usuario)
            #print(nomes)

        elif msg.decode() == 'LIST':
            m = 'LIST:'
            for i in range(len(nomes)-1):
                m += nomes[i] + ', '
            m += nomes[len(nomes)-1]
            udp.sendto(m.encode(),cliente)

        elif msg.decode() == 'BYE':
            usuario = users[cliente]
            nomes.remove(users[cliente])
            del users[cliente]

            for i in users:
                udp.sendto(('INFO:' + usuario + ' saiu').encode(),i)
        
        elif 'FILE' in msg.decode():
            arqNome = msg.decode()[5:]
            clienteUDP = cliente
            #print(arqNome)

            con,cliente = tcp.accept()

            arquivo = open(arqNome,'wb')
            dados = con.recv(1024)
            arquivo.write(dados)
            
            arquivo.close()
            con.close()
            #print('mandou')
            m = 'INFO:' + users[clienteUDP] + ' enviou ' + arqNome
            #print(m)
            #print('cliudp',clienteUDP)
            #print('clitcp',cliente)
            for i in users:
                #print('i:',i,'->',users[i])
                if i != clienteUDP:
                    udp.sendto(m.encode(),i)

        elif 'GET' in msg.decode():
            arqNomeGet = msg.decode()[4:]
            if (arqNome != arqNomeGet):
                udp.sendto(('ARQUIVO NÃO ENCONTRADO').encode(),cliente)

            else:
                clienteUDP = cliente
                
                con,cliente = tcp.accept()

                arquivo = open(arqNomeGet,'rb')
                dados = arquivo.read()
                con.send(dados)

                arquivo.close()
                con.close()


        else:
            m = msg.decode()[4:]
            m = 'MSG:' + users[cliente] + ':' + m
            for i in users:
                if i != cliente:
                    udp.sendto(m.encode(),i)
            #for i in users:

        #if cliente not in users:
        #    users[cliente] = msg.decode()[5:]
        #    nomes.append(msg.decode()[5:])
        #print(cliente,' ',msg.decode())
    
    udp.close()

    return

(threading.Thread(target=conecta)).start()


