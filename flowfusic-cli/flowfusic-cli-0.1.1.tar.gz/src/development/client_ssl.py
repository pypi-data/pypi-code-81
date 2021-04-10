import pprint
import socket
import ssl


def Main():
    host = "api.gcp.flowfusic.com"
    port = 5000

    context = ssl.create_default_context()

    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
    conn.connect((host, port))

    cert = conn.getpeercert()
    pprint.pprint(cert)

    conn.send(("Auth very_secret_secret").encode())
    print("Auth from the server :", conn.recv(1024).decode())

    # message you send to server
    message = "shaurya says geeksforgeeks"
    while True:

        # message sent to server
        conn.send(message.encode("ascii"))

        # messaga received from server
        data = conn.recv(1024)

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
    conn.close()


if __name__ == "__main__":
    Main()
