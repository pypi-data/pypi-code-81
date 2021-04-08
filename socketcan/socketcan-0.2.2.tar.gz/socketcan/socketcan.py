""" Socketcan

    An abstraction to socketcan interface using python objects
    @author: Patrick Menschel (menschel.p@posteo.de)
    @license: GPL v3 
"""

import socket
import struct

from enum import IntEnum, IntFlag
from typing import Sequence, Union
from io import DEFAULT_BUFFER_SIZE
import logging

LOGGER = logging.getLogger("socketcan")


class BcmOpCodes(IntEnum):
    TX_SETUP = 1
    TX_DELETE = 2
    TX_READ = 3
    RX_SETUP = 5
    RX_DELETE = 6
    RX_READ = 7
    RX_STATUS = 10
    RX_TIMEOUT = 11
    RX_CHANGED = 12


class BCMFlags(IntFlag):
    SETTIMER = 0x01
    STARTTIMER = 0x02
    RX_FILTER_ID = 0x20


class CanFlags(IntFlag):
    CAN_ERR_FLAG = 0x20000000
    CAN_RTR_FLAG = 0x40000000
    CAN_EFF_FLAG = 0x80000000


class CanFdFlags(IntFlag):
    CAN_FD_BIT_RATE_SWITCH = 0x01
    CAN_FD_ERROR_STATE_INDICATOR = 0x02


def float_to_timeval(val):
    """ helper to split time value """
    sec = int(val)
    usec = int((val - sec) * 1000000)
    return sec, usec


def timeval_to_float(sec, usec):
    """ helper to merge time values """
    return sec + (usec / 1000000)


def combine_can_id_and_flags(can_id, flags=0):
    """ helper to combine can_id and flags"""
    return can_id | flags


def split_can_id_and_flags(can_id_with_flags):
    """ helper to split can_id from flags"""
    flags = CanFlags(can_id_with_flags & 0xE0000000)
    can_id = (can_id_with_flags & 0x1FFFFFFF)
    return can_id, flags


class CanFrame:
    """ A CAN frame or message, low level calls it frame, high level calls it a message
    
        @param can_id: the can bus id of the frame, integer in range 0-0x1FFFFFFF
        @param data: the data bytes of the frame
        @param flags: the flags, the 3 top bits in the MSB of the can_id
    """

    FORMAT = "IB3x8s"

    def __init__(self,
                 can_id: int,
                 data: bytes,
                 flags: CanFlags = 0,
                 ):
        LOGGER.debug("CanFrame creation with {0:08X} {1:08X} {2}".format(can_id, flags, data.hex()))
        self.can_id = can_id
        self.flags = flags
        if (can_id > 0x7FF) and not (CanFlags.CAN_EFF_FLAG & self.flags):
            # convenience function but at least log this mangling
            LOGGER.debug("CanFrame.__init__() adding CAN_EFF_FLAG for extended can_id {0:08X}".format(can_id))
            self.flags = self.flags | CanFlags.CAN_EFF_FLAG
        self.data = data

    def to_bytes(self):
        """ return the byte representation of the can frame that socketcan expects """
        data = self.data
        data.ljust(8)
        return struct.pack(self.FORMAT, combine_can_id_and_flags(self.can_id, self.flags), len(self.data), data)

    def __eq__(self, other):
        """ standard equality operation """
        return all((self.can_id == other.can_id,
                    self.flags == other.flags,
                    self.data == other.data
                    ))

    def __ne__(self, other):
        """ standard non equality operation """
        return not self.__eq__(other)

    @classmethod
    def from_bytes(cls, byte_repr):
        """ factory to create instance from bytes representation """
        assert len(byte_repr) == cls.get_size()
        can_id_with_flags, data_length, data = struct.unpack(cls.FORMAT, byte_repr)
        can_id, flags = split_can_id_and_flags(can_id_with_flags)
        LOGGER.debug("extracted flags {0:08X}".format(flags))
        return CanFrame(can_id=can_id,
                        flags=flags,
                        data=data[:data_length])

    @classmethod
    def get_size(cls):
        """ size getter """
        return struct.calcsize(cls.FORMAT)


class CanFdFrame(CanFrame):
    """
    A class to abstract a CAN FD Frame
    """

    FORMAT = "IBB2x64s"

    def __init__(self,
                 can_id: int,
                 data: bytes,
                 flags: CanFlags = 0,
                 fd_flags: CanFdFlags = CanFdFlags.CAN_FD_BIT_RATE_SWITCH):
        LOGGER.debug("CanFdFrame creation with {0:08X} {1:08X} {2}".format(can_id, flags, data.hex()))
        self.can_id = can_id
        self.flags = flags
        self.fd_flags = fd_flags
        if (can_id > 0x7FF) and not (CanFlags.CAN_EFF_FLAG & self.flags):
            # convenience function but at least log this mangling
            LOGGER.debug("CanFdFrame.__init__() adding CAN_EFF_FLAG for extended can_id {0:08X}".format(can_id))
            self.flags = self.flags | CanFlags.CAN_EFF_FLAG
        self.data = data

    def to_bytes(self):
        """ return the byte representation of the can fd frame that socketcan expects """
        data = self.data
        data.ljust(64)
        return struct.pack(self.FORMAT, combine_can_id_and_flags(self.can_id, self.flags), len(self.data),
                           self.fd_flags, data)

    def __eq__(self, other):
        """ standard equality operation """
        return all((self.can_id == other.can_id,
                    self.flags == other.flags,
                    self.fd_flags == other.fd_flags,
                    self.data == other.data
                    ))

    def __ne__(self, other):
        """ standard non equality operation """
        return not self.__eq__(other)

    @classmethod
    def from_bytes(cls, byte_repr):
        """ factory to create instance from bytes representation """
        assert len(byte_repr) == cls.get_size()
        can_id_with_flags, data_length, fd_flags, data = struct.unpack(cls.FORMAT, byte_repr)
        can_id, flags = split_can_id_and_flags(can_id_with_flags)
        LOGGER.debug("extracted flags {0:08X}".format(flags))
        return CanFdFrame(can_id=can_id,
                          flags=flags,
                          fd_flags=fd_flags,
                          data=data[:data_length])


class BcmMsg:
    """ Abstract the message to BCM socket
    
        For tx there are two use cases,
        1. a message to be sent with a defined interval for a defined number of times (count)
            populate opcode, flags, count, interval1, can_id, frame
        2. a message to be sent with a defined interval for the whole time the BcmSocket remains open
            populate opcode, flags, interval2, can_id, frame

        For rx there is X use cases,
        1. receive a message that is sent with a defined interval and be informed about timeout of this message
            populate opcode, flags, can_id, interval1

        @param opcode: operation code of / to BCM
        @param flags: flags of / to BCM
        @param count: a count
        @param interval1: in case of tx this is the time in between each count to transmit the message,
                          in case of rx, this is the timeout value at which RX_TIMEOUT is sent from BCM to user space
        @param interval2: in case of tx, this is the time in between each subsequent transmit after count has exceeded
                          in case of rx, this is a time to throttle down the flow of messages to user space
        @param can_id: of can message
               CAVEAT: THE CAN_FLAGS ARE PART OF CAN_ID HERE, e.g. long can id's are not recognized if flags are not set
                       and comparing the bcm can_id with the frame id fails because the flags have been excluded by
                       concept of CanFrame
        @param frames: an iterable of CanFrames
    """

    # this is a great hack, we force alignment to 8 byte boundary
    # by adding a zero length long long 
    FORMAT = "IIIllllII0q"

    def __init__(self,
                 opcode: BcmOpCodes,
                 flags: BCMFlags,
                 count: int,
                 interval1: float,
                 interval2: float,
                 can_id: int,
                 frames: Sequence[CanFrame],

                 ):
        self.opcode = opcode
        self.flags = flags
        self.count = count
        self.interval1 = interval1
        self.interval2 = interval2
        self.can_id = can_id
        self.frames = frames

    def to_bytes(self):
        """ return the byte representation of the bcm message that socketcan expects """
        interval1_seconds, interval1_microseconds = float_to_timeval(self.interval1)
        interval2_seconds, interval2_microseconds = float_to_timeval(self.interval2)
        byte_repr = bytearray()
        byte_repr.extend(struct.pack(self.FORMAT, self.opcode, self.flags,
                                     self.count, interval1_seconds, interval1_microseconds,
                                     interval2_seconds, interval2_microseconds, self.can_id,
                                     len(self.frames)))
        for frame in self.frames:
            byte_repr.extend(frame.to_bytes())

        return byte_repr

    def __eq__(self, other):
        """ standard equality operation """
        return all((self.opcode == other.opcode,
                    self.flags == other.flags,
                    self.count == other.count,
                    self.interval1 == other.interval1,
                    self.interval2 == other.interval2,
                    self.can_id == other.can_id,
                    self.frames == other.frames,
                    ))

    def __ne__(self, other):
        """ standard non equality operation """
        return not self.__eq__(other)

    @classmethod
    def from_bytes(cls, byte_repr: bytes):
        """ factory to create instance from bytes representation """
        opcode, flags, count, interval1_seconds, interval1_microseconds, interval2_seconds, interval2_microseconds, \
        can_id, number_of_frames = struct.unpack(cls.FORMAT, byte_repr[:cls.get_size()])
        interval1 = timeval_to_float(interval1_seconds, interval1_microseconds)
        interval2 = timeval_to_float(interval2_seconds, interval2_microseconds)
        frames = [CanFrame.from_bytes(byte_repr[idx:idx + CanFrame.get_size()])
                  for idx in range(cls.get_size(), len(byte_repr), CanFrame.get_size())]
        assert len(frames) == number_of_frames
        return BcmMsg(opcode=BcmOpCodes(opcode),
                      flags=BCMFlags(flags),
                      count=count,
                      interval1=interval1,
                      interval2=interval2,
                      can_id=can_id,
                      frames=frames,
                      )

    # @classmethod  # obsolete function
    # def get_nframes_from_bytes(cls, byte_repr: bytes):
    #     """ return the nframes value from a bcm_msg_head"""
    #     return struct.unpack(cls.FORMAT, byte_repr[:cls.get_size()])[-1]

    @classmethod
    def get_size(cls):
        """ size getter """
        return struct.calcsize(cls.FORMAT)


class CanRawSocket:
    """ A socket to raw CAN interface
    
        @param: interface name
    """

    def __init__(self, interface: str, use_can_fd: bool = True):
        self.s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        if use_can_fd:
            self.s.setsockopt(socket.SOL_CAN_RAW, socket.CAN_RAW_FD_FRAMES, True)
        self.s.bind((interface,))

    def __del__(self):
        self.s.close()

    def send(self, frame: Union[CanFrame, CanFdFrame]):
        """ send a CAN frame
        
            @param frame: a CanFrame 
        """
        return self.s.send(frame.to_bytes())

    def recv(self):
        """ receive a CAN frame """
        data = self.s.recv(DEFAULT_BUFFER_SIZE)
        try:
            frame = CanFrame.from_bytes(data)
        except AssertionError:
            LOGGER.error("Could not create CanFrame from buffer {0}".format(data.hex()))
            frame = None
        else:
            return frame

        if frame is None:
            try:
                frame = CanFdFrame.from_bytes(data)
            except AssertionError:
                LOGGER.error("Could not create CanFrame from buffer {0}".format(data.hex()))
                frame = None
        return frame


# Note: RX side is untested
class CanBcmSocket:
    """ A socket to broadcast manager
    
        @param: interface name
    """

    def __init__(self, interface: str):
        self.s = socket.socket(socket.PF_CAN, socket.SOCK_DGRAM, socket.CAN_BCM)
        self.s.connect((interface,))

    def __del__(self):
        self.s.close()

    def send(self, bcm: BcmMsg):
        """ send a bcm message to bcm socket
        
            @param bcm: A bcm message to be sent
        """
        return self.s.send(bcm.to_bytes())

    def recv(self) -> Union[BcmMsg, None]:
        """ receive a bcm message from bcm socket """
        data = self.s.recv(DEFAULT_BUFFER_SIZE)
        try:
            bcm = BcmMsg.from_bytes(data)
        except AssertionError:
            LOGGER.error("Could not create BcmMsg from buffer {0}".format(data.hex()))
            bcm = None
        return bcm

    def setup_cyclic_transmit(self,
                              frame: CanFrame,
                              interval: float):
        """ convenience function to abstract the socket interface
        
            @param frame: A CAN frame to be sent
            @param interval: the interval it should be sent  
        """
        bcm = BcmMsg(opcode=BcmOpCodes.TX_SETUP,
                     flags=(BCMFlags.SETTIMER | BCMFlags.STARTTIMER),
                     count=0,
                     interval1=0,
                     interval2=interval,
                     can_id=frame.can_id,
                     frames=[frame, ],
                     )
        return self.send(bcm)

    def setup_receive_filter(self,
                             frame: CanFrame,
                             timeout: float):
        """ convenience function to abstract the socket interface
        
            @param frame: A CAN frame to be received, the frame data is a filter
            @param timeout: the timeout for reception, should be more than the interval of the message
        """

        # Note: The can_id in bcm message is used for addressing the filter and can_id compare
        #       Therefore the can_id must contain the flags.
        can_id = frame.can_id
        can_flags = frame.flags
        if can_flags:
            can_id = can_id | can_flags

        bcm = BcmMsg(opcode=BcmOpCodes.RX_SETUP,
                     flags=(BCMFlags.SETTIMER | BCMFlags.STARTTIMER),
                     count=0,
                     interval1=timeout,
                     interval2=0,
                     can_id=can_id,
                     frames=[frame, ],
                     )
        return self.send(bcm)

    def get_receive_filter(self,
                           can_id: int,
                           can_flags: CanFlags = 0):
        """ convenience function to abstract the socket interface

            @param can_id: The CAN ID which the filter is registered for
            @param can_flags: The can flags that must be sit in the can_id because bcm expects that
        """
        # Note: The can_id in bcm message is used for addressing the filter and can_id compare
        #       Therefore the can_id must contain the flags.
        if (can_id > 0x7FF) and not (CanFlags.CAN_EFF_FLAG & can_flags):
            # convenience function but at least log this mangling
            LOGGER.debug(
                "CanBcmSocket.get_receive_filter() adding CAN_EFF_FLAG for extended can_id {0:08X}".format(can_id))
            can_flags = can_flags | CanFlags.CAN_EFF_FLAG

        bcm = BcmMsg(opcode=BcmOpCodes.RX_READ,
                     flags=BCMFlags(0),
                     count=0,
                     interval1=0,
                     interval2=0,
                     can_id=(can_id | can_flags),
                     frames=[],
                     )
        self.send(bcm)  # send the request to read the filter

        return self.recv()  # return the bcm message with the filter content


class CanIsoTpSocket:
    """ A socket to IsoTp
    
        @param interface: name
        @param rx_addr: the can_id that is received
        @param tx_addr: the can_id that is transmitted 
    """

    def __init__(self,
                 interface: str,
                 rx_addr: int,
                 tx_addr: int):

        if tx_addr > 0x7FF:
            tx_addr = combine_can_id_and_flags(tx_addr,CanFlags.CAN_EFF_FLAG)

        if rx_addr > 0x7FF:
            rx_addr = combine_can_id_and_flags(rx_addr, CanFlags.CAN_EFF_FLAG)

        self.s = socket.socket(socket.AF_CAN, socket.SOCK_DGRAM, socket.CAN_ISOTP)
        self.s.bind((interface, rx_addr, tx_addr))

    def __del__(self):
        self.s.close()

    def send(self, data: bytes):
        """ wrapper for send """
        return self.s.send(data)

    def recv(self, bufsize: int = DEFAULT_BUFFER_SIZE):
        """ wrapper for receive """
        return self.s.recv(bufsize)
