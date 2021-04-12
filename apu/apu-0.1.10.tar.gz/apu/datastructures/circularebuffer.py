"""
ringbuffer store data in a circulate memory
"""

from collections import deque

class CircularBuffer(deque):
    """ ringbuffer based on deque"""
    def __init__(self, size=1):
        super().__init__(maxlen=size)

    @property
    def average(self):
        """ calculate the avarage of all the componentes in the ringbuffer

        Returns:
            float: the avarage
        """
        if not isinstance(self, int) or not isinstance(self, float):
            raise TypeError("check if int or float")

        return sum(self)/len(self)
