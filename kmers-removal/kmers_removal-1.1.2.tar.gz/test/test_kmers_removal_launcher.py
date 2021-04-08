""" I'm just doing a terminal test since I know most functions behave well already """

import os
import logging
import sys
import pytest
import subprocess

def call_process(cmd):
    processname = cmd.split()[0]
    logging.debug('[DEBUG] (call_process) Processname = {}'.format(processname))
    logging.debug('[DEBUG] (call_process) cmd = {}'.format(cmd))

    process = subprocess.run(cmd, shell=True,capture_output=True)

    std_output = process.stdout.decode('utf-8')     # This will also make us wait till the end of the process
    error_output = process.stderr.decode('utf-8')

    print(std_output)

    print(error_output)

    return std_output, error_output


def clean_testdir():
    testdir = os.path.dirname(os.path.realpath(__file__))
    current_dir_content = os.listdir(testdir)


    if "outputest.fa" in current_dir_content:
        os.remove('outputest.fa')
    if "testReport.txt" in current_dir_content:
        os.remove("testReport.txt")

def test_main():
    testdir = os.path.dirname(os.path.realpath(__file__))

    clean_testdir()

    cmd = "kmers_removal --fastaFile ./testfa.fa --kmerFile ./testkmers_allowed.txt --output outputest.fa --report testReport.txt --verbosity WARNING"
    HERE = os.getcwd()
    os.chdir(testdir)
    stdout, stderr = call_process(cmd)

    assert not "ERROR" in stderr

    truth_outputfa = open(os.path.join(os.getcwd(),"./truth/outputest.fa"),"r").read()
    truth_outputreport = open(os.path.join(os.getcwd(),"./truth/testReport.txt"),"r").read()

    obtained_outputfa = open(os.path.join(os.getcwd(),"outputest.fa"),"r").read()
    obtained_outputreport = open(os.path.join(os.getcwd(),"testReport.txt"),"r").read()

    assert truth_outputfa == obtained_outputfa
    assert truth_outputreport == obtained_outputreport

    print('SUCCESS')

    clean_testdir()
    os.chdir(HERE)


if __name__ == "__main__":
    _test_main()
