import threading


class MyThread(threading.Thread):
    def __init__(self, name):
        """
        :param name: 线程名
        """
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print(f"线程 {self.name} 运行中")
