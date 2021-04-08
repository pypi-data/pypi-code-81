import json
import codecs
import os
import sys
import getopt


class ManageTranslator:
    def __init__(self):
        """
        This class is used to manage and maintain translation data for fasifu.
        """
        self.dataFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "language_data.json")
        self.data = self.read_data()
        self.languages = self.data[""].copy()
        del self.data[""]

    def read_data(self):
        # read data with exact encodings using codec.open
        with codecs.open(self.dataFilePath, "r", encoding="utf8")as file:
            return json.load(file)

    def print_table(self):
        """
        This function print all translated data in table form which looks neat
        :return:
        """
        len_dic = {"en": 0}  # stores len of biggest string in each language so table can be made of correct size
        for key in self.data:  # iterates through every string of each language and store the biggest number in dict
            if len(key) > len_dic["en"]:
                len_dic["en"] = len(key)
            for lang in self.data[key]:
                if lang not in len_dic:
                    len_dic[lang] = 0
                if len(self.data[key][lang]) > len_dic[lang]:
                    len_dic[lang] = len(self.data[key][lang])
        format_string = " | ".join([("{:<" + str(len_dic[lang])) + "}" for lang in len_dic])  # manages space
        print(format_string.format(*len_dic.keys()))  # prints header
        print(format_string.format(*["="*len_dic[lang] for lang in len_dic]))  # seperator
        for key, value in self.data.items():
            data = [key] + list(value.values())
            print(format_string.format(*data))  # prints translation values
        print(format_string.format(*["=" * len_dic[lang] for lang in len_dic]))

    def add_item(self, english, save=True):
        """
        Adds english word/sentence in translation data. After these we can store the translation data for these
        word/sentence by using add_word.
        :param english: English word/sentence to be removed.
        :return:
        """
        self.data[english] = self.languages
        if save:
            self.save_data()

    def remove_item(self, english, save=True):
        """
        Removes english word and translations of it from data.
        :param english: English word/sentence to be removed.
        :return:
        """
        try:
            del self.data[english]
            if save:
                self.save_data()
        except Exception as ex:
            print(ex)

    def add_language(self, language_code, save=True):
        """
        Adds a language in data with default value = "" for all english words
        :param language_code: e.g.- English = en, German = de
        :return:
        """
        language_code = language_code.lower()
        for key in self.data:
            if language_code not in self.data[key]:
                self.data[key][language_code] = ""
        self.languages[language_code] = ""
        if save:
            self.save_data()

    def remove_language(self, language_code, save=True):
        """
        removes translation of a language for all words
        :param language_code: e.g.- English = en, German = de
        :return:
        """
        language_code = language_code.lower()
        for key in self.data:
            del self.data[key][language_code]
        del self.languages[language_code]
        if save:
            self.save_data()

    def add_translation(self, english, language_code, translated_word, save=True):
        """
        Adds new translation for the supplied english word.
        :param english: English word whose translation is to be supplied.
        :param language_code: Language code of the language whose translation is to be supplied. e.g.- English = en
        :param translated_word: Translation of the english word in the suppied language
        :return:
        """
        language_code = language_code.lower()
        if language_code not in self.languages:
            self.add_language(language_code)
        if not self.data.get(english):
            self.add_item(english)
        self.data[english][language_code] = translated_word
        if save:
            self.save_data()

    def get_empty_by_language_code(self, language_code):
        """
        Returns list of english words which doesn't have translation for the supplied language_code.
        :param language_code: e.g.- English = en, German = de
        :return: List
        """
        language_code = language_code.lower()
        data = []
        for key in self.data:
            if not self.data[key][language_code]:
                data.append(key)
        return data

    def fill_empty_by_language_code(self, language_code, save=True):
        """
        Fill translated data one by one for the english words doesn't have translation for the supplied language_code.
        :param language_code: e.g.- English = en, German = de
        :return:
        """
        language_code = language_code.lower()
        data = self.get_empty_by_language_code(language_code)
        for english in data:
            print("en:", english)
            translation = input(f"{language_code}: ")
            self.add_translation(english, language_code, translation, save)
            print("added.\n\n")

    def get_all_empty(self):
        """
        Returns List of lists. These lists contain english word/sentence and language code which doesn't have translation
        for the supplied english word/sentence.
        :return:
        """
        data = []
        for key in self.data:
            for language_code in self.languages:
                if not self.data[key][language_code]:
                    data.append([key, language_code])
        return data

    def fill_all_empty(self, save=True):
        """
        Prints english word which doesn't has translation for the language code below it. You can fill all the
        translation one by one.
        :return:
        """
        data = self.get_all_empty()
        for english, language_code in data:
            print("en:", english)
            translation = input(f"{language_code}: ")
            self.add_translation(english, language_code, translation, save)
            print("added.\n\n")

    def save_data(self):
        self.data[""] = self.languages
        with codecs.open(self.dataFilePath, "wb", encoding="utf8")as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)  # writes data and character perfectly


def print_args():
    print("""
    Call: python ManageTranslations.py --parameters 
           --print_table: Prints table of all translations with language code as column name.
           --add_item <english word/sentence to be added in translation>: Adds new word in translations.
           --remove_item <english word/sentence to be removed from translation>: Removes word from translations.
           --add_language <language code e.g.- For English = en>: Adds column for new language code in preexisting and new data
           --remove_language <language code e.g.- For English = en>: Removes column form preexisting and new data
           --add_translation -e <english version of the translation> -l <language_code of translation> -t <translated>: Add/change translation
           --fill_empty_by_language <language_code>: Get none translated words for supplied language and fill translation one by one
           --fill_empty: Get none translated words from all data and fill translation one by one
       """)


def args_read(l_search_parameter):
    l_args = sys.argv[1:]

    try:
        opts, args = getopt.getopt(l_args, "e:l:t:", ["print_table",
                                                "add_item=",
                                                "remove_item=",
                                                "add_language=",
                                                "remove_language=",
                                                "add_translation",
                                                "fill_empty_by_language=",
                                                "fill_empty",
                                                ])
    except getopt.GetoptError as err_det:
        print("Error in reading parameters:" + str(err_det))
        sys.exit("Wrong parameters - exiting")
    if opts:
        for opt, arg in opts:
            if l_search_parameter == opt:  # in ("-u", "--usage"):
                return arg
            if "--" + l_search_parameter == opt or "-" + l_search_parameter == opt:
                if arg:
                    return arg
                elif opt in ["--print_table", "--add_translation", "--fill_empty"]:
                    return opt
    return None

def manage_args():
    m = ManageTranslator()
    if args_read("print_table"):
        m.print_table()
    elif args_read("add_item"):
        m.add_item(args_read("add_item"))
    elif args_read("remove_item"):
        m.remove_item(args_read("remove_item"))
    elif args_read("add_language"):
        m.add_language(args_read("add_language"))
    elif args_read("remove_language"):
        m.remove_language(args_read("remove_language"))
    elif args_read("add_translation"):
        m.add_translation(args_read("e"), args_read("l"), args_read("t"))
    elif args_read("fill_empty_by_language"):
        m.fill_empty_by_language_code(args_read("fill_empty_by_language"))
    elif args_read("fill_empty"):
        m.fill_all_empty()
    else:
        print_args()


if __name__ == "__main__":
    manage_args()