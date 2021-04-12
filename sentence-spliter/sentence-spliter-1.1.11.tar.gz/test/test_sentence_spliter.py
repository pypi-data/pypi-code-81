# from sentence_spliter.sentence_spliter import Spliter
from sentence_spliter.sentence_spliter import Spliter
from loguru import logger


def test_spliter():
    options = {
        'language': 'zh',
        'long_short_sent_handle': 'y',
        'hard_max_length': 300,
        'max_length': 150,
        'min_length': 15,
        'remove_blank': 'True'
    }
    spliter = Spliter(options)
    input_path = '../test/data/test.txt'
    output_path = '../test/data/cut_sentences.txt'
    with open(input_path, 'r', encoding='utf-8') as f_read:
        sentence = f_read.read()
    logger.debug(sentence)
    output_lines = []
    output_lines.extend(spliter.cut_to_sentences(sentence))
    open(output_path, 'w', encoding='utf-8').write('\n'.join(output_lines))


if __name__ == '__main__':
    test_spliter()
