from pysunspec_read.demo.read_sample import demo_read_tcp_to_file


def run():
    print("Starting")
    demo_read_tcp_to_file("192.168.1.110", "reading.json")


if __name__ == '__main__':
    run()
