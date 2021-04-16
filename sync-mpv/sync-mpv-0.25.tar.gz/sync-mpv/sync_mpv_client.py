#!/usr/bin/env python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from python_mpv_jsonipc import MPV
from configparser import ConfigParser
import socket
import os
import hashlib
import sys
import threading
import errno
import time
import datetime

global connected
global mpv





def receive_message(client_socket):

    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header)

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False

    msg = client_socket.recv(message_length)

    decrypted_msg = decrypt_message(msg[16:], msg[:16])

    return_list = decrypted_msg.split(" , ")
    if len(return_list) > 1:
        msg = return_list[0]
        user = return_list[1]

        return msg, user
    else:
        return decrypted_msg, "Server"

    return decrypted_msg

    # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
    #if not len(message_header):
    #    return False

    # Convert header to int value

def pause_video(mpv):
    mpv.command("set_property","pause", True)

def play_video(mpv):
    mpv.command("set_property","pause", False)

def toggle_play(mpv):
    isPaused = mpv.command("get_property","pause")
    if isPaused == True:
        play_video(mpv)
    else:
        pause_video(mpv)

def new_video(mpv, new_link):
    global t_playback
    if new_link is not None:
        pause_video(mpv)
        mpv.play(new_link)
        play_video(mpv)
    t_playback = 0

def new_message():
    thread = True
    global connected
    while thread == True:
        msg = input(f'{my_username} > ')
        if msg == "q":
            thread = False
            connected = False
        if msg[:3] == "mpv":
            print (msg)
        else:
            send(client_socket, msg)

def send(clientsocket, msg):
    global KEY
    cipher = AES.new(KEY, AES.MODE_CBC)

    if type(msg) is not bytes:
       msg = msg.encode("utf-8")

    msg = encrypt_message(msg)
    send_length = prepare_concatenation(len(msg))

    clientsocket.sendall(send_length)
    clientsocket.sendall(msg)

def encrypt_message(msg):
    global KEY

    cipher = AES.new(KEY, AES.MODE_CBC)

    encrypted_msg = cipher.encrypt(pad(msg,AES.block_size))
    encrypted_msg = cipher.iv + encrypted_msg

    return encrypted_msg

def decrypt_message(msg, IV):
    global KEY
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_msg = unpad(cipher.decrypt(msg), AES.block_size)

    try:
        decrypted_msg = decrypted_msg.decode("utf-8")
    except UnicodeDecodeError:
        pass

    return decrypted_msg

def prepare_concatenation(msg):
    global HEADER_LENGTH
    concat = str(msg).encode("utf-8")
    concat += b' ' * (HEADER_LENGTH - len(concat))
    return concat

def ready_when_seeked(mpv):
    while True:
        seek_bool = mpv.command("get_property","seeking")
        if seek_bool == False:
            pause_video(mpv)
            break
    send(client_socket, "ready")

def exit_gracefully():
    send(client_socket, "!DISCONNECT")

def handle_server(server,addr):
    global connected
    global t_playback
    global mpv
    global client_socket

    t_playback = 0
    connected = True
    mpv = MPV(start_mpv=True, quit_callback=exit_gracefully)
    mpv.command("set_property","osd-font-size","18")

    @mpv.property_observer("playback-time")
    def observe_playback_time(name, value):  
        global t_playback  
        if value is not None:
            if value > t_playback+0.25 or value < t_playback:
                t_playback = mpv.command("get_property", "playback-time")
                pause_video(mpv)
                print (t_playback)
                send(client_socket, f"mpv skip {t_playback}")
            t_playback = value
    
    @mpv.property_observer("path")
    def observe_path(name, value):
        if value is not None:
            print (f"New Path: {value}")            
            send(client_socket, f"mpv new {value}")
            new_video(mpv, value)

    @mpv.on_key_press("space")
    def toggle_playback():
        toggle_play(mpv)
        send(client_socket, "toggle play")

    @mpv.on_key_press("q")
    def terminate():
        global connected
        print("Q")
        send(client_socket, "!DISCONNECT")
        #connected = False

    print(f"[CONNECTION ESTABLISHED] to {addr}")
    
    while connected:
        try:
            msg, user = receive_message(server)

            if msg:

                if msg == "!DISCONNECT":
                    connected = False
                    break

                if msg == "mpv pause":
                    pause_video(mpv)

                if msg == "mpv terminate":
                    connected = False

                if msg == "mpv playback":
                    play_video(mpv)

                if "disconnected" in msg:
                    mpv.command("show-text",f"{msg}", "5000")

                if msg == "number of clients":
                    number_of_clients = int(msg.split[" "][3])
                    print ("Number of Clients: %s"%number_of_clients)
                    
                if msg == "toggle play":
                    toggle_play(mpv)
                    mpv.command("show-text",f"{user} toggles", "1500")

                if "mpv skip" in msg:
                    t_playback = float(msg.split(" ")[2])

                    if t_playback < 3600:
                        converted_time = time.strftime("%M:%S", time.gmtime(t_playback))
                    else:
                        converted_time = time.strftime("%H:%M:%S", time.gmtime(t_playback))

                    mpv.command("set_property","playback-time",msg.split(" ")[2])
                    mpv.command("show-text",f"{user} skips to {converted_time}", "1500")

                    pause_video(mpv)                 
                    ready_when_seeked(mpv)

                if "mpv new" in msg:
                    videopath = msg[8:]
                    new_video(mpv, videopath)
                    mpv.command("show-text",f"{user}: {videopath}","1500")
                    pause_video(mpv)
                    ready_when_seeked(mpv)

        except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print(e)
                print('Reading error: {}'.format(str(e)))
                sys.exit()

            # We just did not receive anything
                continue

        except Exception as e:
            # Any other exception - something happened, exit
            print(e)
            print('Reading error: '.format(str(e)))
            sys.exit()

    mpv.terminate()
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()

def parse_config(parser, configfile):

    parser.read(configfile)
    IP = parser.get('connection', 'ip')
    PORT = parser.getint('connection', 'port')
    USERNAME = parser.get('connection', 'username')
    PASSWORD = parser.get('connection', 'password')
    return IP, PORT, USERNAME, PASSWORD

def initialize(parser, configfile):

    IP = input("IP: ")
    PASSWORD = input("Password: ")
    USERNAME = input("Username: ")
    parser['connection'] = {
        'ip': IP,
        'port': '51984',
        'username': USERNAME,
        'password': PASSWORD,
    }
    with open(configfile,"w") as f:
        parser.write(f)


def main():

    global KEY
    global HEADER_LENGTH
    global client_socket

    HEADER_LENGTH = 32
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE ="!DISCONNECT"
    

    configfolder = os.path.expanduser("~/.config/sync-mpv/")
    configfile = os.path.expanduser("~/.config/sync-mpv/sync-mpv.conf")

    parser = ConfigParser()

    if os.path.exists(configfolder):
        pass
    else:
        os.mkdir(configfolder)

    if os.path.exists(configfile):
        IP, PORT, USERNAME, PASSWORD = parse_config(parser, configfile)
    else:
        initialize(parser, configfile)
       
    IP, PORT, USERNAME, PASSWORD = parse_config(parser, configfile)

    KEY = hashlib.sha256(PASSWORD.encode()).digest()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to a given ip and port
    while True:
        try:
            client_socket.connect((IP, PORT))
            break
        except ConnectionRefusedError:
            print("\nEnter new IP if server IP has changed.\nLeave blank otherwise.\n")

            IP = input("IP: ")
            if IP == "":
                pass

    config = ConfigParser()
    config.read(configfile)
    config.set('connection','ip', '%s'%IP)

    with open(configfile,"w") as f:
        config.write(f)

    # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
    client_socket.setblocking(True)

    # Prepare username and header and send them
    # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well

    send(client_socket, USERNAME)

    handle_server(client_socket, (IP,PORT))
# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
if __name__ == "__main__":
    main()
