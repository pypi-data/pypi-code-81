from PygFW.Data import DataContainer
from _thread import start_new_thread
from time import sleep


class Clock:

    def __init__(self, run_clock=True, initial_clock_ticks=1):

        self._clock = initial_clock_ticks

        self._run_clock = run_clock
        start_new_thread(self._start_, ())

    @property
    def fmilliseconds(self):

        return self._clock

    @property
    def milliseconds(self):
        return int(self.fmilliseconds)

    @property
    def fseconds(self):

        return self.fmilliseconds / 1000

    @property
    def seconds(self):

        return int(self.fseconds)

    @property
    def fminutes(self):

        return self.fseconds / 60

    @property
    def minutes(self):

        return int(self.fminutes)

    @property
    def fhours(self):

        return self.fminutes / 60

    @property
    def hours(self):

        return int(self.fhours)

    def tick(self, amount=1):

        self._clock += amount

    def _start_(self):

        while self._run_clock:

            sleep(.001)

            self.tick(1)

    def _stop_(self):

        self._run_clock = False

    def create_stamp(self):

        return f'<Clock Time Stamp (milliseconds={self.fmilliseconds}, seconds={self.fseconds}, minutes={self.fminutes}, hours={self.fhours})>', self.fmilliseconds, self.fseconds, self.fminutes, self.fhours


default_clock = Clock()


class VolatileObject:

    def __getitem__(self, data_tag):

        return self.mdt[data_tag]

    def __init__(self):

        self._mdt_container = DataContainer()
        self._object_uptime_clock = Clock()
        self._creation_time = default_clock.create_stamp()

    @property
    def mdt(self):

        return self._mdt_container

    @property
    def uptime(self):

        return self._object_uptime_clock

    @property
    def created_at(self):

        return self._creation_time
