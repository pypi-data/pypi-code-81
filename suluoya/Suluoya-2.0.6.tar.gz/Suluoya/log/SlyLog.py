import time


class sprint(object):
    
    def __init__(self):
        '''
        red, green, yellow, blue, magenta紫, cyan青, white.
        '''
        from termcolor import colored
        self.colored = colored

    def red(self, content='Suluoya'):
        print(self.colored(content, 'red'))

    def green(self, content='Suluoya'):
        print(self.colored(content, 'green'))

    def yellow(self, content='Suluoya'):
        print(self.colored(content, 'yellow'))

    def blue(self, content='Suluoya'):
        print(self.colored(content, 'blue'))

    def magenta(self, content='Suluoya'):
        print(self.colored(content, 'magenta'))

    def cyan(self, content='Suluoya'):
        print(self.colored(content, 'cyan'))

    def pink(self, contents='Suluoya'):
        print(f'\033[1;35;40m{contents}')
        print(self.colored('', 'white'), end='')

    def black(self, contents='Suluoya'):
        print(f'\033[1;30;40m{contents}')
        print(self.colored('', 'white'), end='')
    
    def hide(self):
        print(f'\033[0;30;40m',end='')
    
    def show(self):
        print(self.colored('', 'white'), end='')


class slog(sprint):
    def __init__(self,filename='log'):
        import os
        try:
            os.makedirs('./log')
        except:
            pass
        self.filename = filename
        self.Time = time.asctime(time.localtime(time.time()))
        with open(f'log\\{self.filename}.log', 'w', encoding='utf8') as f:
            f.write(self.Time+'\n')
            f.write("(｡･∀･)ﾉﾞ嗨!\n\n")
    def log(self,content='Suluoya',mode=0):
        with open(f'log\\{self.filename}.log', 'a', encoding='utf8') as f:
            if mode == 0:
                f.write(f'\n{content}\n')
            elif mode == 1:
                f.write(content+'\n')
            elif mode == 2:
                f.write(content+' ')


