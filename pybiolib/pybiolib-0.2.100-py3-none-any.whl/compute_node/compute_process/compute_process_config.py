CLIENT_PORT = 5005
DOCKER_SOCKET_PATH = 'unix://var/run/docker.sock'

# The default recv buffer size
DEFAULT_BUFFER_SIZE = 32768

# The amount of RAM (in MB) to provision the enclave. Half of it will become disk space.
MEMORY_TO_PROVISION_ENCLAVE = '26624'

# The amount of vCPUs to provision the enclave. This has to be atleast 2.
CPU_COUNT_TO_PROVISION_ENCLAVE = '2'
