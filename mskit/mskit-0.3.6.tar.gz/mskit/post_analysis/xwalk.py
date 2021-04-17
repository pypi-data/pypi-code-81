import os
import re
import time
from sys import argv


def extract_xwalk_cmd(xwalk_cmd):
    aa1 = re.findall('-aa1 (.+?) ', xwalk_cmd, re.I)[0]
    aa2 = re.findall('-aa2 (.+?) ', xwalk_cmd, re.I)[0]
    a1 = re.findall('-a1 (.+?) ', xwalk_cmd, re.I)[0]
    a2 = re.findall('-a2 (.+?) ', xwalk_cmd, re.I)[0]
    inter_intra = re.findall('-(inter|intra)', xwalk_cmd, re.I)
    inter_intra = inter_intra[0] if inter_intra else None
    max_length = re.findall('-max (\d+?)[> ]', xwalk_cmd, re.I)[0]
    return aa1, aa2, a1, a2, inter_intra, max_length


def read_command_file(cmd_file, pdb_name):
    cmd_list = []
    with open(os.path.abspath(cmd_file), 'r') as cmd_handle:
        for each_line in cmd_handle:
            each_cmd = each_line.strip('\n')
            if not each_cmd:
                continue
            aa1, aa2, a1, a2, inter_intra, maxlength = extract_xwalk_cmd(each_cmd)

            rearranged_cmd = 'java -Xmx1024m Xwalk -infile {}.pdb -aa1 {} -aa2 {} -a1 {} -a2 {}{} -max {} -bb >'.format(
                pdb_name, aa1, aa2, a1, a2, ' -{}'.format(inter_intra) if inter_intra else '', maxlength)
            out_filename = '{pdb_filename}-{aa1}_{aa2}_{a1}_{a2}{inter_intra}-{maxlength}.txt'.format(
                pdb_filename=pdb_name, aa1=aa1, aa2=aa2, a1=a1, a2=a2,
                inter_intra='-{}'.format(inter_intra) if inter_intra else '', maxlength=maxlength)

            cmd_list.append((rearranged_cmd, out_filename))
    return cmd_list


def xwalk_run(cmd_list, result_add):
    cmd_num = len(cmd_list)
    for cmd_series, _ in enumerate(cmd_list):
        rearranged_cmd, out_filename = _
        each_cmd = '{}"{}"'.format(rearranged_cmd, os.path.join(result_add, out_filename))
        print('{}/{} Now running {}'.format(cmd_series + 1, cmd_num, each_cmd))
        os.system(each_cmd)


def merge_result(result_add):
    result_file_list = os.listdir(result_add)
    file_num = len(result_file_list)
    with open(os.path.join(result_add, 'MergedIntra.txt'), 'w') as intra_handle, open(os.path.join(result_add, 'MergedInter.txt'), 'w') as inter_handle:
        for file_series, each_result in enumerate(result_file_list):
            print('{}/{} Merging {}'.format(file_series + 1, file_num, each_result))
            intra_handle.write(each_result + '\n')
            inter_handle.write(each_result + '\n')

            result_path = os.path.join(result_add, each_result)
            with open(result_path, 'r') as result_handle:
                for each_line in result_handle:
                    if not each_line.strip('\n'):
                        continue
                    split_line = each_line.split('\t')
                    first_site = split_line[2]
                    second_site = split_line[3]
                    if first_site.split('-')[2] == second_site.split('-')[2]:
                        intra_handle.write(each_line)
                    else:
                        inter_handle.write(each_line)
            intra_handle.write('\n')
            inter_handle.write('\n')


if __name__ == '__main__':
    pdb_file = argv[1]
    command_file = argv[2]
    if not pdb_file.lower().endswith('.pdb'):
        raise NameError('Input file {}'.format(pdb_file))
    pdb_filename = os.path.splitext(pdb_file)[0]
    work_address = os.path.dirname(os.path.abspath(__file__))
    start_time = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime())
    print('Start from {}'.format(start_time))
    result_address = os.path.join(work_address, 'XwalkProject-{}-{}'.format(pdb_filename, start_time))
    os.makedirs(result_address)
    processed_cmd = read_command_file(command_file, pdb_filename)
    xwalk_run(processed_cmd, result_address)
    merge_result(result_address)
    print('End at {}'.format(time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime())))
