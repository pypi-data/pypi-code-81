import socket


def Main():
    host = "api.gcp.flowfusic.com"
    port = 5000
    # host = '35.188.52.236'
    # port = 8080

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))
    # print('Received from the server :', s.recv(1024).decode())

    # message you send to server
    message = "shaurya says geeksforgeeks"
    while True:

        # message sent to server
        s.send(message.encode("ascii"))

        # messaga received from server
        data = s.recv(1024)

        # print the received message
        # here it would be a reverse of sent message
        print("Received from the server :", str(data.decode("ascii")))

        # ask the client whether he wants to continue
        ans = input("\nDo you want to continue(y/n) :")
        if ans == "y":
            continue
        else:
            break
    # close the connection
    s.close()


if __name__ == "__main__":
    Main()
