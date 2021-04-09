import os
import socket

if __name__ == '__main__':
    # RUN LOCALLY
    # os.system(f'ftsa report')

    # OR REMOTE (DOCKER)
    os.system(f'ftsa docker-report')
