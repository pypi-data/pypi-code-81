import re
import ast
import numpy as np
from .space import Space


class MultiDiscrete(Space):
    """A series of discrete action spaces

    The multi-discrete action space consists of a series of discrete action
    spaces with different number of actions in each. It is useful to represent
    game controllers or keyboards where each key can be represented as a
    discrete action space. It is parametrized by passing an array of positive
    integers specifying number of actions for each discrete action space.

    For example:

        MultiDiscrete([ 5, 2, 2 ])
    """

    _MULTI_DISCRETE_RE = re.compile(r"MultiDiscrete\(([^)]+)\)")

    def __init__(self, nvec):
        """Constructs a new multi-discrete action space

        :param list[int] nvec: Vector of counts of each categorical variable
        """

        assert (np.array(nvec) > 0).all(), "nvec (counts) have to be positive"
        self.nvec = np.asarray(nvec, dtype=np.int64)
        super(MultiDiscrete, self).__init__(self.nvec.shape, np.int64)

    def sample(self):
        return (
            self.np_random.random_sample(self.nvec.shape) * self.nvec
        ).astype(self.dtype)

    def contains(self, x):
        if isinstance(x, list):
            x = np.array(x)  # Promote list to array for contains check
        # if nvec is uint32 and space dtype is uint32,
        # then 0 <= x < self.nvec guarantees that x is within correct bounds
        # for space dtype (even though x does not have to be unsigned)
        return (0 <= x).all() and (x < self.nvec).all()

    def to_string(self):
        return "MultiDiscrete(%s)" % np.array2string(self.nvec, separator=", ")

    @classmethod
    def from_string(cls, s):
        complete_match = MultiDiscrete._MULTI_DISCRETE_RE.match(s)
        if not complete_match:
            raise RuntimeError(
                "String '%s' does not match '%s'"
                % (s, MultiDiscrete._MULTI_DISCRETE_RE)
            )

        inner_str = complete_match[1]
        nvec = np.array(ast.literal_eval(inner_str))
        return MultiDiscrete(nvec)

    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return isinstance(other, MultiDiscrete) and np.all(
            self.nvec == other.nvec
        )
