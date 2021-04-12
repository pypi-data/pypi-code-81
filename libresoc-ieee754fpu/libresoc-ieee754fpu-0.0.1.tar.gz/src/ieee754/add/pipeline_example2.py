""" Example 5: Making use of PyRTL and Introspection. """

from nmigen import Module, Signal
from nmigen.cli import main, verilog


from pipeline import SimplePipeline

class Adder:
    def __init__(self, width):
        self.a   = Signal(width)
        self.b   = Signal(width)
        self.o   = Signal(width)

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.o.eq(self.a + self.b)
        return m


class Subtractor:
    def __init__(self, width):
        self.a   = Signal(width)
        self.b   = Signal(width)
        self.o   = Signal(width)

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.o.eq(self.a - self.b)
        return m



class ModulePipelineExample(SimplePipeline):
    """ A very simple pipeline to show how registers are inferred. """

    def __init__(self, pipe):
        SimplePipeline.__init__(self, pipe)
        self._a = Signal(4)
        self._b = Signal(4)
        self._o = Signal(4)
        self._setup()

    def stage0(self):
        self.a = self._a
        self.b = self._b
        self.o = self._add.

    def stage1(self):
        self.a = self.o
        self.b = self.b

    def stage2(self):
        self._pipe.sync += self._loopbacka.eq(self.a)
        self._pipe.sync += self._loopbackb.eq(self.b)

class PipeModule:

    def __init__(self):
        self.m = Module()
        self.p = SimplePipelineExample(self.m.d)

        self.p._add = Adder(4)
        self.p._sub = Subtractor(4)

        self.m.submodules.add = self.p._add
        self.m.submodules.sub = self.p._sub

            self.add.a.eq(self.a),
            self.sub.a.eq(self.a),
            self.add.b.eq(self.b),
            self.sub.b.eq(self.b),


    def elaborate(self, platform=None):
        return self.m

if __name__ == "__main__":
    example = PipeModule()
    main(example, ports=[
                    example.p._loopback,
        ])

    print(verilog.convert(example, ports=[ 
               example.p._a, example.p._b, example._o
             ]))
