import os
import sys
import inspect

class setup:

    @staticmethod
    def init():
        dir = os.getcwd()
        yes = input(f'Would you like to init project at dir: {dir}? [Y|N]\n')

        if yes.lower().strip() in ['y', 'yes']:

            definitions_prod = dir + '/definitions_prod.py'
            config_file = dir + '/config.json'
            if not os.path.exists(definitions_prod):
                from swissarmykit.templates import definitions
                src = inspect.getsource(definitions)
                f = open(definitions_prod, "w")
                f.write(src)
                f.close()
                print(f'INFO: Generated file: {definitions_prod}')

            if not os.path.exists(config_file):
                from swissarmykit.templates.config_default import ConfigDefault
                ConfigDefault.generate_config(config_file)

            from definitions_prod import swissarmykit_conf
            swissarmykit_conf.init_folder()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python -c "from swissarmykit.admin import setup; setup.init()" ')
    else:
        setup.init()

