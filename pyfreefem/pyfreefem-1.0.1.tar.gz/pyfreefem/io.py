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
import scipy.sparse as sp
import numpy as np
import time
import sys
import subprocess
import threading
import queue

try:
    import colored as col

    def colored(text, color=None, attr=None):
        if color:
            text = col.stylize(text, col.fg(color))
        if attr:
            text = col.stylize(text, col.attr(attr))
        return text
except:
    def colored(text, color=None, attr=None):
        return text


def display(message, level=0, debug=0, color=None, attr=None, end='\n',
            flag=None):
    """ Display function with tunable level of verbosity

    INPUTS
    ------

    message        :   text to be printed
    level          :   level of importance of the message; will be actually 
                       printed if debug >= level
    debug          :   current verbosity level
    color, attr    :   formattings with the `colored` package
    end            :   if set to '', will remove the final line carriage return
    flag           :   an extra indicator equal to None, 'stdout' or 'stderr',
                       the last two indicating that the text 
                       passed to display comes from the standard output or 
                       or error of a shell command. 
                       Useful if display is overrided.
    """
    if color or attr:
        message = colored(message, color, attr)
    if debug >= level:
        print(message, end=end, flush=True)

tclock = dict()
def tic(ref=0):
    global tclock
    tclock[ref] = time.time()

def toc(ref=0):
    global tclock
    return format(time.time()-tclock[ref],"0.2f")+"s"

class ExecException(Exception):
    def __init__(self, message, returncode, stdout, stderr, mix):
        super().__init__(message)
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.mix = mix

def readFFArray(ffarray):
    """
    Read an array stored in the file `ffarray` created by FreeFem++.
    For instance, if an .edp file has run
    ```
        real[int] table = [1, 2, 3, 4, 5];
        {
            ifstream f("file.gp");
            f << table;
        }
    ```
    Then
    >>> readFFArray("file.gp") 

    returns the numpy array [1, 2, 3, 4, 5]
    """
    with open(ffarray, "r") as f:
        return np.asarray([float(x) for line in f.readlines()[1:]
                           for x in line.split()])


def writeFFArray(A: np.array, fileName):
    """
    Store a numpy array into a FreeFEM array file

    Input
    _____

    A         :  a numpy array
    fileName  :  the file in which the array will be saved
    """
    text = f"{len(A)}\t\n"
    lines = [A[5*k:5*(k+1)] for k in range(0, int(np.ceil(len(A)/5)))]
    for line in lines:
        text += ''.join([f"\t  {x}" for x in line])+"\n"
    text = text[:-1]+"\t"
    with open(fileName, "w") as f:
        f.write(text)


def writeFFMatrix(A, fileName):
    """
    Convert a scipy sparse matrix to a FreeFEM sparse matrix file

    Input
    -----

    A        : a scipy sparse matrix or a numpy dense matrix
    fileName : the file in which the sparse matrix will be saved

    """
    if isinstance(A,np.ndarray):
        preamble = " ".join(map(str,A.shape))+"\t\n"
        preamble += "\n".join(["\t   "+"   ".join(map(str,line)) for line in A.tolist()])
        preamble += "\n\t"
    else:
        (I, J, V) = sp.find(A)
        (n, m) = A.shape
        nnz = A.nnz
        preamble = f"#  HashMatrix Matrix (COO) 0x2d90200\n"
        preamble += "#    n       m        nnz     half     fortran   state  \n"
        preamble += f"{n} {m} {nnz} 0 0 0 0 \n"
        lines = [f"     {i}     {j} {d}" for (i, j, d) in zip(I, J, V)]
        preamble = preamble+"\n".join(lines)
        preamble += "\n"
    with open(fileName, "w") as f:
        f.write(preamble)


def readFFMatrix(ffmatrix):
    """
    Read a matrix stored in the file `ffmatrix` created by FreeFEM.
    For instance, if an .edp file has run 
    ```
        matrix table = [[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]];
        {
            ifstream f("file.gp");
            f << table;
        }
    ```
    Then
    >>> readFFMatrix("file.gp") 

    returns the numpy matrix [[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]].
    """
    with open(ffmatrix, 'r') as f:
        lines = f.readlines()
    i = []
    j = []
    data = []
    if len(lines[0].strip().split())==2:
        shape = tuple([int(x) for x in lines[0].strip().split()])
        data = [line.strip().split() for line in lines[1:shape[0]+1]]
        return np.asarray(data, dtype=float)
    elif lines[0].startswith('#  HashMatrix'):
        shape = tuple([int(x) for x in lines[2].strip().split()[:2]])
        I,J,data = list(zip(*[line.strip().split() for line in lines[3:]]))
        I = list(map(int,I))
        J = list(map(int,J))
        data=list(map(float,data))
        return sp.csc_matrix((data, (I,J)),shape=shape)
    else:
        for (k, line) in enumerate(lines[4:]):
            i.append(int(line.split()[0])-1)
            j.append(int(line.split()[1])-1)
            data.append(float(line.split()[2]))
    return sp.csc_matrix((data, (i, j)))

def enqueue_stream(stream, queue, type):
    for line in iter(stream.readline, b''):
        queue.put(str(type) + line.decode('utf-8', errors='replace'))
    stream.close()


def enqueue_process(process, queue):
    process.wait()
    queue.put('x')

def exec2(cmd, **kwargs):
    """ Interface with subprocess.Popen """
    debug = kwargs.pop('debug', 0)
    level = kwargs.pop('level', 1)
    silent = kwargs.pop('silent', True)
    display(colored(cmd, color="yellow"), level=level, debug=debug, end='',
            flag='shell')
    # Put a line break to separate from the stdout 
    if not silent:
        display("",level=level,debug=debug,flag='')
    tic(121)
    proc = subprocess.Popen("stdbuf -oL "+cmd,shell=True,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE
                            )
    q = queue.Queue()
    to = threading.Thread(target=enqueue_stream, args=(proc.stdout, q,1))
    te = threading.Thread(target=enqueue_stream, args=(proc.stderr, q,2))
    tp = threading.Thread(target=enqueue_process, args=(proc, q))
    te.start()
    to.start()
    tp.start()

    stdout = "" 
    stderr = "" 
    mix = "" 
    while True:
        line = q.get()
        if line[0] == 'x':
            break
        if line[0] == '1':
            line = line[1:]
            stdout += line
            mix += line 
            if not silent:
                display(line,end='',flag='stdout')
        if line[0] == '2':
            line = line[1:]
            stderr += line
            mix += line 
            if not silent:
                display(line,attr="dim",end='',flag='stderr')
    tp.join()
    te.join()
    to.join()
    if mix and not silent:
        if not mix.endswith('\n'):
            display("",level,debug)
        display("Finished in",level,debug,color="cyan",end="",flag="")
    display(' ('+toc(121)+')', level=level, debug=debug,color="cyan",
            flag="time")

    if proc.returncode != 0:
        raise ExecException('Error : the process "'
                        + colored(cmd, "red")
                        + '" failed with return code '+str(proc.returncode)
                        + ".",proc.returncode,stdout,stderr,mix)
    return proc.returncode, stdout, stderr, mix
