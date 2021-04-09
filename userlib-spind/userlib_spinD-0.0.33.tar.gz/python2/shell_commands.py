

import subprocess
import os
import sys
from contextlib import contextmanager
import time
from tempfile import mkstemp
from shutil import move, copy2
from os import fdopen, remove


#======================================================================
# Lib for python - shell communication

# Moritz Goerzen
# 08.2018
# Spintronic Theory Kiel
#======================================================================









@contextmanager
def change_directory(newdir):
    #==================================================================
    # changes the directory in the following way:
    #
    # with change_directory(path_string):
    #    print os.getcwd()               # example line
    #
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)



def make_directory(directory):
    #==================================================================
    bashCommand = "mkdir " + str(directory)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()



def copy_folder(target, destination):
    #==================================================================
    bashCommand = "cp -r " + str(target) + " " + str(destination)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()




def copy_element(target, destination):
    #==================================================================
    bashCommand = "cp " + str(target) + " " + str(destination)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def copy_all_elements(targetdirectory, extension, destination):
    #==================================================================
    for filename in os.listdir(targetdirectory):
        if filename.endswith(extension):
            pathname = os.path.join(targetdirectory, filename)
            if os.path.isfile(pathname):
                copy2(pathname, destination)



def remove_element(filename):
    #==================================================================
    bashCommand = "rm " + str(filename)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()



def remove_folder(directory):
    #==================================================================
    bashCommand = "rm -r " + str(directory)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()




def call_bash(scriptname):
    #==================================================================
    # calls an .sh-script on linux desktop
    bashCommand = "bash " + str(scriptname)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()



def call_sbatch(scriptname):
    #==================================================================
    # calls an .sh-script on linux clusters
    bashCommand = "sbatch " + str(scriptname)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()



def call_python(scriptname):
    #==================================================================
    # calls an external python script
    bashCommand = "python " + str(scriptname)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()



def adjust_parameter(keyword, value, directory_file):
    #==================================================================
    # looks up "directory_file" for the given "keyword" and substitutes everything behind it
    # with "value"
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(directory_file) as old_file:
            for line in old_file:
                words = line.split()
                if not words :
                    pass
                elif words[0] == keyword :
                    new_file.write(line.replace(line, keyword + " " + str(value) + "\n"))
                else :
                    new_file.write(line)
    #Remove original file
    remove(directory_file)
    #Move new file
    move(abs_path, directory_file)


def set_jobname(name, directory_file):
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(directory_file) as file:
            for line in file :
                print 'new line'
                if line.startswith('#SBATCH'):
                    print 'starts with #SBATCH'
                    if line.split()[1].startswith('--job-name=') :
                        print 'is the correct line'
                        new_file.write(line.replace(line, '#SBATCH --job-name='+ name + "\n"))
                    else :
                        new_file.write(line)
                else :
                    new_file.write(line)
    #Remove original file
    remove(directory_file)
    #Move new file
    move(abs_path, directory_file)






def adjust_line_under_key(keyword, value, directory_file):
    #==================================================================
    # looks up "directory_file" for the given "keyword" and substitutes everything behind it
    # with "value"
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(directory_file) as old_file:
            for line in old_file:
                words = line.split()
                if not words :
                    pass
                elif words[0] == keyword :
                    new_file.write(line)
                    line2 = next(old_file)
                    new_file.write(line2.replace(line2, str(value) + "\n"))
                else :
                    new_file.write(line)
    #Remove original file
    remove(directory_file)
    #Move new file
    move(abs_path, directory_file)




def adjust_parameter_new_version(keyword, value, directory_file):
   #==================================================================
   # looks up "directory_file" for the given "keyword" and substitutes everything behind it
   # with "value"
   keyword_array=keyword.split()
   fh, abs_path = mkstemp()
   with fdopen(fh,'w') as new_file:
       with open(directory_file) as old_file:
           for line in old_file:
               words = line.split()
               # keywords can consist of more than one word. Every word has to match the corresponding element of the current line
               keyword_match=True
               set_space=True
               if len(keyword_array)==0 or len(keyword_array)>len(words):
                  keyword_match=False
               else:
                 for i in range(0,len(keyword_array)):
                    if keyword_array[i] not in words[i]:
                       keyword_match=False
                    elif keyword_array [i] != words [i]:
                       set_space=False
               if not words :
                   pass
               elif keyword_match==True :
                   if set_space==True:
                       new_file.write(line.replace(line, keyword + " " + str(value) + "\n"))
                   else:
                       new_file.write(line.replace(line, keyword + str(value) + "\n"))
               else :
                   new_file.write(line)
   #Remove original file
   remove(directory_file)
   #Move new file
   move(abs_path, directory_file)





def make_file(filename):
    #==================================================================
    # simple touch
    bashCommand = "touch " + str(filename)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()



def call_spin():
    #==================================================================
    # call SpinD_Kiel code lying on given directory
    #bashCommand = r" ~/code/SpinD/SpinD_Kiel/spin"
    bashCommand = r" ~/code/spind_kiel_v032020/spin"
    #bashCommand = r" ~/code/Sd_solver_HOI_gneb/spin"
    #subprocess.call(bashCommand, shell=True)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

def call_spin_():
    #==================================================================
    # call SpinD_Kiel code lying on given directory
    bashCommand = r" ~/code/SpinD/SpinD_Kiel/spin"
    #subprocess.call(bashCommand, shell=True)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()



def backuping_mkdir(directory):
    #==================================================================
    # copies folder to oldVersion if already exists and then creates new one as required
    if os.path.isdir(directory) :
        temp_directory = directory + "_backup"
        i = 1
        while os.path.isdir(temp_directory) :
            temp_directory = directory + "_backup" + str(i)
            i += 1
        print 'directory ' + '\"' + directory + '\" ' + 'already exists : backuping old version to ' + '\"' + temp_directory + '\"'
        copy_folder(directory, temp_directory)
        remove_folder(directory)
    make_directory(directory)
    time.sleep(1.0)



def backuping_touch(filename):
    #==================================================================
    # copies file to oldVersion if already exists and then creates new one as required
    if Path(filename).is_file() :
        temp_file = filename + "_backup"
        i = 1
        while Path(temp_file).is_file() :
            temp_file = filename + "_backup" + str(i)
            i += 1
        print 'file ' + '\"' + filename + '\" ' + 'already exists : backuping old version to ' + '\"' + temp_file + '\"'
        copy_element(filename, temp_file)
        remove_element(filename)
    make_file(filename)
    time.sleep(1.0)


def cluster():
    #==================================================================
    # reads the current machines name and returns the bool variable @cluster
    bashCommand = 'hostname'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output[0:2]=='rz':
        return True
    elif output[0:3]=='sh8' or output[0:7] == 'goerzen' or output[0:3] == 'cau':
        return False
    else:
        print 'Name =', output
        print 'ERROR at determining current machine. \n Please go to "shell_commands.py" and edit @cluster with the correct machine names '
        quit()
    return cl



def read_last_line(filename):
    #==================================================================
    num_lines = sum(1 for line in open(filename))
    with open(filename, 'rb') as f:
        if num_lines > 1 :
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            return f.readline().decode()
        else :
            return f.readline().decode()
