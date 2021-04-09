import queue
import threading
import time
from typing import Callable
from enum import Enum, unique

from ..daq.daq_labjack import DAQLabJack

@unique
class Encoders(Enum):
    HALL = 0
    QEI = 1


class DAQCallback:

    def __init__(self, port_a: str, port_b: str, port_c: str, device: str = 'T7', connectionType: str = 'USB', id: str = 'ANY', daq: DAQLabJack = None):
        if daq == None:
            self.daq = DAQLabJack(device, connectionType, id)
        else:
            self.daq = daq
        self.port_a = port_a
        self.port_b = port_b
        self.port_c = port_c

    @staticmethod
    def print(h1: int, h2: int, h3: int):
        """
        Show a visualization of the QEI/Hall signals.
        Parameters
        ----------
        h1 : int
            Hall Phase 1 / QEI I
        h2 : int
            Hall Phase 2 / QEI B
        h3 : int
            Hall Phase 3 / QEI A
        """
        h1_repr = '|  ' if h1 == 0 else '  |'
        h2_repr = '|  ' if h2 == 0 else '  |'
        h3_repr = '|  ' if h3 == 0 else '  |'
        _output_string = f'{h3_repr}     {h2_repr}     {h1_repr}'
        print(_output_string)

    def write(self, a: int, b: int, c: int):
        """
        Write signals to DAQ.

        Parameters
        ----------
        a : int
            Hall Phase 1 / QEI I
        b : int
            Hall Phase 1 / QEI I
        c : int
            Hall Phase 1 / QEI I
        """
        self.daq.write([self.port_a, self.port_b, self.port_c], [a, b, c])


class Sanssouci:
    """
    SOmanet SEnsor SImulator -> SOSESI -> Sanssouci (the n is silent!)

    Very primitive QEI and HALL simulator. Can set a velocity (maximum velocity depends on speed of used DAQ)
    """
    SECONDS_PER_MINUTE: int = 60

    def __init__(self, output_callback: Callable, sensor: Encoders, resolution: int = 0, pole_pairs: int = 0):
        self.__sensor = sensor
        self.__resolution = resolution
        self.__pole_pairs = pole_pairs
        self.__cmd_queue = queue.Queue()
        self.__alive = threading.Event()
        self.__alive.set()
        self.__output_callback = output_callback
        self.__thread = None

        self.state = 0
        self.ticks = 0
        self.i = 0
        self.polarity = 0

    def __del__(self):
        self.close()

    def close(self):
        self.__alive.clear()
        if self.__thread:
            self.__thread.join()

    def _start_thread(self):
        """
        Starts the loop as thread.
        """
        fct = None
        if self.__sensor == Encoders.HALL:
            fct = self._hall
        elif self.__sensor == Encoders.QEI:
            fct = self._qei

        if fct is not None:
            self.__thread = threading.Thread(target=self._loop, args=(fct,))
            self.__thread.start()

    def _calc_timing(self, velocity: int) -> float:
        """
        Calculate loop time depending on velocity.

        Parameters
        ----------
        velocity : int
            Velocity in RPM.

        Returns
        -------
        float
            Loop time in seconds.
        """
        loop_time = 0.0
        if self.__sensor == Encoders.HALL:
            time_electric_turn = abs(self.SECONDS_PER_MINUTE / (velocity * self.__pole_pairs))
            loop_time = time_electric_turn / 6  # time for electrical 60°
        elif self.__sensor == Encoders.QEI:
            time_mechanical_turn = abs(self.SECONDS_PER_MINUTE / velocity)
            time_abi_tick = time_mechanical_turn / self.__resolution
            loop_time = time_abi_tick
        self.polarity = velocity / abs(velocity)

        return loop_time

    def _hall(self) -> (int, int, int):
        """
        Returns the phase states depending on virtual position of motor.

        Returns
        -------
        (int, int, int)
            H1, H2, H3
        """
        h1 = 0
        h2 = 0
        h3 = 0

        if self.state == 0:  # 0/360 degree
            h1 = 1
            h2 = 0
            h3 = 1
        elif self.state == 1:  # 60 degree
            h1 = 1
            h2 = 0
            h3 = 0
        elif self.state == 2:  # 120
            h1 = 1
            h2 = 1
            h3 = 0
        elif self.state == 3:  # 180
            h1 = 0
            h2 = 1
            h3 = 0
        elif self.state == 4:  # 240
            h1 = 0
            h2 = 1
            h3 = 1
        elif self.state == 5:  # 300
            h1 = 0
            h2 = 0
            h3 = 1

        if self.polarity > 0:
            self.state = (self.state + 1) % 6
        elif self.polarity < 0:
            self.state -= 1
            if self.state == -1:
                self.state = 5

        return h1, h2, h3

    def _qei(self) -> (int, int, int):
        """
        Returns the phase states depending on virtual position of motor.

        Returns
        -------
        (int, int, int)
            I, B, A
        """
        a = 0
        b = 0

        if self.state == 0:
            a = 0
            b = 1
        elif self.state == 1:
            a = 0
            b = 0
        elif self.state == 2:
            a = 1
            b = 0
        elif self.state == 3:
            a = 1
            b = 1

        if self.polarity > 0:
            self.state = (self.state + 1) % 4
            self.ticks = (self.ticks + 1) % self.__resolution
        elif self.polarity < 0:
            self.state -= 1
            if self.state == -1:
                self.state = 3
            self.ticks -= 1
            if self.ticks < 0:
                self.ticks = self.__resolution

        if self.i == 1 and self.state == 2:
            self.i = 0
        if self.ticks == 0 and self.state == 0:
            self.i = 1

        return self.i, b, a

    def _loop(self, sensor_callback: Callable):
        """
        Main loop, which writes new states to the callback DAQ function.

        Parameters
        ----------
        sensor_callback : Callable
            QEI or HALL state machine.
        """
        loop_time = 0

        while self.__alive.is_set():
            t0 = time.time()
            h1_i, h2_b, h3_a = sensor_callback()

            if not self.__cmd_queue.empty():
                loop_time = self.__cmd_queue.get_nowait()

            self.__output_callback(h1_i, h2_b, h3_a)  # some output write function
            t1 = time.time()
            td = t1 - t0  # time delta
            if (loop_time - td) > 0:
                time.sleep(loop_time - td)  # - t1 - t0)

    def set_velocity(self, velocity: int):
        """
        Set the velocity. Starts also the thread.

        Parameters
        ----------
        velocity : int
            Velocity in RPM.
        """
        if not self.__thread:
            self._start_thread()
        # Because of a typical sensor problem, velocity is always one RPM less
        if velocity > 0:
            velocity += 1
        elif velocity < 0:
            velocity -= 1
        loop_time = self._calc_timing(velocity)
        self.__cmd_queue.put(loop_time)


if __name__ == '__main__':
    import somanet_test_suite as sts

    print("Start Sanssouci")
    printer = DAQCallback('MIO2', 'MIO1', 'MIO0', daq=sts.DAQLabJack())
    """
    hall_gen = Sanssouci(printer.write, 'HALL', pole_pairs=7)
    hall_gen.set_velocity(100)
    #time.sleep(5)
    #hall_gen.set_velocity(-100)
    #time.sleep(5)
    #hall_gen.set_velocity(2000)
    #time.sleep(5)
    """
    # qei_gen = Sanssouci(printer.write, 'HALL', pole_pairs=7)
    qei_gen = Sanssouci(printer.write, Encoders.QEI, resolution=100)
    qei_gen.set_velocity(40)
    # time.sleep(5)
    # hall_gen.set_velocity(-100)
    # time.sleep(5)
    # hall_gen.set_velocity(2000)
    # time.sleep(5)
