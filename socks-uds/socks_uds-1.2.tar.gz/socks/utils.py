__all__ = (
    'check_either',
    'start_tls',
)

import asyncio
import ssl


def check_either(first, second):
    def check_good(arg):
        if type(arg) is not tuple:
            if arg:
                return True, True
            else:
                return False, False
        else:
            return all(arg), any(arg)

    fg_all, fg_any = check_good(first)
    sg_all, sg_any = check_good(second)
    if fg_all and not sg_any:
        return True
    if sg_all and not fg_any:
        return True
    return False


async def start_tls(domain_name, transport, ssl_context=None):
    loop = asyncio.get_running_loop()
    ctx = ssl_context or ssl.create_default_context()
    reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(reader)
    new_transport = await loop.start_tls(transport, protocol, sslcontext=ctx, server_hostname=domain_name)
    # https://github.com/encode/httpcore/blob/4b662b5c42378a61e54d673b4c949420102379f5/httpcore/_backends/asyncio.py#L123
    protocol.connection_made(new_transport)
    writer = asyncio.StreamWriter(new_transport, protocol, reader, loop)
    return reader, writer


