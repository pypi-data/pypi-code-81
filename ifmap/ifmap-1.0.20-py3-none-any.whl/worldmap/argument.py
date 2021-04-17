import argparse
import simple_utils
from simple_utils import logging


def get(caller='main', kind='', name='', unknown_args={}):
    default_templates_dir = './'
    if caller == 'main':
        # python3 -m worldmap 으로 실행할 때의 매개변수를 받습니다.
        parser = argparse.ArgumentParser(description='WorldMap')
        parser.add_argument('kind', help='실행 할 모듈의 이름을 입력해주세요.', type=str)
        parser.add_argument('name', help='실행 할 명령어의 이름을 입력해주세요.', type=str)
        parser.add_argument('--templates-dir', help='템플릿 폴더가 저장되어있는 루트 경로를 입력해주세요.', default=default_templates_dir)
        args, unknown_args = parser.parse_known_args()
    elif caller == 'code':
        args = simple_utils.structure.dotdict({
            'kind': kind,
            'name': name,
            'templates_dir': default_templates_dir
        })
    else:
        logging.error(f'invalid caller {caller}')
        exit()

    if len(unknown_args) % 2 != 0:
        logging.error('추가 매개변수는 짝을 맞추어야 합니다.')
        exit()

    
    kwargs = {key: unknown_args[index * 2 + 1]for index, key in enumerate(unknown_args[::2])}
    kwargs['--templates-dir'] = args.templates_dir

    nkwargs = {}
    for key, value in kwargs.items():
        if not key.startswith('--'):
            logging.error('추가 매개변수는 \'--\'으로 시작해야 합니다.')
            exit()

        if len(key) <= 2:
            logging.error('추가 매개변수의 길이가 너무 짧습니다.')
            exit()
        
        nkwargs[key[2:].replace('-', '_')] = value

    kwargs = nkwargs
    print("""

    ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗ ███╗   ███╗ █████╗ ██████╗ 
    ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗████╗ ████║██╔══██╗██╔══██╗
    ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║██╔████╔██║███████║██████╔╝
    ██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║██║╚██╔╝██║██╔══██║██╔═══╝ 
    ╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝██║ ╚═╝ ██║██║  ██║██║     
    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     
    """)                                                         
    print(f"""
    * [USER INPUT] {simple_utils.time.get_kst()} *
    ■ kind: {args.kind}
    ■ name: {args.name}
    ■ kwargs: {kwargs}
    """)
    
    return args.kind, args.name, kwargs
