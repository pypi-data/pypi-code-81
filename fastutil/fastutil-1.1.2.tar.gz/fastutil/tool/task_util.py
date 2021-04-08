import os
import argparse


def kill_task():
    parser = argparse.ArgumentParser(description='杀掉任务')
    parser.add_argument('name', nargs='*', help='进程grep标记')
    parser.add_argument('-s', '--signal', default='TERM', help='信号')
    args = parser.parse_args()
    name = ' '.join(args.name)
    if not name:
        print('please input task name')
        return
    cmd = """
    if ps aux | grep '%s' |grep -v 'grep';then
        ps aux | grep '%s' |grep -v 'grep' | awk '{print $2}' | xargs kill -%s
    fi
    """ % (name, name, args.signal)
    os.system(cmd)
