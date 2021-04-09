#!/usr/bin/env python

'''
algocli - print common algorithms via the command line
written by Emanuel Ramirez (emanuel2718@gmail.com)
'''

import argparse
import algocli.replacer as replacer
from algocli.util import ALGORITHMS, SUPPORTED_LANGUAGES, get_available_colors
from bs4 import BeautifulSoup, SoupStrainer
from contextlib import closing
from requests import Session
from requests.exceptions import RequestException
from time import time
from algocli import __version__

STOP_FLAGS = ["'''Library'''"]

BOLD = '\033[1m'
ITALIC = '\033[3m'
END = '\033[0m'

STACK = []
SKIP = ['<pre>']
END_SKIP = ['</pre>']


DEFAULT_LANGUAGE = 'Python'
DEFAULT_COLOR = 'monokai'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12871.102.0)'
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36'}

session = Session()


class DataHandler:
    def __init__(self, args, algorithm, language):
        '''
            Example variable values:
                self.language                   =: 'cpp'
                self.algorithm_name             =: 'insertionsort'
                self.sanitized_language         =: 'C.2B.2B'
                self.sanitized_algorithm_name   =: 'Insertion_sort'
                self.formal_language            =: 'C++'
                self.formal_algorithm           =: 'Insertion Sort algorithm'
        '''

        self.language = language
        self.algorithm_name = algorithm
        self.args = args
        self.color = args['colorscheme']

        self.sanitized_language = self.get_sanitized_language()
        self.sanitized_algorithm_name = self.get_sanitized_algorithm_name()

        self.formal_language = SUPPORTED_LANGUAGES[self.language][1]
        self.formal_algorithm = ALGORITHMS[self.algorithm_name][1]

        self.data = self.get_data(self.get_url(), True)

        self.section_number, self.formatted_language = self.get_section_and_language()

    def _print_banner(self, msg):
        print('\n\n' + '=' * 70)
        print(msg.center(70))
        print('=' * 70 + '\n\n')

    def _get_colored_output(self, output_code):
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import Terminal256Formatter

        user_style = self.color if self.color in get_available_colors() else 'default'
        lexer = get_lexer_by_name(self.language, stripall=True)
        formatter = Terminal256Formatter(
            bg='dark', linenos=False, style=user_style)

        return highlight(output_code, lexer, formatter)

    def display_tip_if_applicable(self):
        if self.args['colorscheme'] not in get_available_colors():
            _print_tip(f'"algocli --list-colors" for available colorschemes\n')

    def dump_output_to_file(self, output_code):
        header = f'\n===== {self.formal_algorithm} using {self.formal_language} ====='
        with open('results.txt', 'a') as output_file:
            output_file.write(header)
            output_file.write(output_code)
            output_file.write(
                '\n====================================================\n')

    def print_code_to_console(self, output_code):
        if not output_code.startswith('{{task'):
            self._print_banner(
                f'{self.formal_algorithm} using {self.formal_language}')

            if not self.args['colorscheme']:
                print(output_code)
            else:
                print(self._get_colored_output(output_code))

            self._print_banner('ALGORITHM OUTPUT ENDS HERE')

        # No modifications done to the raw algorithm means no match was found
        # for that specific language/algorithm
        else:
            _print_error(
                f'No results found for {self.formal_algorithm} using {self.formal_language}')

    def is_valid_line(self, line):
        if line.startswith('<pre>') and line.endswith('</pre>'):
            return False
        if line.startswith('<pre>'):
            STACK.append('<pre>')
            return False

        if len(STACK) == 0:
            return True

        if line.endswith('</pre>'):
            STACK.pop()
            return False

    def format_code_for_output(self, raw_algorithm_code):
        result = []
        code = raw_algorithm_code.split('\n')

        for line in code:
            if line in STOP_FLAGS:
                return result
            else:
                if self.is_valid_line(line):
                    line = replacer.get_replacement_line(line)
                    result.append(line)
        return result

    def get_url(self):
        ''' Returns the url of the desired algorithm
            This url points to a a rosettacode page with all the available
            languages for the specified algorithm.

            NOTE: algorithm name must match RosettaCode naming convention.
                  If the user want to search for `algocli insertionsort cpp`
                  then the url should be:

                  https://rosettacode.org/wiki/Sorting_algorithms/Insertion_sort'

        '''
        return f'https://rosettacode.org/wiki/{self.sanitized_algorithm_name}'

    def get_code_url(self):
        return (
            f'https://rosettacode.org/mw/index.php?title={self.sanitized_algorithm_name}'
            f'&action=edit&section={self.section_number}')

    '''
    NOTE:   THIS IS SLOOOOOOOOW! Taking ~3 seconds on average. Want to take this down to 1
            second on average TOPS!

    TODO:   divide this into separate function for more legibility
    '''

    def get_data(self, url, formatting_data=False):
        '''code := the request is for the final algorithm code'''

        try:
            with closing(session.get(url, headers=HEADERS, stream=True, timeout=10)) as response:
                if self.is_valid_response(response):
                    if formatting_data:
                        return BeautifulSoup(
                            response.content,
                            'html.parser').find(
                            id='toc')
                    return str(
                        BeautifulSoup(
                            response.content,
                            'html.parser').find('textarea').text)
                else:
                    return None
        except RequestException as e:
            _print_error(e)
            return None

    def is_valid_response(self, resp):
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

    def get_section_and_language(self):
        for category in self.data('li'):
            current_language = category.find('a')['href'].lstrip('#')
            if current_language.lower() == self.sanitized_language.lower():
                section_number = str(category).split('"')[1].split('-')[-1]
                formatted_language = category.find(
                    'span', {'class': 'toctext'}).text
                return section_number, formatted_language
        return None, None

    def get_sanitized_algorithm_name(self):
        ''' The rosettacode page address must contain the sorting algorithm in
            a specific format. For example, -insertionsort appear as Insertion_sort
            in Rosseta Code. Another example is the dijstra algorithm, if the user
            gives the algorithm flag "dijkstra" it needs to be formatted into
            Dijkstra%27s_algorithm to match Rosseta Code formatting

        :return formatted self.algorithm (dijkstra) string as Dijkstra%27s_algorithm
        '''
        for key, value in ALGORITHMS.items():
            if self.algorithm_name == key:
                return value[0]
        return None

    def get_sanitized_language(self):
        ''' Rosseta Code has some specific names for different languages. For example
            C++ is represented as C.2B.2B and Python is reprensented as python in lowercase.
            This function "sanitizes" the language flag to match the formatting of Rosseta Code

            Default language is chosen if no language flag was found

        :return formatted self.language (chsarp) string as C.23
        '''
        if self.language is None:
            return DEFAULT_LANGUAGE
        for key, value in SUPPORTED_LANGUAGES.items():
            if self.language == key:
                return value[0]
        return None


def _print_tip(msg):
    print(f'{BOLD}[TIP]{END} {msg}')


def _print_error(err):
    print(f'{BOLD}[ERROR]{END} {err}')


def _print_warning(msg):
    print(f'{BOLD}[WARNING]{END} {msg}')


def _print_ok(msg):
    print(f'{BOLD}[OK]{END} {msg}')


def _print_debug(msg):
    print(f'{BOLD}[DEBUG]{END} {msg}')


def _print_list(msg, arr):
    print('\n' + msg + '\n')

    if isinstance(arr, tuple) or isinstance(arr, list):
        for item in arr:
            print(f'- {item}')
    else:
        for item, value in arr.items():
            print(f'- {item:<20s} {value[1]:<10s}')
    print()


def get_parser():
    parser = argparse.ArgumentParser(
        description='print common algorithms via the command line',
        usage='algocli [INPUT ...] [-h] [-v] [-c COLORSCHEME] [--list-colors] '
              '[--list-lang] [--list-algo]',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        'input',
        type=str,
        nargs='*',
        metavar='INPUT',
        help='the language and algorithm (i.e algocli python fib)')

    parser.add_argument(
        '-v',
        '--version',
        help='displays the current version of algocli',
        action='store_true')

    parser.add_argument(
        '--list-colors',
        help='print list of available colorschemes',
        action='store_true')

    parser.add_argument(
        '--list-lang',
        help='print list of supported languages',
        action='store_true')

    parser.add_argument(
        '--list-algo',
        help='print list of supported algorithms',
        action='store_true')

    parser.add_argument(
        '--file',
        help='save output to results.txt',
        action='store_true')

    parser.add_argument(
        '-c',
        '--color',
        help='colorized output',
        nargs='?',
        dest='colorscheme',
        const='vim',
        metavar='COLORSCHEME')

    return parser


def is_valid_input(arr, input_flag) -> str:
    ''' Check if the given algorithm or language flag (@input_flag) is valid.

    :param  arr: list of available algorithms or supported language
    :param: input_flag: list of algorithm and/or language input flags
    :return the language or algorithm flag if valid
    '''
    for arg in input_flag:
        if arg.lower() in arr.keys():
            return arg.lower()

    return None


def parse_input(stdin) -> tuple:
    ''' Returns the parsed algorithm and language input flags received from stdin.

    :param: stdin: argument parser
    :return tuple in the form (algorithm name, language name)
    '''
    args = stdin

    # handle input of form: algocli -c radixsort cpp were the color flag is followed
    # by an algorithm or language flag
    if (args['colorscheme'] in ALGORITHMS.keys() or
            args['colorscheme'] in SUPPORTED_LANGUAGES.keys()):

        args['input'].append(args['colorscheme'])
        args['colorscheme'] = DEFAULT_COLOR

    if isinstance(stdin, str):
        parser = get_parser()
        args = vars(parser.parse_args(raw_in.split(' ')))

    algo = is_valid_input(ALGORITHMS, args['input'])
    lang = is_valid_input(SUPPORTED_LANGUAGES, args['input'])
    return algo, lang


def run():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(f'algocli {__version__}')
        return

    if args['list_colors']:
        _print_list(
            'Supported Colorscemes: [Example: algocli -b64 -python --color rrt]',
            get_available_colors())
        return

    if args['list_lang']:
        _print_list('Supported Languages flags:', SUPPORTED_LANGUAGES)
        return

    if args['list_algo']:
        _print_list('Supported Algorithms flags:', ALGORITHMS)
        return

    if not args['input']:
        parser.print_help()
        return

    else:
        algo, lang = parse_input(args)
        if algo is None:
            _print_error(
                'Not valid algorithm specified. See algocli --list-algo')
            return
        if lang is None:
            _print_error(
                'Not valid language specified. See algocli --list-lang')
            return

        #start_time = time()
        data_handler = DataHandler(args, algo, lang)
        raw_algorithm_code = data_handler.get_data(data_handler.get_code_url())
        formatted_output_code = '\n'.join(
            data_handler.format_code_for_output(raw_algorithm_code))

        if args['file']:
            data_handler.dump_output_to_file(formatted_output_code)
        else:
            data_handler.print_code_to_console(formatted_output_code)
        #_print_debug(f'Time taken: {time()-start_time:.4} seconds')


if __name__ == '__main__':
    run()
