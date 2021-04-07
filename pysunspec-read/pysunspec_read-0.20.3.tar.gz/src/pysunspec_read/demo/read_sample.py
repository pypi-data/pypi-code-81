import logging
import sys

from pysunspec_read.connect_options import ConnectOptions, ConnectOptionsTcp
from pysunspec_read.output_options import OutputOptions
from pysunspec_read.read_to_output import read_with_clean

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.info("****************************")
logger.info("*         Starting         *")
logger.info("****************************")


def demo_read_tcp(ip_address: str):
    print("Starting demo reading from {}".format(ip_address))
    logger.info("Checking logging")
    if len(sys.argv) > 1:
        logger.info("using IP address from command line: {}".format(sys.argv[1]))
        ip_address = sys.argv[1]

    read_with_clean(connect_options=ConnectOptions(tcp=ConnectOptionsTcp(ip_address=ip_address)),
                    output_options=OutputOptions(save_reading=False, log_reading=True,
                                                 add_timestamp_to_reading=True))


def demo_read_tcp_to_file(ip_address: str, file_path: str):
    print("Starting demo reading from {} to file {}".format(ip_address, file_path))
    logger.info("Checking logging")
    if len(sys.argv) > 2:
        logger.info("using IP address and file {} from command line: {}".format(sys.argv[1], sys.argv[2]))
        ip_address = sys.argv[1]
        file_path = sys.argv[2]

    read_with_clean(connect_options=ConnectOptions(tcp=ConnectOptionsTcp(ip_address=ip_address)),
                    output_options=OutputOptions(save_reading=True, output_file_path=file_path, log_reading=True,
                                                 add_timestamp_to_reading=True))


def usage():
    print("For a demo reading, call instead to demo_ip.py")


if __name__ == '__main__':
    usage()
