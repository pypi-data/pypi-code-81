from mnemonic import Mnemonic

def generate_mnemonic(strength=128):
    """
    生成英文助记词

    :param stength: 助词词个数, 128 对应 12 个单词, 256 对应 24 个单词
    """
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=strength)
    return words

def to_seed(words, passphrase=""):
    """
    获取种子

    :param words: 助记词
    :param passphrase: 密码
    """
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(words, passphrase)
    return seed

def to_hd_master_key(seed):
    mnemo = Mnemonic("english")
    return mnemo.to_hd_master_key(seed)