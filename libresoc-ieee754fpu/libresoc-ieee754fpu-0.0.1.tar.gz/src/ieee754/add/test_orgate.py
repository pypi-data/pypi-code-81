from nmigen import Module, Signal
from nmigen.compat.sim import run_simulation

class ORGate:
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.x = Signal()

    def elaborate(self, platform=None):

        m = Module()
        m.d.comb += self.x.eq(self.a | self.b)

        return m

dut = ORGate()

def check_case(a, b, x):
    yield dut.a.eq(a)
    yield dut.b.eq(b)
    yield

    assert (yield dut.x) == x

def testbench():
  yield from check_case(0, 0, 0)
  yield from check_case(0, 1, 1)
  yield from check_case(1, 0, 1)
  yield from check_case(1, 1, 1)

run_simulation(dut, testbench(), vcd_name="test_add.vcd")

