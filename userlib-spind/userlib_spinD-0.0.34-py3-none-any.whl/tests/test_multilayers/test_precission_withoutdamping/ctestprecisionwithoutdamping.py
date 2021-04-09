# -*- coding: utf-8 -*-
r"""
Module contains classes which belong to testing the precision of two spins from different layers.
"""
from tests.itest import ITest
import python3.testsignatures as sign
from python3.write_inputs.cwrite_inputs import CWriteInput
from python3.shell_commands import call_spin, change_directory, writelog, cluster, call_sbatch
import time
from tests.test_multilayers.test_precission_withoutdamping.canalyzeprecisionwithoutdamping import \
    CAnalyzePrecisionWithoutDamping
from pathlib import Path


class CTestPrecisionWithoutDamping(ITest):
    r"""
    Test the precision of two spins from different layers.
    """
    @property
    def testsignature(self) -> int:
        r"""
        Returns:
            the testsignature of a test
        """
        return sign.MULTI_PRECISIONWITHOUTDAMPING

    def __init__(self, logfile: Path, cleanup: bool = True, interlayerinteraction: str = 'ab') -> None:
        r"""
        Initializes the test.

        Args:
            interlayerinteraction(str): Interlayer interaction type. It is possible to test within the same unit cell
            (J_ab, J_ac, J_bc) and between different unit cells (J_AA, J_AB, J_AC, J_BA, J_BB, J_BC, J_CA, J_CB, J_CC).
        """
        super().__init__(logfile=logfile, cleanup=cleanup)
        self._interaction = interlayerinteraction
        # interlayer exchange coupling in meV
        self._J = 1.0
        self.setup_input_files()
        self._analyzer = CAnalyzePrecisionWithoutDamping(logfile=logfile, J=self._J, tempdir=self.tempdir,
                                                         lowerline=self.lowerline, upperline=self.upperline)

    def __call__(self) -> bool:
        r"""
        Call the test:
        - Start the calculation
        - Call the analyzer
        - Do the clean up
        """
        with change_directory(self.tempdir):
            if not cluster():
                call_spin()
            else:
                call_sbatch('/work_beegfs/supas384/jobs/job_cau_agheinze.sh')
        while not (self.tempdir / 'SpinSTM_end.dat').is_file():
            time.sleep(0.2)

        l_result = self._analyzer()
        if l_result:
            writelog(self.logfile, message='Test Passed')
        else:
            writelog(self.logfile, message='Test Failed')
        writelog(self.logfile, '=' * 100)

        if self.cleanup:
            self.cleanup_test()

        return l_result

    def setup_input_files(self) -> None:
        r"""
        Setup the input files
        """
        self.write_inp()
        self.write_dyna()
        self.write_lattice()
        self.write_interlayer()
        self.write_simu()
        self.write_stmi()

    def write_stmi(self) -> None:
        r"""
        Writes the SpinSTMi.dat file
        """
        stmi = CWriteInput(file=self.tempdir / 'SpinSTMi.dat')
        stmi()
        if self._interaction in ['ab', 'AA']:
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 1.0 0.0 0.0 3.0')
            self.lowerline = 0
            self.upperline = 1
        elif self._interaction == 'bc':
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.5 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 1.0 0.0 0.0 3.0')
            self.lowerline = 1
            self.upperline = 2
        elif self._interaction == 'ac':
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.5 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 1.0 0.0 0.0 3.0')
            self.lowerline = 0
            self.upperline = 2
        elif self._interaction == 'AB':
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.5 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.5 1.0 0.0 0.0 3.0')
            self.lowerline = 0
            self.upperline = 3
        elif self._interaction == 'BA':
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.5 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 1.0 0.0 0.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.5 0.0 0.0 1.0 3.0')
            self.lowerline = 1
            self.upperline = 2
        elif self._interaction == 'BB':
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.5 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 1.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.5 1.0 0.0 0.0 3.0')
            self.lowerline = 1
            self.upperline = 3
        elif self._interaction == 'AC':
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.3 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.6 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.3 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.6 1.0 0.0 0.0 3.0')
            self.lowerline = 0
            self.upperline = 5
        elif self._interaction == 'BC':
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.3 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.6 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.3 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.6 1.0 0.0 0.0 3.0')
            self.lowerline = 1
            self.upperline = 5
        elif self._interaction == 'CA':
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.3 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.6 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 1.0 0.0 0.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.3 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.6 0.0 0.0 1.0 3.0')
            self.lowerline = 2
            self.upperline = 3
        elif self._interaction == 'CB':
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.3 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.6 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.3 1.0 0.0 0.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.6 0.0 0.0 1.0 3.0')
            self.lowerline = 2
            self.upperline = 4
        elif self._interaction == 'CC':
            stmi.appendline(key='', value=' 0.0 0.0 0.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.3 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 0.6 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.0 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.3 0.0 0.0 1.0 3.0')
            stmi.appendline(key='', value=' 0.0 0.0 1.6 1.0 0.0 0.0 3.0')
            self.lowerline = 2
            self.upperline = 5

    def write_dyna(self) -> None:
        r"""
        Writes the dyna.in file
        """
        dyna = CWriteInput(file=self.tempdir / 'dyna.in', integration='6', timestep='0.1', duration='10000',
                           damping='0.0')
        dyna()

    def write_lattice(self) -> None:
        r"""
        Writes the lattice.in file
        """
        if self._interaction == 'ab':
            lattice = CWriteInput(file=self.tempdir / 'lattice.in', Nsize='1 1 1', alat='1.0 1.0 1.0')
            lattice()
            lattice.appendmultilinevalues(key='lattice', values=['0.5 -0.86602540378 0.0', '0.5 0.86602540378 0.0',
                                                                 '0.0 0.0 1.0'])
            lattice.appendmultilinevalues(key='motif 2 atoms', values=['0.0 0.0 0.0 3.0', '0.0 0.0 1.0 3.0'])
        elif self._interaction == 'AA':
            lattice = CWriteInput(file=self.tempdir / 'lattice.in', Nsize='1 1 2', alat='1.0 1.0 1.0')
            lattice()
            lattice.appendmultilinevalues(key='lattice', values=['0.5 -0.86602540378 0.0', '0.5 0.86602540378 0.0',
                                                                 '0.0 0.0 1.0'])
            lattice.appendmultilinevalues(key='motif 1 atoms', values=['0.0 0.0 0.0 3.0'])
        elif self._interaction in ['ac','bc']:
            lattice = CWriteInput(file=self.tempdir / 'lattice.in', Nsize='1 1 1', alat='1.0 1.0 1.0')
            lattice()
            lattice.appendmultilinevalues(key='lattice', values=['0.5 -0.86602540378 0.0', '0.5 0.86602540378 0.0',
                                                                 '0.0 0.0 1.0'])
            lattice.appendmultilinevalues(key='motif 3 atoms', values=['0.0 0.0 0.0 3.0', '0.0 0.0 0.5 3.0',
                                                                       '0.0 0.0 1.0 3.0'])
        elif self._interaction in ['AB', 'BA', 'BB']:
            lattice = CWriteInput(file=self.tempdir / 'lattice.in', Nsize='1 1 2', alat='1.0 1.0 1.0')
            lattice()
            lattice.appendmultilinevalues(key='lattice', values=['0.5 -0.86602540378 0.0', '0.5 0.86602540378 0.0',
                                                                 '0.0 0.0 1.0'])
            lattice.appendmultilinevalues(key='motif 2 atoms', values=['0.0 0.0 0.0 3.0', '0.0 0.0 0.5 3.0'])
        elif self._interaction in ['AC', 'BC', 'CA', 'CB', 'CC']:
            lattice = CWriteInput(file=self.tempdir / 'lattice.in', Nsize='1 1 2', alat='1.0 1.0 1.0')
            lattice()
            lattice.appendmultilinevalues(key='lattice', values=['0.5 -0.86602540378 0.0', '0.5 0.86602540378 0.0',
                                                                 '0.0 0.0 1.0'])
            lattice.appendmultilinevalues(key='motif 3 atoms', values=['0.0 0.0 0.0 3.0', '0.0 0.0 0.3 3.0',
                                                                       '0.0 0.0 0.6 3.0'])

    def write_inp(self) -> None:
        r"""
        Writes the inp file
        """
        inp = CWriteInput(file=self.tempdir / 'inp', H_ext='0.0 0.0 0.0', J_1='0.0d-3', Periodic_log='.T. .T. .F.',
                          Gra_log='.T. 100')
        inp()

    def write_interlayer(self) -> None:
        r"""
        Writes the interlayer.in file
        """
        interlayer = CWriteInput(file=self.tempdir / 'interlayer.in')
        if self._interaction in ['ab','AA']:
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer()
        elif self._interaction == 'bc':
            interlayer.appendline(key='J_ab1', value='0.0d-3')
            interlayer.appendline(key='J_ac1', value='0.0d-3')
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer()
        elif self._interaction == 'ac':
            interlayer.appendline(key='J_ab1', value='0.0d-3')
            interlayer.appendline(key='J_bc1', value='0.0d-3')
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer()
        elif self._interaction == 'AB':
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer.appendline(key='J_ab1', value='0.0d-3')
            interlayer.appendline(key='J_AA1', value='0.0d-3')
            interlayer.appendline(key='J_BB1', value='0.0d-3')
            interlayer.appendline(key='J_BA1', value='0.0d-3')
            interlayer()
        elif self._interaction == 'BA':
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer.appendline(key='J_ab1', value='0.0d-3')
            interlayer.appendline(key='J_AA1', value='0.0d-3')
            interlayer.appendline(key='J_BB1', value='0.0d-3')
            interlayer.appendline(key='J_AB1', value='0.0d-3')
            interlayer()
        elif self._interaction == 'BB':
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer.appendline(key='J_ab1', value='0.0d-3')
            interlayer.appendline(key='J_AA1', value='0.0d-3')
            interlayer.appendline(key='J_BA1', value='0.0d-3')
            interlayer.appendline(key='J_AB1', value='0.0d-3')
            interlayer()
        elif self._interaction == 'AC':
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer.appendline(key='J_ab1', value='0.0d-3')
            interlayer.appendline(key='J_bc1', value='0.0d-3')
            interlayer.appendline(key='J_ac1', value='0.0d-3')
            interlayer.appendline(key='J_AA1', value='0.0d-3')
            interlayer.appendline(key='J_AB1', value='0.0d-3')
            interlayer.appendline(key='J_BA1', value='0.0d-3')
            interlayer.appendline(key='J_BB1', value='0.0d-3')
            interlayer.appendline(key='J_BC1', value='0.0d-3')
            interlayer.appendline(key='J_CA1', value='0.0d-3')
            interlayer.appendline(key='J_CB1', value='0.0d-3')
            interlayer.appendline(key='J_CC1', value='0.0d-3')
            interlayer()
        elif self._interaction == 'BC':
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer.appendline(key='J_ab1', value='0.0d-3')
            interlayer.appendline(key='J_bc1', value='0.0d-3')
            interlayer.appendline(key='J_ac1', value='0.0d-3')
            interlayer.appendline(key='J_AA1', value='0.0d-3')
            interlayer.appendline(key='J_AC1', value='0.0d-3')
            interlayer.appendline(key='J_AB1', value='0.0d-3')
            interlayer.appendline(key='J_BA1', value='0.0d-3')
            interlayer.appendline(key='J_BB1', value='0.0d-3')
            interlayer.appendline(key='J_CA1', value='0.0d-3')
            interlayer.appendline(key='J_CB1', value='0.0d-3')
            interlayer.appendline(key='J_CC1', value='0.0d-3')
            interlayer()
        elif self._interaction == 'CA':
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer.appendline(key='J_ab1', value='0.0d-3')
            interlayer.appendline(key='J_bc1', value='0.0d-3')
            interlayer.appendline(key='J_ac1', value='0.0d-3')
            interlayer.appendline(key='J_AA1', value='0.0d-3')
            interlayer.appendline(key='J_AC1', value='0.0d-3')
            interlayer.appendline(key='J_AB1', value='0.0d-3')
            interlayer.appendline(key='J_BA1', value='0.0d-3')
            interlayer.appendline(key='J_BB1', value='0.0d-3')
            interlayer.appendline(key='J_BC1', value='0.0d-3')
            interlayer.appendline(key='J_CB1', value='0.0d-3')
            interlayer.appendline(key='J_CC1', value='0.0d-3')
            interlayer()
        elif self._interaction == 'CB':
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer.appendline(key='J_ab1', value='0.0d-3')
            interlayer.appendline(key='J_bc1', value='0.0d-3')
            interlayer.appendline(key='J_ac1', value='0.0d-3')
            interlayer.appendline(key='J_AA1', value='0.0d-3')
            interlayer.appendline(key='J_AC1', value='0.0d-3')
            interlayer.appendline(key='J_AB1', value='0.0d-3')
            interlayer.appendline(key='J_BA1', value='0.0d-3')
            interlayer.appendline(key='J_BB1', value='0.0d-3')
            interlayer.appendline(key='J_BC1', value='0.0d-3')
            interlayer.appendline(key='J_CA1', value='0.0d-3')
            interlayer.appendline(key='J_CC1', value='0.0d-3')
            interlayer()
        elif self._interaction == 'CC':
            interlayer.appendline(key='J_' + self._interaction + '1', value=str(self._J) + 'd-3')
            interlayer.appendline(key='J_ab1', value='0.0d-3')
            interlayer.appendline(key='J_bc1', value='0.0d-3')
            interlayer.appendline(key='J_ac1', value='0.0d-3')
            interlayer.appendline(key='J_AA1', value='0.0d-3')
            interlayer.appendline(key='J_AC1', value='0.0d-3')
            interlayer.appendline(key='J_AB1', value='0.0d-3')
            interlayer.appendline(key='J_BA1', value='0.0d-3')
            interlayer.appendline(key='J_BB1', value='0.0d-3')
            interlayer.appendline(key='J_BC1', value='0.0d-3')
            interlayer.appendline(key='J_CA1', value='0.0d-3')
            interlayer.appendline(key='J_CB1', value='0.0d-3')
            interlayer()

    def write_simu(self) -> None:
        r"""
        Writes the simu.in file
        """
        simu = CWriteInput(file=self.tempdir / 'simu.in', i_sd='.T.')
        simu()

    def __repr__(self) -> str:
        r"""
        Returns:
            representation of test
        """
        return f'Testing precision of two spins coupled with interlayer exchange of type: {self._interaction} ...'
