from nmigen import Module, Signal, Cat
from nmigen.hdl.rec import Record
from nmigen.compat.sim import run_simulation
from nmigen.cli import rtlil, verilog
from nmigen.tools import flatten

class RecordSliceBug:

    def __init__(self):
        record_spec = [('src1', 16), ('src2', 16)]
        self.r = Record(record_spec)
        self.sig = Signal(32)
        self.flatrec = Cat(*flatten(self.r))
        self.sigslice = Signal(4)

    def elaborate(self, platform):
        m = Module()

        # XXX ok this way round!  except the graphviz is a dog's dinner mess
        # (due to the massive amount of bit-slicing)
        m.d.comb += self.sig.eq(self.flatrec)

        # this way round is what fails.  it will have the same extreme
        # level of bit-slicing.
        #m.d.comb += self.flatrec.eq(self.sig)
        m.d.comb += self.r.eq(self.sig)
        m.d.comb += self.sigslice.eq(Cat(self.r[2:4], self.r[18:20]))

        return m


def tbench(dut):

    yield dut.sig.eq(0x10002000)
    yield
    src1 = yield dut.r.src1
    src2 = yield dut.r.src2

    ss = yield dut.sigslice

    assert src1 == 0x2000
    assert src2 == 0x1000


######################################################################
# Unit Tests
######################################################################

if __name__ == '__main__':

    dut = RecordSliceBug()
    ports = [dut.sig, dut.r.src1, dut.r.src2]
    vl = rtlil.convert(dut, ports=ports)
    with open("test_recordslice.il", "w") as f:
        f.write(vl)
    vl = verilog.convert(dut, ports=ports)
    with open("test_recordslice.v", "w") as f:
        f.write(vl)
    run_simulation(dut, tbench(dut), vcd_name="test_recordslice.vcd")

