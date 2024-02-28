import socket
import threading
import ssl
import os
from pyfiglet import figlet_format
from colorama import Fore, init

host = '10.1.19.9'  # LocalHost
port = 7976  # Choosing unreserved port

clients = {}
nicknames = {}
rooms = {}

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def broadcast(message, thisguy, room=''):
    if room:
        for client in rooms[room]:
            client.send(message)
    else:
        for client in rooms[clients[thisguy]]:
            client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            data = message.decode('utf-8')
            if data.startswith('Details'):
                room = data.replace('Details ', '')
                rooms[clients[client]].remove(client)
                ex = clients[client]
                clients[client] = room
                if room in rooms:
                    members = [nicknames[client] for client in rooms[room]]
                    members = ' ,'.join(members)
                    client.send(f" 📢 {members} already in the room!".encode('utf-8'))
                    rooms[room].append(client)
                else:
                    rooms[room] = [client]
                broadcast(f" 📢 {nicknames[client]} joined!".encode('utf-8'), client)
                broadcast(f" 📢 {nicknames[client]} left!".encode('utf-8'), client, room=ex)
            else:
                broadcast(message, client)
        except:
            broadcast(f" 📢 {nicknames[client]} left!".encode('utf-8'), client, room=clients[client])
            clients.pop(client)
            client.close()
            nickname = nicknames[client]
            broadcast('{} left!'.format(nickname).encode('utf-8'), client)
            nicknames.pop(client)
            break

def receive():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('abhi.crt', 'abhi.key')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        with context.wrap_socket(server, server_side=True) as ssock:
            print(Fore.GREEN + "\033[1m🚨🚨🚨 You can see all the joined devices below\033[0m")
            print("\n")
            while True:
                client, address = ssock.accept()
                print("🔘 Connected with {}".format(str(address)))       
                client.send('DETAILS'.encode('utf-8'))
                data = client.recv(1024).decode('utf-8')
                data = data.replace('Details ', '')
                nickname, room = data.split(',')
                clients[client] = room
                nicknames[client] = nickname
                if room in rooms:
                    rooms[room].append(client)
                else:
                    rooms[room] = [client]
                print("   {} joined {}".format(nickname, room))
                broadcast(" 📢 {} joined!".format(nickname).encode('utf-8'), client)
                client.send(f' 📢 Connected to {room} room!'.encode('utf-8'))
                if len(rooms[room]) > 1:
                    members = [nicknames[client] for client in rooms[room][:-1]]
                    members = ' ,'.join(members)
                    client.send(f" 📢 {members} already in the room!".encode('utf-8'))
                
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()

if __name__ == "__main__":
    clear_screen()
    print(Fore.CYAN + figlet_format("CHATTER BOX", font="big_money-se"))
    print("\n")
    print(f"Started server on {host}:{port} 🗄️🗄️🗄️...\n")
    
    receive()