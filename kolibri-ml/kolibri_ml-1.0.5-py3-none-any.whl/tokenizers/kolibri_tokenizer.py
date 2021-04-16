#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'mohamedbenhaddou'

import regex as re
from kolibri.tokenizers.tokenizer import Tokenizer
from kolibri.stopwords import get_stop_words
from kdmt.dict import update


types_abstraction={
        'NUM' :  '__NUMBER__',
        'NUMCODE' :  '__CODE__',
        'MAYBECODE': '__MAYBECODE__',
        'DAY' :  '__DAY__',
        'YEAR' :  '__YEAR__',
        'NUM_TS' :  '__NUMBER__',
        'PLUS' :  '__SYMBOL__',
        'MINUS' :  '__SYMBOL__',
        'ELLIPSIS' :  '__PUNCTUATION__',
        'DOT' :  '__PUNCTUATION__',
        'COMA' :  '__PUNCTUATION__',
        'COLON' :  '__PUNCTUATION__',
        'SEMICOLON' :  '__PUNCTUATION__',
        'OTHER' :  '__SYMBOL__',
        'TIMES' :'__SYMBOL__',
        'EQ' : '__SYMBOL__',
        'CANDIDATE' : '__CANDIDATE__',
        'CLOSEPARENTHESIS' :'__SYMBOL__',
        'WEB_ADRESSS' : '__WEB__',
        'EMAIL' :'__EMAIL__',
        'DATE' :'__DATETIME__',
        'TIME' :'__DATETIME__',
        'DATE_NL' : '__DATETIME__',
        'MONTH' :'__DATETIME__',
        'MONTH_NL' :'__DATETIME__',
        'DICIMAL' : '__NUMBER__',
        'PIPE' : '__SYMBOL__',
        'FILE' :'__FILENAME__',
        'MONEY' :'__MONEY__',
        'IBAN' : '__BANKACCOUNT__',
        'PAYMENTCOMMUNICATION' : '__PAYMENTCOMMUNICATION__'
}
class KolibriTokenizer(Tokenizer):
    name = "kolibri_tokenizer"
    provides = ["tokens"]

    hyperparameters= {
        "fixed": {
        },

        "tunable": {
            "abstract-entities": {
                "value": True,
                "type": "categorical",
                "values": [True, False]
            }
        }
    }
    def __init__(self, hyperparameters=None):
        self.hyperparameters=update(self.hyperparameters, KolibriTokenizer.hyperparameters)
        super().__init__(hyperparameters)

        self.override_default_parameters(hyperparameters)

        self.stopwords = None
        if "language" in self.hyperparameters:
            self.language = self.hyperparameters['language']
            self.stopwords = get_stop_words(self.language)



        WORD = r"(?P<WORD>[^.'\s,#:!;/\({\[\]\)}?-]+|(?:'s|'t))"  # catch all
        NUM = r'(?P<NUM>\d+)'
        CODE = r'(?P<NUMCODE>\b(?:[A-Z\.-]+[0-9\.-]+|[0-9\.-]+[A-Z\.-]+)[A-Z0-9\.-]*\b)'
        MAYBECODE = r'(?P<MAYBECODE>\b\d{0,3}[ ]?\d{3}[ ]?\d{3}[ ]?\d{3}\b)'
        DAY = r'(?P<DAY>\d+(st|nd|rd|th))'
        NUM_TS = r'(?P<NUM_TS>[0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]+))'
        PLUS = r'(?P<PLUS>\+)'
        MINUS = r'(?P<MINUS>\-)'
        ELLIPSIS = r'(?P<ELLIPSIS>\.\.\.)'
        DOT = r'(?P<DOT>\.)'
        COMA = r'(?P<COMA>,)'
        QUESTION = r'(?P<QUESTION>\?)'
        EXLAMATION = r'(?P<EXLAMATION>\!)'
        COLON = r'(?P<COLON>\:)'
        SEMICOLON = r'(?P<SEMICOLON>;)'
        OTHER = r'[/\\{}\(\[\)\]#-]'
        TIMES = r'(?P<TIMES>\*)'
        EQ = r'(?P<EQ>=)'
        WS = r'(?P<WS>\s+)'
        IBAN = r'(?P<IBAN>[A-Z]{2}[0-9]{2}(?:[ ]?[0-9X]{4}){3,4}(?:[ ]?[0-9X]{1,2})?)'
        CANDIDATE1 = r'(?P<CANDIDATE>(?:[A-Z]+[-\.\s_]))'
        CANDIDATE2 = r'(?P<CANDIDATE>(?:[A-Z]\w+\s*(?:de\sla|de|du|di|des|van|of)+\s(?:[A-Z]\w+)))'
        CANDIDATE3 = r'(?P<CANDIDATE>[A-Z][\w\.-]*\'?\w(?:[,\. ]{0,2}[A-Z][\w-]*\'?[\w-]*)*\b)'
        OPENPARENTHESIS = r'(?P<OPENPARENTHESIS>[\(\<])'
        CLOSEPARENTHESIS = r'(?P<CLOSEPARENTHESIS>[\)\<])'
        DURATION = r'(?P<DURATION>\d+[\.,]?\d*\s*(?:\w+)?\s*(days?|hours?|minutes?)\s*(\d+[?.]?\d*\s*(days?|hours?|minutes?))?)'
        ACORNYM = r'(?P<ACRONYM>\b[A-Z][A-Z0-9-\&]+\b)'
        AR = r'(?P<AR_CONTRACTED>(?:[lcdjmntsLCDJMNTS]|qu|Qu)[\'’])'
        WA = r'(?P<WEB_ADRESSS>https?://[\S\%]+|www\.\w+(\.\w+)+)'
        EMAIL = r'(?P<EMAIL>[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][\.-0-9a-zA-Z]*\.[a-zA-Z]+)'
        DATE = r'(?P<DATE>\b((([0-3]?[0-9]|1st|2nd|3rd|\d{,2}th|(?:19|20)\d{2})[\.\/ -]{1,2}([0-3]?[0-9]|J(an(uary)?|u(ne?|ly?))|Feb(ruary)?|Ma(rch|y|r)|A(pr(il)?|ug(ust)?)|(((Sept?|Nov|Dec)(em)?)|Octo?)(ber)?))|(J(an(uary)?|u(ne?|ly?))|Feb(ruary)?|Ma(rch|y|r)|A(pr(il)?|ug(ust)?)|(((Sept?|Nov|Dec)(em)?)|Octo?)(ber)?[, ]\d{1,2}))([\/\., -]{0,2}(19|20)?[0-9]{2})?\b)'
        DATE_NL = r'(?P<DATE>\b([0-3]?[0-9]|1st|2nd|3rd|\d{,2}th|(?:19|20)\d{2})[\.\/ -]([0-3]?[0-9]|j(?:an(uari)?|u(?:ni?|li?))|feb(ruari)?|m(?:aart|ei)|a(?:pril|ug(ustus)?)|(?:(?:(?:sept|nov|dec)(em)?)|o(k|c)to?)(ber)?)([\/\. -]+(?:19|20)?[0-9]{2})?\b)'
        DATE_NL2 = r'(?P<DATE>\b(?:an(uari)?|u(?:ni?|li?))|feb(ruari)?|m(?:aart|ei)|a(?:pril|ug(ustus)?)|(?:(?:(?:sept|nov|dec)(em)?)|o(k|c)to?)(ber)?([\/\. -]+(?:19|20)?[0-9]{2})?\b)'
        TIME = r'(?P<TIME>(\d{1,2}[:hH]\d{2}\sGMT)|(\d{1,2}[:hH]\d{2}))'
        MONTH = r'\b(?P<MONTH>J(?:anuary|u(?:ne|ly))|February|Ma(?:rch|y)|A(?:pril|ugust)|(?:(?:(?:Sept|Nov|Dec)em)|Octo)ber)\b'
        MONTH_NL = r'(?P<DATE>\b([0-3]?[0-9]|1ste?|2nde?|3rde?|\d{,2}de|(?:19|20)\d{2})[\.\/ -]([0-3]?[0-9]|j(?:an(uari)?|u(?:ni?|li?))|feb(ruari)?|m(?:aart|ei)|a(?:pril|ug(ustus)?)|(?:(?:(?:sept|nov|dec)(em)?)|o(k|c)to?)(ber)?)([\/\. -]+(?:19|20)?[0-9]{2})?\b)'
        DICIMAL = r'(?P<DICIMAL>\d+[.,]\d+)'
        OPENQOTE = r'(?P<OPENQOTE>«+)'
        ENDQOTE = r'(?P<ENDQOTE>»+)'
        EXCEPTIONS = r'(?P<WORD>Aujourd\'hui)'
        DOUBLEQOTE = r'(?P<DOUBLEQOTE>"+)'
        SINGLEQOTE = r'(?P<SINGLEQOTE>\'+)'
        PIPE = r'(?P<PIPE>\|)'
        YEAR = r'(?P<YEAR>\b201\d\b)'
        PAYMENTCOMMUNICATION=r'(?P<PAYMENTCOMMUNICATION>\b(?:\d{3}[\/-]\d{4}[\/-]\d{5})\b)'
        MULTIPLEWORD = r'(?P<MULTIWORD>(?:\w+-)(?!\d{6,})(?:\w+\-?)+)'
        FILE = r'(?P<FILE>(?:\w+-?)(?:\w+\-?)+\.(?:pdf|png|xlsx?|docx?|pptx?|jpe?g|csv|txt|rtf)\b)'
        MONEY = r'(?P<MONEY>-?(?:(?:\$|£|€)\s?\d+([,\.]\d+)*)|\b(?:\d{1,3}[,\. ]?)+\d{0,2}\s*(?:\$|£|€|euro?s?|EUR)\b|\b\d{1,3}[,\.](?:\d{3}[,\.])+\d{0,2}\b)'


        self.master_pat = re.compile(r'|'.join(
                [OTHER, AR, EXCEPTIONS, WA, EMAIL, MONEY, DATE, TIME, MONTH, CODE, DURATION, DICIMAL, NUM_TS, ACORNYM,
                 DAY, NUM,
                 OPENPARENTHESIS, CLOSEPARENTHESIS, WS, FILE, MULTIPLEWORD, PLUS, MINUS, ELLIPSIS, DOT, TIMES, EQ,
                 QUESTION,
                 EXLAMATION, COLON, COMA, SEMICOLON, OPENQOTE, ENDQOTE, DOUBLEQOTE, SINGLEQOTE, PIPE, WORD]),
                re.UNICODE)


    def tokenize(self, text):
        text = str(text).replace(r'\u2019', '\'')
        scanner = self.master_pat.scanner(text)

        tokens= [(m.group().strip(), m.lastgroup) for m in iter(scanner.match, None) if m.group().strip()!=""]
        if self.get_prameter("abstract-entities"):
            tokens=[t[1] if t[1] in ['WA', 'EMAIL', 'MONEY', 'DATE', 'MONTH', 'DURATION', 'NUM_TS', 'NUM', 'FILE'] else t[0] for t in tokens]
        else:
            tokens=[t[0]  for t in tokens]
        return tokens

    def transform(self, X):
        if not isinstance(X, list):
            X=[X]
        return [self.tokenize(x) for x in X]




from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(KolibriTokenizer.name, KolibriTokenizer)



if __name__=='__main__':
    tokenizer = KolibriTokenizer()
    text = """This automated mail is triggered for $ 123 to inform you a rescind has been executed in Change Job with an effective date of 2019 10 01"""
    tokens = tokenizer.transform(text)

    print(tokens)