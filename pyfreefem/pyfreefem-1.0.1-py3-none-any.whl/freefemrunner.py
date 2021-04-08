# This file is part of PyFreeFEM.
#
# PyFreeFEM is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# PyFreeFEM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# A copy of the GNU General Public License is included below.
# For further information, see <http://www.gnu.org/licenses/>.
from os import path
from .preprocessor import Preprocessor
import os.path
import shutil
from .io import colored, display, tic, toc, exec2, ExecException
import tempfile



class FreeFemRunner:
    """A class to run a FreeFem code given by an interpreter or raw code."""

    def __init__(self, code, config=dict(), script_dir=None,
                 run_file=None, debug=0, plot=False, 
                 macro_files=None, verbosity=0):
        """
        Usage
        _____
        Load a single file .edp file
        >>> runner=FreeFemRunner('solveState.edp')

        Load a list of files (to be assembled consecutively)
        >>> runner=FreeFemRunner(['params.edp','solveState.edp'])

        Load a single file with an updated configuration
        >>> runner=FreeFemRunner('solveState.edp',{'ITER':'0010'})

        Load raw code
        >>> code = "mesh Th=square(10,10);"
            runner=FreeFemRunner(code)

        Load a pyfreefem.Preprocessor object
        >>> preproc = Preprocessor('solveState.edp')
            runner = FreeFemRunner(preproc)

        Then execute the code with `~FreeFemRunner.execute':
        >>> runner.execute();
            runner.execute({'Re':30}); # Update magic variable value

        It is possible to execute the code in parallel with ff-mpirun by using
        >>> # Run on 4 cpus with ff-mpirun -np 4
            runner.execute(ncpu=4); 
        >>> # Run on 1 cpu with ff-mpirun -np 1
            runner.execute(ncpu=1,with_mpi=1);

        Note that in that case, a magic variable 'WITH_MPI' is automatically
        assigned and set to 1, which is useful to make adaptations in the 
        source code, e.g. 
        ```
        IF WITH_MPI
        /* Instructions to do if the code is parallel */
        ELSE
        /* Instructions to do if the code is not parallel */
        int mpirank = 0; 
        int mpisize = 1;
        ENDIF
        ```

        Executing the code creates (by default) a temporary file which is
        to be executed by FreeFEM and which is removed after the python 
        execution. This behavior can be changed by using the
        `script_dir` and `run_file` arguments. 

        Note : for some usage, it is necessary to modify the
               FreeFem command. This can be achieved by
               updating the method `~FreeFemRunner.cmd`
               See pyfreefem/examples/hello_world_vglrun.py 

        Parameters 
        ----------

        code          : raw text code, instance of Preprocessor, or files

        config        : a default assignment of magic variables
                        which can be modified later on during the execute() 
                        operation.

        script_dir : where the running script will be written. If this 
                        argument is speficied, then script_dir is not 
                        deleted after the FreeFEM execution.

        run_file      : name of the written script

        debug         : tuning for verbosity. The FreeFEM command is not 
                        is displayed if debug>=1.
                        Details of the parsing operation are displayed if 
                        debug>=10.

        plot          : (default False). If set to True, then FreeFEM is run
                        with the graphical -wg option.

        macro_files   : list of enhanced .edp dependency files
                        (with meta-instructions)
                        which are also to be parsed and placed in the 
                        run folder of the final executable.

        verbosity     : verbosity level of FreeFem output
        """
        self.freefemFiles = dict()
        self.debug = int(debug)
        self.plot = plot
        self.verbosity = verbosity
        self.script_dir = script_dir
        self.run_file = run_file
        self.run_time = -1

        if isinstance(code, Preprocessor):
            self.preprocessor = code
        else:
            self.preprocessor = Preprocessor(code, config, debug=self.debug-10)
        self.config = config

        # create temporary directory if needed
        self.__context__ = False
        self.__tempdir__ = False

        if not self.run_file:
            self.run_file = "run.edp"

        self.macro_files = macro_files


    def write_edp_file(self, config=dict(), **kwargs):
        """
        Write the parsed .edp file in the running directory.

        Arguments
        ---------

            config      : a dictionary of magic variable which updates the 
                          default FreeFemRunner.config assignment.

            ncpu        : the number of CPUs for a run with ff-mpirun

            with_mpi    :  will run with ff-mpirun even if ncpu=1

            target_file : file name of the output .edp file to be written
        """
        ncpu = int(kwargs.get('ncpu', 1))
        self.config.update(config)
        if ncpu > 1 or kwargs.get('with_mpi', False):
            config.update({'WITH_MPI': 1})

        if not self.script_dir:
            self.__tempdir__ = True
            self.script_dir = tempfile.mkdtemp(prefix="pyfreefem_")

        if not os.path.exists(self.script_dir):
            os.makedirs(self.script_dir)
            display("Create "+self.script_dir, level=10, debug=self.debug,
                    color="magenta")
        target_file = path.join(self.script_dir, self.run_file)

        self.config.update({'SCRIPTDIR':self.script_dir})
        code = self.preprocessor.parse(config)

        f = open(target_file, "w")
        f.write(code)
        f.close()
        display("Write "+target_file, level=10, debug=self.debug,
                color="magenta")

        if self.macro_files:
            for mf in self.macro_files:
                file_name = os.path.split(mf)[1]
                with open(self.script_dir+"/"+file_name, "w") as f:
                    f.write(Preprocessor(mf, self.config, debug=self.debug-10).parse(config))
        return target_file

    def __enter__(self):
        self.__context__ = True
        if not self.script_dir:
            self.__tempdir__ = True
            self.script_dir = tempfile.mkdtemp(prefix="pyfreefem_")
        if not os.path.exists(self.script_dir):
            os.makedirs(self.script_dir)
            display("Create "+self.script_dir, level=10, debug=self.debug,
                    color="magenta")
        return self

    def __exit__(self, type, value, traceback):
        if self.__tempdir__:
            display("Remove "+self.script_dir, level=10, debug=self.debug,
                    color="magenta")
            exec2("rm -rf "+self.script_dir, level=10)


    def execute(self, config=dict(), **kwargs):
        """
        Parse with the input config, save the code in .edp file
        and call FreeFEM.

        Usage:
            >>> runner = FreeFemRunner('solveState.edp')
            runner.execute();
            runner.execute({"ITER" : "0024"});

        Options
        -------
        config    :  dictionary of updated magic variable values
                     Warning : a "SET" instruction in the .edp file
                     always has the precedence over the values specified
                     by `config`

        debug       :  execute the edp file with an updated level of verbosity

        target_file : change of location to write the .edp file.

        silent      : (default False) if set to True, there will be no standard 
                      output displayed in the shell (although it will still be 
                      returned in the output variables stdout, stderr and mix).

        Returns
        -------

        returncode   :  the return code of the FreeFEM process
        stdout       :  the standard output
        stderr       :  the standard error output
        mix          :  the integrality of the of the FreeFEM process output 

        """
        debug = kwargs.pop('debug', self.debug)
        target_file = self.write_edp_file(config, **kwargs)
        verbosity = max(self.verbosity,kwargs.get('verbosity',-1))
        silent = kwargs.get('silent', False) or verbosity < 0
        level = kwargs.pop('level',1)
        try:
            returncode, stdout, stderr, mix = \
                exec2(self.cmd(target_file, **kwargs),
                       debug=debug, level=level, silent=silent)
        except ExecException as e:
            display(e.args[0], level = 0, debug = 0)
            if max(self.verbosity,kwargs.get('verbosity',-1))<0:
                display('\n'.join(e.mix.splitlines()[-15:]), level=0, debug=0)
            e.args = []
            raise e

        if self.__tempdir__ and not self.__context__:
            display("Remove "+self.script_dir, level=10, debug=self.debug,
                    color="magenta")
            exec2("rm -rf "+self.script_dir, level=10)
        return returncode, stdout, stderr, mix


    def cmd(self, target_file, **kwargs):
        """Return the shell command that is to be run."""
        ncpu = kwargs.get('ncpu', 1)
        if ncpu > 1 or kwargs.get('with_mpi', False):
            cmd = f"ff-mpirun -np {ncpu}"
        else:
            cmd = "FreeFem++"
        cmd += " " + target_file
        if 'verbosity' in kwargs:
            cmd = cmd+" -v "+str(kwargs['verbosity'])
        elif self.verbosity != 1:
            cmd = cmd+" -v "+str(self.verbosity)
        if self.plot or kwargs.get('plot', False):
            cmd = cmd+" -wg"
        elif not kwargs.get('with_mpi', False):
            cmd += " -nw"
        return cmd
