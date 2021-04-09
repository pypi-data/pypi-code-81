from triedTree.base_tried_tree import BaseTriedTree
import os


class InfoTriedTree(BaseTriedTree):
    def __init__(self, path):
        super(InfoTriedTree, self).__init__(path=path)

    def _load_data_tree(self, file_or_path, type_prefix=None):
        total_file = []
        if not os.path.isfile(file_or_path):
            files = os.listdir(file_or_path)
            for file in files:
                real_path = os.path.join(file_or_path, file)
                if type_prefix == None:
                    new_type_prefix = file
                else:
                    new_type_prefix = type_prefix + "_" + file
                if os.path.isdir(real_path):
                    self._load_data_tree(real_path, type_prefix=new_type_prefix)
                else:
                    total_file.append((real_path, new_type_prefix))
        else:
            total_file.append((file_or_path, type_prefix))

        for file_and_type in total_file:
            self._add_file_to_tree(file_and_type)

    def _add_file_to_tree(self, file_and_type):
        '''从文件中读取数据'''
        filename, type_prefix = file_and_type
        with open(filename, 'r', encoding='utf-8') as fread:
            for line in fread:
                line = line.split('#')[0].strip()
                if line == "":
                    continue
                token_list = line.split(" ")
                word = token_list[0]

                self._insert_word_and_type_to_tree(word, type_prefix)

                #字数太短了就不做处理，比如新县
                if len(word) >= 3:
                    if type_prefix == 'province':
                        self._insert_word_and_type_to_tree(word.replace("省",""), type_prefix)
                    elif type_prefix == 'city':
                        if word[-1] == "市":
                            self._insert_word_and_type_to_tree(word[:-1], type_prefix)
                    elif type_prefix == 'town':
                        if word.endswith('街道'):
                            self._insert_word_and_type_to_tree(word[:-1], type_prefix)

                    elif type_prefix == 'county':
                        if word[-1] == "市":
                            self._insert_word_and_type_to_tree(word[:-1],type_prefix)
                        elif word[-1] == "县":
                            self._insert_word_and_type_to_tree(word[:-1],type_prefix)
                        elif word[-2] != "新" and word[-1] == "区":
                            self._insert_word_and_type_to_tree(word[:-1],type_prefix)



    def update_triedTree_keys(self, keys_list):
        '''
        跟新字典树的key值，
        mode  type  key
        +   common_电话   咨询电话
        -   ingore  咨询电话
        '''
        for item in keys_list:
            if len(item) < 3:
                continue
            item=item[0:3]
            assert len(item) == 3
            mode, key_type, key = item
            if mode == "+":
                self._insert_word_and_type_to_tree(key, key_type)
            elif mode == "-":
                self._delete_word_and_type_from_tree(key, key_type)
            else:
                raise TypeError("不支持的mode")

    def _delete_word_and_type_from_tree(self, word, type):
        current_root = self.trie_tree
        for char in list(word):
            if char not in current_root:
                current_root[char] = {}
            current_root = current_root[char]

        if 'end' not in current_root:
            #print("Warning:%s %s 不在字典树中，请确认" % (word, type))
            return

        if type not in current_root['type_list']:
            #print("Warning:%s %s 不在字典树中，请确认" % (word, type))
            return

        current_root['type_list'].remove(type)
        if not current_root['type_list']:
            if 'end' in current_root:
                del current_root['end']
            del current_root['type_list']

    def process(self, content,start_positions = []):
        cn_chars = content
        word_list = []
        type_list = []
        position_list = []
        tmp_search_word = []

        current_position = 0
        while len(cn_chars) > 0:
            word_tree = self.trie_tree
            current_word = ""  # 当前词
            for (index, cn_char) in enumerate(cn_chars):
                if cn_char not in word_tree:
                    break
                current_word += cn_char
                # 词结束
                if 'end' in word_tree[cn_char]:
                    tmp_search_word.append((current_word, index, word_tree[cn_char]['type_list']))
                word_tree = word_tree[cn_char]  # 继续深搜

            # 没有找到以这个字开头的词，继续下一个字

            tmp_search_word = self.check_entity_valid(tmp_search_word,cn_chars,current_position,start_positions)

            if len(tmp_search_word) == 0:
                cn_chars = cn_chars[1:]
                current_position += 1
            else:

                word, index, type = tmp_search_word[-1]
                word_list.append(word)
                type_list.append(type)
                current_position += len(word)
                position_list.append(current_position)
                cn_chars = cn_chars[index + 1:]
                tmp_search_word = []

        return word_list, type_list, position_list

    def get_word_types(self, word):
        types = []
        word_tree = self.trie_tree
        for (index, cn_char) in enumerate(word):
            if cn_char not in word_tree:
                break
            # 词结束
            if 'end' in word_tree[cn_char] and index == (len(word) - 1):
                types = word_tree[cn_char]['type_list']
            word_tree = word_tree[cn_char]  # 继续深搜

        return types


    def check_entity_valid(self,tmp_search_word,content,current_position,start_positions):
        '''
        根据当前已经解析出来的实体，判断实体是不是一个合法的实体
        '''
        filter_search_word = []
        for (word, index, type) in tmp_search_word:
            if current_position not in start_positions:
                continue
            if 'province' in type or 'city' in type:
                check_list = ['路','街道',"东路","西路",'北路','南路','大道', '大街',"村",'岸','花苑']
                check_in = False
                for check in check_list:
                    if content[index+1:].startswith(check):
                        check_in = True
                        break

                if not check_in:
                    filter_search_word.append((word,index,type))
            elif 'county' in type:
                check_list = ['路','街道',"东路","西路",'北路','南路','大道', '大街',"村"]
                check_in = False
                for check in check_list:
                    if content[index + 1:].startswith(check):
                        check_in = True
                        break

                if not check_in:
                    filter_search_word.append((word, index, type))

            else:
                filter_search_word.append((word, index, type))
        return filter_search_word

