from nmigen import Module, Signal, Mux
from nmigen.hdl.rec import Record
from nmigen.compat.sim import run_simulation
from nmigen.cli import verilog, rtlil

from nmigen_add_experiment import FPADDBasePipe

from random import randint

class Dummy:
    pass

def data_tuple():
        data = []
        for i in range(num_tests):
            i = Dummy()
            i.a = randint(0, 1<<16-1)
            i.b = randint(0, 1<<16-1)
            i.mid = randint(0, 1<<4-1)
            data.append(i)
        return data



def test5_resultfn(data_o, expected, i, o):
    res = (expected.a + expected.b, expected.mid)
    assert data_o == res, \
                "%d-%d data %s not match %s\n" \
                % (i, o, repr(data_o), repr(expected))


class Test5:
    def __init__(self, dut, resultfn, data=None):
        self.dut = dut
        self.resultfn = resultfn
        if data:
            self.data = data
        else:
            self.data = []
            for i in range(num_tests):
                self.data.append((randint(0, 1<<16-1), randint(0, 1<<16-1)))
        self.i = 0
        self.o = 0

    def send(self):
        while self.o != len(self.data):
            send_range = randint(0, 3)
            for j in range(randint(1,10)):
                if send_range == 0:
                    send = True
                else:
                    send = randint(0, send_range) != 0
                o_p_ready = yield self.dut.p.ready_o
                if not o_p_ready:
                    yield
                    continue
                if send and self.i != len(self.data):
                    yield self.dut.p.valid_i.eq(1)
                    for v in self.dut.set_input(self.data[self.i]):
                        yield v
                    self.i += 1
                else:
                    yield self.dut.p.valid_i.eq(0)
                yield

    def rcv(self):
        while self.o != len(self.data):
            stall_range = randint(0, 3)
            for j in range(randint(1,10)):
                stall = randint(0, stall_range) != 0
                yield self.dut.n.ready_i.eq(stall)
                yield
                o_n_valid = yield self.dut.n.valid_o
                i_n_ready = yield self.dut.n.ready_i
                if not o_n_valid or not i_n_ready:
                    continue
                z = yield self.dut.n.data_o.z
                mid = yield self.dut.n.data_o.mid
                data_o = (z, mid)
                self.resultfn(data_o, self.data[self.o], self.i, self.o)
                self.o += 1
                if self.o == len(self.data):
                    break


num_tests = 100

if __name__ == '__main__':
    print ("test 1")
    dut = FPADDBasePipe(16, 4)
    test = Test5(dut.pipe, test5_resultfn, data=data_tuple())
    run_simulation(dut, [test.send, test.rcv], vcd_name="test_fpaddpipe1.vcd")

    ports = [dut.pipe.p.valid_i, dut.pipe.n.ready_i,
             dut.pipe.n.valid_o, dut.pipe.p.ready_o] + \
             [dut.pipe.p.data_i.a, dut.pipe.p.data_i.b,
              dut.pipe.p.data_i.mid] + \
             [dut.pipe.n.data_o.z,
              dut.pipe.n.data_o.mid]

    vl = rtlil.convert(dut, ports=ports)
    with open("test_fpaddpipe1.il", "w") as f:
        f.write(vl)


