# -*- coding: utf-8 -*-
r"""
This module start the testing procedure for the monolayer mode following testing.
"""
from tests.test_modefollowing.test_mf_fm.ctest_fm_modes import CTestFmModes
from tests.test_modefollowing.test_mf_fm.canalyze_fm_modes import CAnalyzeFmModes
from pathlib import Path
from python3.shell_commands import writelog, startlogger

def main() -> None:
    r"""
    main program function
    """
    logfile = Path.cwd() / 'modefollowing_tests.log'
    startlogger(logfile)
    writelog(logfile, 'Perform monolayer modefollowing testing: ....')
    writelog(logfile, '#' * 100)
    #CAnalyzeFmModes(logfile=logfile,tempdir=Path.cwd() / '4_temp_',modenr=1)()
    l_test = CTestFmModes(logfile=logfile, cleanup=False, lattice=25, modenr=1)
    writelog(logfile, message=repr(l_test))
    result = l_test()


if __name__ == "__main__":
    main()