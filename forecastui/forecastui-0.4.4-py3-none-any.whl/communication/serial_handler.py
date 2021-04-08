from enum import Enum
import serial
import time
import threading
from queue import Queue
import struct
import sys
import os
from easyserial import ReadError, ChecksumError, Serial


class Type(Enum):
    LOG = 0x00
    ERROR = 0x01
    STX = 0x02
    ETX = 0x03
    HANDSHAKE_SYN = 0x04
    HANDSHAKE_ACK = 0x05
    DATA_REQ = 0x06
    DATA = 0x07
    MSG = 0x08


class ErrorType(Enum):
    OTHER = -1
    CHECKSUM = 0
    USER = 1
    MSG = 2


class Action(Enum):
    UNKNOWN = -1
    STANDBY = 0
    LOGGING = 1
    ERROR = 2
    REQ_PARAM = 3


class SerialHandler:

    def __init__(self, port, baudrate=921600):
        self.__serial = Serial(port, baudrate)
        self.__serial.timeout = 2
        self._run = True
        self._loopThread = threading.Thread(target=self.loop, args=(), daemon=True)
        self.__logsQ = Queue()
        self.__errorsQ = Queue()
        self._dataReqCallback = None
        self._statusCallback = None

    def __del__(self):
        print("Deleting serial handler... ", end="")
        print("Done!")

    def handshake(self):
        while self._run:
            self._statusCallback.update(action=Action.STANDBY.value)
            print("Trying the handshake... ", end="")
            synPkg = bytearray()
            synPkg.append(Type.STX.value)
            synPkg.append(Type.HANDSHAKE_SYN.value)
            synPkg.append(Type.ETX.value)
            self.__serial.flush()

            self.__serial.write_package(synPkg)
            print("Sent SYN... ", end="")
            self._statusCallback.update(ack=True, message="Establishing connection...")

            time.sleep(1)

            data = self.__serial.read(tries=1)

            if data is None:
                print("Read nothing.")
                continue

            if data[1] == Type.HANDSHAKE_ACK.value:
                print("Success!")
                self._statusCallback.update(synack=True, message="Connection established")
                break
            else:
                print("Received error, reset the board!")
                self._statusCallback.update(action = Action.ERROR.value, message="Received error, reset the board")
                time.sleep(1)

    def loop(self):
        self.__serial.open()
        self.handshake()
        self._statusCallback.update(handshake=True, action = Action.LOGGING.value, message="Executing control loop")
        self._statusCallback.timeout = 1

        while self._run:
            try:
                package_type, payload = self.__serial.read_package()
            except ReadError:
                continue
            except ChecksumError:
                self.__errorsQ.put((ErrorType.CHECKSUM.value, None))
                continue

            if package_type is None or payload is None:
                # Whether the serial crashed or the buffer sent no package
                continue

            if package_type == Type.LOG.value:
                try:
                    self.__logsQ.put(struct.unpack(
                        '<'+'f'*int(len(payload)/4), payload))
                    self._statusCallback.logssec += 1
                except struct.error as e:
                    error_string = "Error while unpacking data! The unpack string was "
                    error_string += "<" + "f"*int(len(payload)/4) + "and the length of the payload was: " + str(len(payload)) + "\n"
                    error_string += "Payload: [{}]\n".format(", ".join([hex(i) for i in payload]))
                    self.__errorsQ.put((ErrorType.OTHER.value, error_string))
                    continue

            elif package_type == Type.ERROR.value:
                try:
                    msg = struct.unpack('<' + 's' * len(payload), payload)
                except:
                    self.__errorsQ.put(ErrorType.OTHER.value, "Error in reading an user defined error message")
                    continue
                decoded_msg = ''
                for b in msg:
                    decoded_msg += b.decode('utf-8')
                self.__errorsQ.put((ErrorType.USER.value, decoded_msg))

            elif package_type == Type.MSG.value:
                try:
                    msg = struct.unpack('<' + 's' * len(payload), payload)
                except:
                    self.__errorsQ.put(ErrorType.OTHER.value, "Error in reading a message from the board")
                    continue
                decoded_msg = ""
                for b in msg:
                    decoded_msg += b.decode("utf-8")
                self.__errorsQ.put((ErrorType.MSG.value, decoded_msg))

            elif package_type == Type.DATA_REQ.value:
                # decoding the name of the data required
                msg = struct.unpack('<' + 'c' * len(payload), payload)
                decoded_msg = ''
                for b in msg:
                    decoded_msg += b.decode('utf-8')
                self._statusCallback.update(action = Action.REQ_PARAM.value, message="Requesting parameters")
                to_send = self._dataReqCallback(decoded_msg)
                self.__serial.write_float(Type.DATA.value, to_send)
                self._statusCallback.update(action = Action.LOGGING.value, message="Executing control loop")

            else:
                self.__errorsQ.put((ErrorType.OTHER.value, "Unknown package identifier {}\n".format(package_type)))


    def stop(self):
        # sending the response.
        print("\tInterrupting serial handler loop... ", end="")
        self._run = False
        self.__serial.write_float(Type.DATA.value, 0)
        self.__serial.close()
        print("Done!")
        print("\tInterrupting status callback... ", end="")
        self._statusCallback.stop()
        print("Done!")
        print("\tInterrupting data req. callback... ", end="")
        self._dataReqCallback.stop()
        print("Done!")
        print("\tInterrupting serial handler thread... ", end="")
        self._loopThread.join()
        print("Done!")

    def start(self):
        assert self._dataReqCallback is not None
        self._run = True
        self._loopThread = threading.Thread(target=self.loop, args=(), daemon=True)
        self._loopThread.start()

    def setDataReqCb(self, callback):
        self._dataReqCallback = callback

    def setStatusCb(self, callback):
        self._statusCallback = callback

    def getLog(self):
        return self.__logsQ.get(True, timeout=2)

    def getErr(self):
        return self.__errorsQ.get(True, timeout=2)
