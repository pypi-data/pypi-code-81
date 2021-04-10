import socket
import threading

# import thread module
from _thread import *

print_lock = threading.Lock()

# thread function
def threaded(c, addr):
    c.send(("Thank you for connecting").encode())
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print("Bye")

            # lock released on exit
            # print_lock.release()
            break

        print("[+] %s:%d >>> %s [%d]" % (addr[0], addr[1], data.decode(), len(data)))

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        c.send(data)

    print("[-] Closing %s:%d" % (addr[0], addr[1]))
    c.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")

    port = 3004

    s.bind(("localhost", port))
    print("socket binded to %s" % (port))

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        # print_lock.acquire()
        print("Connected to :", addr[0], ":", addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c, addr))

    s.close()


if __name__ == "__main__":
    main()
