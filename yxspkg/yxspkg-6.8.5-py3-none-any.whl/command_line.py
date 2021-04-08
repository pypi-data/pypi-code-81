import sys
import importlib
def main():
    command_dict = {
        'md5':         'yxspkg.md5',
        'fafa-excel':  'yxspkg.fafa_excel',
        'songzigif':   'yxspkg.songzgif.gif',
        'songziviewer':'yxspkg.songziviewer',
        'm3u8':        'yxspkg.m3u8',
        'server':      'yxspkg.file_server.server',
        'video2html':  'yxspkg.video2html',
        'getdata':     'yxspkg.getdata.getdata_qt',
        'convert_url': 'yxspkg.convert_url',
        'image':       'yxspkg.image.image_operator',
        'video':       'yxspkg.video.video_operator',
        'samefile':    'yxspkg.same_file',
        'ls':          'yxspkg.yxsfile',
        'loop':        'yxspkg.loop_cmd'
    }
    run_yxs_command(sys.argv,command_dict)
def run_yxs_command(argv,command_dict):
    if len(argv) > 1:
        cmd = argv[1]
        argv.pop(1)
        sys.argv = argv
    else:
        cmd = '--help'
    if cmd not in command_dict:
        cmd = '--help'
    if cmd == '--help':
        print('useage:module list')
        l = list(command_dict.keys())
        l.sort(key=lambda x:x.lower())
        max_length = max([len(i) for i in l])+4
        fmt = '    {:max_lengths}'.replace('max_length',str(max_length))
        for i in l:
            tcmd = command_dict[i]
            if tcmd.find('/help:') != -1:
                help_info = command_dict[i].split('/help:')[1].strip()
            else:
                help_info = ''
            print(fmt.format(i),end='')
            print(help_info)
    else:
        tcmd = command_dict[cmd].split('/help:')[0].strip()
        importlib.import_module(tcmd).main()
if __name__=='__main__':
    main()