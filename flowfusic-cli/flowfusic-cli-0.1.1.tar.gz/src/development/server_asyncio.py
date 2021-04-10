import asyncio
import ssl


def validateAuth(data):
    if data == "very_secret_secret":
        return True
    else:
        return False


def getPort():
    return 3004


async def pipe(reader, writer):
    try:
        while not reader.at_eof():
            writer.write(await reader.read(2048))
    finally:
        writer.close()


async def auth(reader, writer):
    addr = writer.get_extra_info("peername")
    isauth = False
    # listen for auth header:
    data = await reader.read(1024)
    while data:
        msg = data.decode()
        if msg[0:4] == "Auth":
            if validateAuth(msg[5:]):
                print("[+]", addr, "auth ok")
                isauth = True
                writer.write("auth_ok".encode())
                await writer.drain()
                break
            else:
                print("[-]", addr, "auth not ok")
                writer.write("auth_not_ok".encode())
                await writer.drain()
                break
        data = await reader.read(1024)
    return isauth


@asyncio.coroutine
async def handle_client(reader, writer):

    addrfrom = writer.get_extra_info("peername")
    isauth = await auth(reader, writer)

    if isauth:
        try:
            remote_reader, remote_writer = await asyncio.open_connection(
                "127.0.0.1", getPort()
            )
            pipe1 = pipe(reader, remote_writer)
            pipe2 = pipe(remote_reader, writer)
            addrto = remote_writer.get_extra_info("peername")

            print("[+] piping", addrfrom, "to", addrto)

            await asyncio.gather(pipe1, pipe2)

        except ConnectionResetError:
            pass

        finally:
            print("[-]", addrfrom, "to", addrto, "Close the connection")
            writer.close()
            remote_writer.close()

    else:
        print("[-]", addrfrom, "Close the connection")
        writer.close()


def setup_server():

    withSsl = False

    if withSsl:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain("./fullchain.pem", "./privkey.pem")
    else:
        context = None

    loop = asyncio.get_event_loop()
    coroutine = asyncio.start_server(handle_client, "", 5000, ssl=context, loop=loop)

    server = loop.run_until_complete(coroutine)
    print("Serving on {}".format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("Closing server...")
    server.close()
    loop.close()


if __name__ == "__main__":
    setup_server()
