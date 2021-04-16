import regex as re
from kdmt.text import clean_text


def fix_formating(text):

    text = text.replace('...', '.')
    text = text.replace('..', '.')
    text = re.sub(r':\s+', ': ', text)
    #    text = text.replace('\\r', '. ')
    text = text.replace(' .', '. ')
    text = re.sub(r':\s?\.', ':', text)
    return text.strip('\n').strip().strip('\n')



if __name__ == '__main__':
    mail = "[1235456] hi how are you"
    print(clean_text(mail))
