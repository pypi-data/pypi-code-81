#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tcp Port Forwarding (Reverse Proxy)
# Author : WangYihang <wangyihanger@gmail.com>


import socket
import sys
import threading


def validateAuth(data):
    print("I've received key:", data)
    if data == "very_secret_secret":
        return True
    else:
        return False


def getPort():
    return 3004


def transfer(src, dst, direction):
    src_name = src.getsockname()
    src_address = src_name[0]
    src_port = src_name[1]
    dst_name = dst.getsockname()
    dst_address = dst_name[0]
    dst_port = dst_name[1]
    while True:
        buffer = src.recv(1024)
        if len(buffer) == 0:
            print("[-] No data received! Breaking...")
            break
        dst.send(buffer)
    print("[+] Closing connecions! [%s:%d]" % (src_address, src_port))
    # src.shutdown(socket.SHUT_RDWR)
    src.close()
    print("[+] Closing connecions! [%s:%d]" % (dst_address, dst_port))
    # dst.shutdown(socket.SHUT_RDWR)
    dst.close()


def auth(src, dst):

    auth = False
    # listen for auth header:
    while True:
        data = src.recv(1024).decode()
        print("data: ", data)
        if data[0:4] == "Auth":
            print("I have auth header")
            if validateAuth(data[5:]):
                auth = True
                src.send("auth_ok".encode())
                break
            else:
                src.send("auth_not_ok".encode())
                break

    if auth:
        remote_host = "localhost"
        remote_port = getPort()
        print(
            "[+] Trying to connect the REMOTE server [%s:%d]"
            % (remote_host, remote_port)
        )
        dst.connect((remote_host, remote_port))
        print("[+] Tunnel connected! Tranfering data...")

        threading.Thread(target=transfer, args=(dst, src, False)).start()
        threading.Thread(target=transfer, args=(src, dst, True)).start()
    else:
        print("Closing auth proxy")
        src.close()
        dst.close()


def server(local_host, local_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((local_host, local_port))
    server_socket.listen(16)
    print("[+] Server started [%s:%d]" % (local_host, local_port))
    while True:
        local_socket, local_address = server_socket.accept()
        print(local_socket)
        print(
            "[+] Detect connection from [%s:%s]" % (local_address[0], local_address[1])
        )
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        threading.Thread(target=auth, args=(local_socket, remote_socket)).start()

    print("[+] Releasing resources...")
    # remote_socket.shutdown(socket.SHUT_RDWR)
    remote_socket.close()
    # local_socket.shutdown(socket.SHUT_RDWR)
    local_socket.close()
    print("[+] Closing server...")
    server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
    print("[+] Server shuted down!")


def main():
    server("localhost", 3003)


if __name__ == "__main__":
    main()
