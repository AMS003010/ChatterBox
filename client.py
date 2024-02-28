import socket
import threading
import ssl
from bot import Bot
from colorama import init, Fore
import os
from pyfiglet import figlet_format

nickname = input("Choose your nickname: ")
ip_addr =  input("Enter the IP address: ")
port_soc = 7976
room = input("Enter the Room Name to Join: ")
print("\n")

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Create a regular socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the socket with SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('abhi.crt')
secure_client = context.wrap_socket(client, server_hostname='Abhi')

try:
    # Connect to the server
    clear_screen()
    print(Fore.CYAN + figlet_format("CHATTER BOX", font="big_money-se"))
    print("\n")
    secure_client.connect((ip_addr, int(port_soc)))
    print("Connected to the server.")
except Exception as e:
    print("Connection failed:", e)
    exit()

client_clos = True

def receive():
    while True:
        try:
            message = secure_client.recv(1024).decode('utf-8')
            if message == 'DETAILS':
                msg = 'Details ' + nickname + ',' + room
                secure_client.send(msg.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            if client_clos:
                print(f"An error occurred: {e}")
            secure_client.close()
            break

def write():
    while True:
        client_msg = input('')
        message = '\n{}: {}\n'.format(Fore.LIGHTBLACK_EX + nickname, Fore.LIGHTRED_EX + client_msg)
        mssg = str(message)
        if client_msg == '':
            secure_client.send(message.encode('utf-8'))
        elif client_msg[0] == '@':
            colon_index = mssg.index(':')
            substring = mssg[colon_index+1:].strip()
            Bot(substring[1:])
        elif client_msg.lower() in ["exit", "quit"]:
            choice = input('Would you like to join a different room (Y/N): ')
            if choice.lower() == 'y':
                room = input('Enter the Room Name to Join: ')
                msg = 'Details ' + room
                secure_client.send(msg.encode('utf-8'))
                clear_screen()
                print(Fore.CYAN + figlet_format("CHATTER BOX", font="big_money-se"))
                print("\n")
                print(f' 📢 Connected to {room} room!')
            else:
                global client_clos
                client_clos = False
                secure_client.close()
                print("Connection closed.")
                break
        else:
            secure_client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()