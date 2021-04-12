''' package entry module '''
from dofast.simple_parser import SimpleParser

def main():
    parser=SimpleParser()
    parser.input('-seg', '--segment')
    parser.parse_args()
    
    if parser.segment:
        from .segment import MMM
        print(MMM().bidirectional_segment(parser.segment.value))

    
