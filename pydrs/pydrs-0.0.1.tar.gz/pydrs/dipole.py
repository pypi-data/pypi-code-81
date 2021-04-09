from pydrs import SerialDRS

# TODO: Create a standard interface with the common power supplies methods.
# TODO: All power supplies need the same methods?
# TODO: Make a good use of inheritance and Object Oriented design
# TODO: Don't forget to handle all returns from serial interface
# TODO: Make a good use of exception handling

class Dipole:
    # TODO: Force user to pass initialization values in constructor.
    # TODO: Init values can be DCLINK voltage or whatever
    def __init__(self):
        try:
            self._drs = SerialDRS()
            self._drs.SetSlaveAdd(1)
        except RuntimeError:
            print("Erro ao instanciar SerialDRS")
    
    def turn_on_dclink(self):
        for i in range(2, 9, 2):
            self._drs.SetSlaveAdd(i)
            # TODO: Handle return from turn_on and possible exceptions
            self._drs.turn_on()
        self._drs.SetSlaveAdd(1)
    
    def close_loop_dclink(self):
        for i in range(2, 9, 2):
            self._drs.SetSlaveAdd(i)
            # TODO: Handle return from closed_loop and possible exceptions
            self._drs.closed_loop()
        self._drs.SetSlaveAdd(1)

    def set_dclink_voltage(self, val=0):
        #TODO: Check if loop is closed and raise an exception if in open loop.
        for i in range(2, 9, 2):
            self._drs.SetSlaveAdd(i)
            self._drs.set_slowref(val)
        self._drs.SetSlaveAdd(1)

    def turn_on_output(self):
        # TODO: Check if DCLINK is Ok and raise ex
        self._drs.turn_on()

    def close_loop_output(self):
        # TODO: Handle return from closed_loop and possible exceptions
        self._drs.closed_loop()