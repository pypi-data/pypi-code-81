import serial
import time

# Global Variables
ser = 0
ComPort = 'COM'


# Function to Initialize the Serial Port
def init_serial(commPort: int, baudrate: int):
    global ser
    ser = serial.Serial()
    ser.port = ComPort + str(commPort)
    ser.baudrate = baudrate
    ser.bytesize = 8
    ser.parity = 'N'
    ser.stopbits = 1
    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control

    # Specify the TimeOut in seconds, so that SerialPort doesn't hangs
    ser.timeout = 10
    ser.open()  # Opens SerialPort

    # print port open or closed
    if ser.isOpen():
        print('Open: ' + ser.portstr)


# Function Ends Here


def encode_command(message: str):
    temp = message + '\r\n'
    encoded_temp = str.encode(temp)
    ser.write(encoded_temp)

    respondbytes = ser.readline()  # Read from Serial Port
    print(respondbytes)
    decoded_temp = respondbytes.decode()
    print('Response :')
    print(decoded_temp)


def waitForResponse(header: str, footer: str):
    while True:
        print("inside while")
        time.sleep(0.2)
        temp = header + "QR" + footer
        encoded_temp = str.encode(temp)
        ser.write(encoded_temp)
        respond_bytes = ser.readline()
        print(respond_bytes)
        decoded_temp = respond_bytes.decode()
        print("Response for Q command:")
        print(decoded_temp)
        time.sleep(0.2)
        new_character = decoded_temp[2:3]
        print("print response bit")
        print(new_character)
        if new_character == '`':
            print("break")
            break


def executeCommand(pump, command, waitForPump=False):
    #pump.checkValidity()
    return send_command(pump.asciiAddress, command, waitForPump)


def send_command(pumpAddress: str, message: str, waitForPump=False):
    commandHeader = '/' + pumpAddress
    commandFooter = '\r\n'

    command = commandHeader + message + commandFooter
    print("Command: " + command)
    encoded_command = str.encode(command)
    ser.write(encoded_command)
    respondbytes2 = ser.readline()  # Read from Serial Port
    print(respondbytes2)
    response = respondbytes2.decode()
    print('Response :')
    print(response)

    if waitForPump:
        waitForResponse(commandHeader, commandFooter)

    return response

