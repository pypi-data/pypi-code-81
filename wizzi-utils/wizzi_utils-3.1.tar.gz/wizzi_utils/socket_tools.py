import socket
import numpy as np
from wizzi_utils import misc_tools


def open_server(server_address: tuple = ('localhost', 10000), ack: bool = True, tabs: int = 1) -> socket:
    if ack:
        print('{}Opening server on IP,PORT {}'.format(tabs * '\t', server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)
    return sock


def get_host_name(ack: bool = True, tabs: int = 1) -> str:
    """ :return: hostname """
    hostname = socket.gethostname()
    if ack:
        print("{}Computer Name: {}".format(tabs * '\t', hostname))
    return hostname


def get_ipv4(ack: bool = True, tabs: int = 1) -> str:
    """ :return ipv4 address of this computer """
    ipv4 = socket.gethostbyname(get_host_name(ack=True, tabs=0))
    if ack:
        print("{}Computer IP Address: {}".format(tabs * '\t', ipv4))
    return ipv4


def send_msg(connection: socket, buflen: int, data: str, msg_end: str) -> None:
    data_e = str.encode(data + msg_end)
    data_e_len = len(data_e)
    for i in range(0, data_e_len, buflen):
        chunk_i = data_e[i:i + buflen]
        connection.send(chunk_i)
    return


def receive_msg(connection: socket, buflen: int, msg_end: str) -> (str, int):
    data_in = ''
    saw_end_delimiter = False
    while not saw_end_delimiter:
        data_in += connection.recv(buflen).decode('utf-8')
        if not data_in:
            break  # empty transmission
        if data_in.endswith(msg_end):
            data_in = data_in.replace('$#$#', '')
            saw_end_delimiter = True

    # data_in = connection.recv(buflen).decode('utf-8')
    data_in_len = len(data_in)
    return data_in, data_in_len


def buffer_to_str(data: str, prefix: str, tabs: int = 1, max_chars: int = 100) -> str:
    """
    :param data:
    :param prefix:
    :param tabs:
    :param max_chars:
    :return:
    data = 'hi server, how you doing???'  # len(data)==27
    print(buffer_to_str(data, prefix='client1', tabs=0, max_chars=27))
    print(buffer_to_str(data, prefix='client1', tabs=0, max_chars=26))
    print(buffer_to_str(data, prefix='client1', tabs=1, max_chars=15))
    """
    data_len = len(data)
    data_chars = data_len + 1 if data_len <= max_chars else max_chars

    msg = '{}{}: {} (bytes sent={})'.format(tabs * '\t', prefix, data[:data_chars], data_len)
    if data_len > max_chars:
        msg += ' ... message is too long'
    return msg


def rounds_summary(times: list) -> None:
    """
    :param times:
    :return:
    times_ti = []
    for t in range(10):
        print('t={}:'.format(t))
        begin_timer_i = misc_tools.get_timer()
        # do_work of round t
        misc_tools.sleep(seconds=0.03)
        end_timer_i = misc_tools.get_timer()
        times_ti.append(end_timer_i - begin_timer_i)
        print('\tDONE round={}: total time={}'.format(t, misc_tools.get_timer_delta(begin_timer_i)))
    rounds_summary(times_ti)
    output:
    Rounds Summary:
        Total rounds = 10
        Total run time = 0.328 seconds
        Avg   run time = 0.033 seconds (std = 0.004)
        30.50 FPS
    """
    if len(times) > 0:  # try print time avg before exit
        print('\nRounds Summary:')
        print('\tTotal rounds = {}'.format(len(times)))
        print('\tTotal run time = {:.3f} seconds'.format(np.sum(times)))
        print('\tAvg   run time = {:.3f} seconds (std = {:.3f})'.format(np.mean(times), np.std(times)))
        if np.mean(times) > 0.0001:
            print('\t{:.2f} FPS'.format(1 / np.mean(times)))
    return


def main():
    return


if __name__ == '__main__':
    main()
