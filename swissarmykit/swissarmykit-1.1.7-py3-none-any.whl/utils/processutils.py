
import psutil

class ProcessUtils:

    @staticmethod
    def terminate_process(names:list = ('chromedriver.exe', 'chromedriver')):
        for process in psutil.process_iter():
            if process.name() in names:
                print('Process found. Terminating it.', names)
                process.terminate()

if __name__ == '__main__':
    p = ProcessUtils()
    p.terminate_process(['docsvw64.exe'])