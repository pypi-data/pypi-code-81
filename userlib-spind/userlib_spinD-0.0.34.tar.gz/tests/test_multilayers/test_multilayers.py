# -*- coding: utf-8 -*-
r"""
This script starts the test procedures for multilayer. Make sure that you are using the correct version of the SpinD-
dynamics code since multilayer are relatively new (~2019).
"""
from tests.test_multilayers.test_precission_withoutdamping.ctestprecisionwithoutdamping import \
    CTestPrecisionWithoutDamping
from python3.shell_commands import writelog, startlogger
from pathlib import Path


def main() -> None:
    r"""
    Main test routine:

    - Test precision frequency for two spins from different layers coupled via different types of interlayer exchange:
        [ab, bc, ac, AA, AB, AC]
    """
    interlayerinteraction=['ab', 'bc', 'ac', 'AA', 'AB', 'AC', 'BA', 'BB', 'BC', 'CA', 'CB', 'CC']

    logfile = Path.cwd() / 'multilayer_tests.log'
    startlogger(logfile)
    writelog(logfile, 'Perform multilayer testing: ....')
    writelog(logfile, '#' * 100)
    writelog(logfile,
             'Testing precision of two spins from different layers coupled via interlayer ex. (without damping):')
    for inter in interlayerinteraction:
        writelog(logfile, '=' * 100)
        l_test = CTestPrecisionWithoutDamping(logfile=logfile, cleanup=True, interlayerinteraction=inter)
        writelog(logfile, message=repr(l_test))
        result = l_test()


if __name__ == "__main__":
    main()
