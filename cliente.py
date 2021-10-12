import socket
import threading

HOST = '127.0.1.1'
PORT = 20000

udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
dest = (HOST,PORT)

bye = False

def recebe():
    while not bye:
        m = udp.recvfrom(1024)[0].decode()

        if 'entrou' in m:
            print(m[5:])
        
        elif 'saiu' in m:
            print(m[5:])

        elif 'MSG' in m:
            m = m[4:].split(':')
            print(m[0],'disse:',m[1])
        #print(m.decode())

        elif 'LIST' in m:
            print('Usuários conectados:',m[5:])

        elif 'enviou' in m:
            print(m[5:])

    return

def envia():
    while True:
        m = input()

        if m == '/bye':
            udp.sendto(('BYE').encode(),dest)
            udp.close()
            bye = True
            break

        elif m == '/list':
            udp.sendto(('LIST').encode(),dest)

        elif '/file' in m:
            arq = (m.split())[1]
            udp.sendto(('FILE:' + arq).encode(),dest)

            tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #print('antes connect')
            tcp.connect(dest)

            #msg = input()
            #tcp.send(msg.encode())

            arquivo = open(arq,'rb')
            dados = arquivo.read()
            tcp.send(dados)
            '''
            dados = arquivo.read(1024)
            while dados:
                print('mandando...')
                tcp.send(dados)
                dados = arquivo.read(1024)
            '''
            #tcp.send(arquivo.read())

            arquivo.close()

            tcp.close()


        elif '/get' in m:
            arq = (m.split())[1]
            
            udp.sendto(('GET:' + arq).encode(),dest)

            tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            tcp.connect(dest)

            arquivo = open(arq,'wb')
            dados = tcp.recv(1024)
            arquivo.write(dados)

            arquivo.close()

            tcp.close()
        
        else:
            msg = 'MSG:' + m
            udp.sendto(msg.encode(),dest)

    return

#msg = input()

#while msg != 'bye':
#    udp.sendto(msg.encode(),dest)
#    resp = udp.recvfrom(1024)[0]
#    print(resp.decode())
#    msg = input()

usuario = input('Nome de usuário: ')
udp.sendto(('USER:'+usuario).encode(),dest)


(threading.Thread(target=recebe)).start()
(threading.Thread(target=envia)).start()



