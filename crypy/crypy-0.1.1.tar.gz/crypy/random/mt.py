class MT19937:
    u = 11
    s, b = 7, 0x9d2c5680
    t, c = 15, 0xefc60000
    l = 18

    def __init__(self, seed: int, generated: list = None) -> None:
        self.index = 624
        if generated is not None and len(generated) >= 624:
            self.state = list(map(self.untemper, generated[-624:]))
        else:
            self.state = [0] * 624
            self.state[0] = seed & 0xffffffff
            for i in range(1, 624):
                self.state[i] = 0x6c078965 \
                                * (self.state[i - 1] ^ self.state[i - 1] >> 30) \
                                + i & 0xffffffff

    @staticmethod
    def untemper(y: int) -> int:
        y ^= y >> MT19937.l
        y ^= y << MT19937.t & MT19937.c
        for _ in range(7):
            y ^= y << MT19937.s & MT19937.b
        for _ in range(3):
            y ^= y >> MT19937.u
        return y

    @staticmethod
    def temper(y: int) -> int:
        y ^= y >> MT19937.u
        y ^= y << MT19937.s & MT19937.b
        y ^= y << MT19937.t & MT19937.c
        y ^= y >> MT19937.l
        return y

    def random(self) -> int:
        if self.index >= 624:
            self._twist()
        y = self.temper(self.state[self.index])
        self.index += 1
        return y

    def _twist(self) -> None:
        for i in range(624):
            y = (self.state[i] & 0x80000000) \
                + (self.state[(i + 1) % 624] & 0x7fffffff)
            self.state[i] = self.state[(i + 397) % 624] ^ y >> 1
            if y % 2 != 0:
                self.state[i] ^= 0x9908b0df
        self.index = 0
