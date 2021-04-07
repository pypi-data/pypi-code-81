import os
from swissarmykit.lib.core import Singleton, Config
from swissarmykit.lib.inspector import Inspector

@Singleton
class AppConfig(Config, Inspector):
    '''
        import os; import sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

        det 'AI_ENV' = 'dev' 'prod' or 'mac' 'stag'
        ps aux | grep python
        pkill -9 python

        Settings env in
            File | Settings | Build, Execution, Deployment | Console | Python Console


        export AI_ENV=stag
        printenv
        echo $MY_VAR


        Usage:

            try: from definitions_prod import *
            except Exception as e: print(e)/

        For IDE Pycharm: edit configuration: Environment Variable: append ;AI_ENV=mac

    '''

    ROOT_DIR = os.getcwd()
    if '\\' in ROOT_DIR:
        ROOT_DIR = ROOT_DIR.replace('\\', '/')

    DEFINITION_FILE = os.getcwd().replace('\\', '/')

    # Add more variable here on your need or method

swissarmykit_conf: AppConfig = AppConfig.instance() # For library to reference

appConfig = swissarmykit_conf # Change variable here on your demand

if __name__ == '__main__':
    print('Test swissarmykit_conf')
    print(os.environ.get('AI_ENV'))
    print(swissarmykit_conf)
    # print(swissarmykit_conf.config.get('env'))

