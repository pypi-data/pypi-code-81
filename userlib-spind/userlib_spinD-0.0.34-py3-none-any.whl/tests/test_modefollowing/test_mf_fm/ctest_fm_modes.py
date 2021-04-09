# -*- coding: utf-8 -*-
r"""
The classes within this module are testing the behaviour of ferromagnetic magnon modes.
"""
from tests.itest import ITest
import python3.testsignatures as sign
from python3.write_inputs.cwrite_inputs import CWriteInput
from pathlib import Path
from python3.magnetisations import SpinLattice
from python3.visualizations import write_STM
from python3.shell_commands import *
from python3.write_inputs.cinvert_eigenvector import CInvertEigenvector
from tests.test_modefollowing.test_mf_fm.canalyze_fm_modes import CAnalyzeFmModes

class CTestFmModes(ITest):
    r"""
    Tests the correct behaviour of ferromagnetic modes. These modes are calculating with the mf-method for the system
    Pd(fcc)/Fe/Ir(111) for an external field of 4.0T. The fitted parabola can be compared with the corresponding eigen-
    value from the hessian, because magnon modes can be treated in good approximation as harmonic modes.
    """

    @property
    def testsignature(self) -> int:
        r"""
        Returns:
            the testsignature of a test
        """
        return sign.MONO_MF_FM_MODES

    def __init__(self, logfile: Path, cleanup: bool = True, lattice: int = 50, modenr: int = 1) -> None:
        r"""
        Initializes the test.

        Args:
            logfile(Path): logfile for the test. Will be used in initializing the abstract super class.
            cleanup(bool): whether to clean up temporary files or not.
            lattice(int):  size of the lattice. Default is 50. This will generate a 50x50x1 hexagonal lattice.
            modenr(int): number of mode which shall be tested
        """
        super().__init__(logfile=logfile, cleanup=cleanup)
        self.lattice = lattice
        self.modenr = modenr
        self._setup_input_files()
        self._analyzer = CAnalyzeFmModes(logfile=logfile, tempdir=self.tempdir, modenr=modenr)

    def __call__(self) -> bool:
        r"""
        Calls the testing. The procedure includes two steps:

        - Start the mode following procedure for the selected vector_init_index. The direction along the mode (+ or -)
        is random. Due to the fact that the magnon modes should behave identical left and right to the minimum it makes
        no difference which direction start. This direction is labeled arbitrary as p-direction (plus)

        - Start the mode following procedure again. But now set i_vector_init to True and load the first eigenvector of
        the previous calculation and invert this eigenvector. This direction will be called n-direction (minus)

        Returns a bool whether the test failed or passed.
        """
        # start p-direction
        with change_directory(self.tempdir):
            if not cluster():
                call_spin()
            else:
                call_sbatch('/work_beegfs/supas384/jobs/job_cau_agheinze.sh')
        while not (self.tempdir / 'spin_0100.dat').is_file():
            time.sleep(2)
        # save vt_energy.dat and eigenvalues from positive direction (This direction has information of the hessian of
        # the untranslated spin configuration, because here the eigenvalue before the first step is written out)
        copy_element(self.tempdir / 'vt_energy.dat', self.tempdir / 'vtp_energy.dat')
        copy_element(self.tempdir / 'vt_eig.dat', self.tempdir / 'vtp_eig.dat')
        # remove old input
        remove_element(self.tempdir / 'vt.in')
        # invert first ev
        CInvertEigenvector(vector_original=self.tempdir / 'vt_0000.dat')(outfile=self.tempdir / 'vt_0000_inverted.dat')
        # write new input
        self.write_vt(direction='n')
        # start n-direction
        with change_directory(self.tempdir):
            if not cluster():
                call_spin()
            else:
                call_sbatch('/work_beegfs/supas384/jobs/job_cau_agheinze.sh')
        while not (self.tempdir / 'spin_0100.dat').is_file():
            time.sleep(2)
        # save vt_energy.dat
        copy_element(self.tempdir / 'vt_energy.dat', self.tempdir / 'vtn_energy.dat')

        # Analyze the results ==========================================================================================
        l_result = self._analyzer()

        if l_result:
            writelog(self.logfile, message='Test Passed')
        else:
            writelog(self.logfile, message='Test Failed')
        writelog(self.logfile, '=' * 100)

        if self.cleanup:
            self.cleanup_test()

        return l_result

    def _setup_input_files(self) -> None:
        r"""
        Prepares input files within the temp-folder
        """
        self.write_inp()
        self.write_lattice()
        self.write_simu()
        self.write_stmi()
        self.write_vt()

    def write_inp(self) -> None:
        r"""
        Writes inp - file
        """
        inp = CWriteInput(file=self.tempdir / 'inp', H_ext='0.0 0.0 4.0',
                          J_1='14.4046d-3',
                          J_2='-2.48108d-3',
                          J_3='-2.68507d-3',
                          J_4='0.520605d-3',
                          J_5='0.73757d-3',
                          J_6='0.277615d-3',
                          J_7='0.160881d-3',
                          J_8='-0.57445d-3',
                          J_9='-0.212654d-3',
                          D_ani='-0.7d-3 0.0 0.0',
                          D_1='1.0d-3',
                          Periodic_log='.T. .T. .F.',
                          Gra_log='.T. 99')
        inp()

    def write_lattice(self) -> None:
        r"""
        Writes the lattice.in file
        """
        lattice = CWriteInput(file=self.tempdir / 'lattice.in',
                              Nsize=f'{self.lattice} {self.lattice} 1',
                              alat='1.0 1.0 1.0')
        lattice()
        lattice.appendmultilinevalues(key='lattice', values=['0.5 -0.86602540378 0.0', '0.5 0.86602540378 0.0',
                                                             '0.0 0.0 1.0'])
        lattice.appendmultilinevalues(key='motif 1 atoms', values=['0.0 0.0 0.0 3.0'])

    def write_simu(self) -> None:
        r"""
        Writes the simu.in file
        """
        simu = CWriteInput(file=self.tempdir / 'simu.in', i_vt='.T.')
        simu()

    def write_stmi(self) -> None:
        r"""
        Creates the SpinSTMi-file. This is a ferromangetic configuration of the defined lattice size.
        """
        SL = SpinLattice(size=self.lattice, key='hex', magmom=3.0)
        write_STM(SL, name=self.tempdir / 'SpinSTMi.dat')

    def write_vt(self, direction: str = 'p') -> None:
        r"""
        writes vt.in

        Args:
            direction(str): direction for the setup. Either p (plus) direction or n (minus) direction along the mode.
        """
        if direction == 'p':
            vt = CWriteInput(file=self.tempdir / 'vt.in',
                             translation_steps='100',
                             ds_norm='1.0d-3',
                             index_steps='10',
                             i_sym_identity='.T.',
                             i_sym_inversion='.T.',
                             i_sym_rotation='.F.',
                             i_vector_init='.F.',
                             i_mod_vec='.F.',
                             vec_init_index=str(self.modenr),
                             label='vtp'
                             )
        elif direction == 'n':
            vt = CWriteInput(file=self.tempdir / 'vt.in',
                             translation_steps='100',
                             ds_norm='1.0d-3',
                             index_steps='10',
                             i_sym_identity='.T.',
                             i_sym_inversion='.T.',
                             i_sym_rotation='.F.',
                             i_vector_init='.T.',
                             i_mod_vec='.F.',
                             vector_file='vt_0000_inverted.dat',
                             label='vtn'
                             )
        else:
            raise ValueError('Only direction p or n are valid.')
        vt()

    def __repr__(self) -> str:
        r"""
        Returns:
            representation of test
        """
        return f'Compare results of HTST with fitted parabola for magnon modes for the system Pd/Fe/Ir(111) at B=4.0T'
