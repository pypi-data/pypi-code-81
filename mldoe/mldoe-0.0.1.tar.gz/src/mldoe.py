# -*-coding: utf-8-*-
"""
File defining the design (meta)class and the two classes:
- Two-level designs
- Mixed-level designs (four- and two-levels)
"""


class design():
    def __init__(self, n_runs):
        self.n_runs = n_runs
        pass

    def __repr__(self):
        return 'Design object'
