#!/usr/bin/env python

# This tool conjugates Galician verbs and can add them enclitic pronouns.
# Copyright (C) 2020 Andrés Vieites Pérez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re

from typing import Callable
from _collections_abc import dict_items

from conxugador.load_paradigms import load, PARADIGM_KEY, ROOTS_KEY,\
    SUFFIX_KEY, TENSES_KEY


WITHOUT_PARADIGM = '-'
PARTICIPIOS_DUPLOS = 'P'
VERBO_HOMOGRAFO = 'D'
VERBO_DEFECTIVO = 'DEF'
CONSONANTS = '(b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|y|z|ç|ñ)'
VOCAL = '(a|e|i|o|u)'

# Irregular verbs
DOER = 'doer'
ENRAIZAR = 'enraizar'
CUINCAR = 'cuincar'
MUSCAR = 'muscar'
LUCIR = 'lucir'
AFIAR = 'afiar'
PROHIBIR = 'prohibir'
SAUDAR = 'saudar'
CONSTRUIR = 'construír'
REUNIR = 'reunir'
ARRUINAR = 'arruinar'
FERIR = 'ferir'
DESPEDIR = 'despedir'
SAIR = 'saír'
SEGUIR = 'seguir'
SUBIR = 'subir'
XUNGUIR = 'xunguir'
CUBRIR = 'cubrir'
CRER = 'crer'

# Regular verbs
CONHECER = 'coñecer'
TRADUCIR = 'traducir'
ABRANGUER = 'abranguer'
ERQUER = 'erquer'
EXTINGUIR = 'extinguir'
MINGUAR = 'minguar'
ARGUIR = 'argüír'
DELINQUIR = 'delinquir'
# CONSTRUIR = 'construír' In original Conshuga there are two strategies for
# CONSTRUIR verb as irregular and as regular
COMUNICAR = 'comunicar'
CHEGAR = 'chegar'
AFIUZAR = 'afiuzar'
ABRAZAR = 'abrazar'
CANTAR = 'cantar'
VENDER = 'vender'
PARTIR = 'partir'


def get_conjugation(tenses_items: dict_items, conjugate_from_paradigm:
                    Callable[[str], str]) -> dict:
    new_paradigm = {}
    for tense, ps in tenses_items:
        new_paradigm[tense] = []
        for p in ps:
            new_paradigm[tense].append(conjugate_from_paradigm(p))
    return {TENSES_KEY: new_paradigm}


def get_conjugate_from_paradigm(or0: str, or1: str, or2: str, or3: str,
                                nr0: str, nr1: str, nr2: str, nr3: str) \
                                    -> Callable[[str], str]:

    def f3(p): return re.sub('^' + or3, nr3, p) if or3 else p

    def f2(p): return f3(re.sub('^' + or2, nr2, p) if or2 and nr2 else p)

    def f1(p): return f2(re.sub('^' + or1, nr1, p) if or1 and nr1 else p)

    return lambda p: f1(re.sub('^' + or0, nr0, p) if or0 and nr0 else None)


def get_irregular_conjugation(paradigms: dict, user_verb: str) -> dict:
    """This function looks among irregular paradigms for the appropriate one for
    user_verb"""

    for verb, paradigm in paradigms.items():
        tenses_items = paradigm[TENSES_KEY].items()
        if verb == user_verb:
            if paradigm[ROOTS_KEY] and \
                    paradigm[ROOTS_KEY][0] == WITHOUT_PARADIGM:
                return paradigm
            elif paradigm[ROOTS_KEY] and \
                    paradigm[ROOTS_KEY][0] == PARTICIPIOS_DUPLOS:
                return paradigm
            elif paradigm[ROOTS_KEY] and \
                    paradigm[ROOTS_KEY][0] == VERBO_HOMOGRAFO:
                return paradigm
            elif paradigm[ROOTS_KEY] and \
                    paradigm[ROOTS_KEY][0] == VERBO_DEFECTIVO:
                return paradigm
            elif paradigm[SUFFIX_KEY]:
                paradigm_verb = paradigm[PARADIGM_KEY]
                suffix = paradigm[SUFFIX_KEY]
                prefix = paradigm_verb[:-len(suffix)]
                new_prefix = user_verb[:-len(suffix)]

                def conjugate(p): return re.sub('(^|(/))' + prefix,
                                                '\\2' + new_prefix, p)

                return get_conjugation(tenses_items, conjugate)
            else:
                paradigm_verb = paradigm[PARADIGM_KEY]
                paradigm_roots = paradigm[ROOTS_KEY]
                or0 = paradigm_roots[0] if len(paradigm_roots) > 0 else None
                or1 = paradigm_roots[1] if len(paradigm_roots) > 1 else None
                or2 = paradigm_roots[2] if len(paradigm_roots) > 2 else None
                or3 = paradigm_roots[3] if len(paradigm_roots) > 3 else None
                nr0 = re.sub('(a|e|i|í)r$', '', user_verb)
                nr1 = None
                nr2 = None
                nr3 = None

                if paradigm_verb == DOER:
                    nr1 = re.sub('$', 'í', nr0)
                    nr2 = re.sub('$', 'i', nr0)
                    nr3 = re.sub('$', 'ï', nr0)
                elif paradigm_verb == ENRAIZAR:
                    nr1 = re.sub('i' + CONSONANTS + '?z$', 'i\\1c', nr0)
                    nr2 = re.sub('i' + CONSONANTS + '?z$', 'í\\1z', nr0)
                    nr3 = re.sub('i' + CONSONANTS + '?z$', 'í\\1c', nr0)
                elif paradigm_verb == CUINCAR:
                    nr1 = re.sub('i' + CONSONANTS + '?c$', 'i\\1qu', nr0)
                    nr2 = re.sub('i' + CONSONANTS + '?c$', 'í\\1c', nr0)
                    nr3 = re.sub('i' + CONSONANTS + '?c$', 'í\\1qu', nr0)
                elif paradigm_verb == MUSCAR:
                    nr1 = re.sub('u' + CONSONANTS + '?' + CONSONANTS + '?' +
                                 CONSONANTS + '?$', 'o\\1\\2\\3', nr0)
                    nr2 = re.sub('c$', 'qu', nr0)
                elif paradigm_verb == LUCIR:
                    nr1 = re.sub('u' + CONSONANTS + '?' + CONSONANTS + '?' +
                                 CONSONANTS + '?$', 'o\\1\\2\\3', nr0)
                    nr2 = re.sub('c$', 'z', nr0)
                elif paradigm_verb == AFIAR or paradigm_verb == PROHIBIR:
                    nr1 = re.sub('i' + CONSONANTS + '?$', 'í\\1', nr0)
                elif paradigm_verb == SAUDAR or paradigm_verb == CONSTRUIR or \
                        paradigm_verb == REUNIR:
                    nr1 = re.sub('u' + CONSONANTS + '?$', 'ú\\1', nr0)
                elif paradigm_verb == ARRUINAR:
                    nr1 = re.sub(VOCAL + 'i' + CONSONANTS + '?$', '\\1í\\2',
                                 nr0)
                elif paradigm_verb == FERIR or paradigm_verb == DESPEDIR:
                    nr1 = re.sub('e' + CONSONANTS + '?' + CONSONANTS + '?' +
                                 CONSONANTS + '?$', 'i\\1\\2\\3', nr0)
                elif paradigm_verb == SAIR:
                    nr1 = re.sub('$', 'i', nr0)
                elif paradigm_verb == SEGUIR:
                    nr1 = re.sub('egu$', 'ig', nr0)
                elif paradigm_verb == SUBIR:
                    nr1 = re.sub('u' + CONSONANTS + '?' + CONSONANTS + '?' +
                                 CONSONANTS + '?$', 'o\\1\\2\\3', nr0)
                elif paradigm_verb == XUNGUIR:
                    nr1 = re.sub('u' + CONSONANTS + '?' + CONSONANTS + '?gu$',
                                 'o\\1\\2gu', nr0)
                    nr2 = re.sub('gu$', 'g', nr0)
                elif paradigm_verb == CUBRIR:
                    nr1 = re.sub('u' + CONSONANTS + '?' + CONSONANTS + '?' +
                                 CONSONANTS + '?$', 'o\\1\\2\\3', nr0)
                    nr2 = re.sub('br$', 'b', nr0)
                elif paradigm_verb == CRER:
                    # nr0 = re.sub('(a|e|i|í)r$', '', user_verb)
                    pass
                # Regular verbs with paradigm in verbos.txt: CANTAR, VENDER and
                # PARTIR. Probably this section it is not necessary for CANTAR,
                # VENDER and PARTIR because they could be conjugate in function
                # get_regular_conjugation anyway.
                # elif not or1:
                #    nr0 = re.sub('(a|e|i|í)r$', '', user_verb)
                # Due to the elision of nr0 assigment we need to mark when the
                # verb did not match any of the above cases
                else:
                    or0 = nr0 = None

                if or0 and nr0:
                    conjugate = get_conjugate_from_paradigm(or0, or1, or2, or3,
                                                            nr0, nr1, nr2, nr3)
                    return get_conjugation(tenses_items,
                                           conjugate)


def get_regular_conjugation(paradigms: dict, user_verb: str) -> dict:
    or0 = None
    or1 = None
    or2 = None
    or3 = None
    nr0 = re.sub('(a|e|i|í)r$', '', user_verb)
    nr1 = None
    nr2 = None
    nr3 = None

    if re.search('cer$', user_verb):
        tenses_items = paradigms[CONHECER][TENSES_KEY].items()
        or0, or1 = paradigms[CONHECER][ROOTS_KEY]
        nr1 = re.sub('c$', 'z', nr0)
    elif re.search('cir$', user_verb):
        tenses_items = paradigms[TRADUCIR][TENSES_KEY].items()
        or0, or1 = paradigms[TRADUCIR][ROOTS_KEY]
        nr1 = re.sub('c$', 'z', nr0)
    elif re.search('guer$', user_verb):
        tenses_items = paradigms[ABRANGUER][TENSES_KEY].items()
        or0, or1 = paradigms[ABRANGUER][ROOTS_KEY]
        nr1 = re.sub('gu$', 'g', nr0)
    elif re.search('quer$', user_verb):
        tenses_items = paradigms[ERQUER][TENSES_KEY].items()
        or0, or1 = paradigms[ERQUER][ROOTS_KEY]
        nr1 = re.sub('qu$', 'c', nr0)
    elif re.search('guir$', user_verb):
        tenses_items = paradigms[EXTINGUIR][TENSES_KEY].items()
        or0, or1 = paradigms[EXTINGUIR][ROOTS_KEY]
        nr1 = re.sub('gu$', 'g', nr0)
    elif re.search('guar$', user_verb):
        tenses_items = paradigms[MINGUAR][TENSES_KEY].items()
        or0, or1 = paradigms[MINGUAR][ROOTS_KEY]
        nr1 = re.sub('gu$', 'gü', nr0)
    elif re.search('güír$', user_verb):
        tenses_items = paradigms[ARGUIR][TENSES_KEY].items()
        or0, or1, or2 = paradigms[ARGUIR][ROOTS_KEY]
        nr1 = re.sub('gü$', 'gu', nr0)
        nr2 = re.sub('gü$', 'gú', nr0)
    elif re.search('quir$', user_verb):
        tenses_items = paradigms[DELINQUIR][TENSES_KEY].items()
        or0, or1 = paradigms[DELINQUIR][ROOTS_KEY]
        nr1 = re.sub('qu$', 'c', nr0)
    elif re.search('uír$', user_verb):
        tenses_items = paradigms[CONSTRUIR][TENSES_KEY].items()
        or0, or1 = paradigms[CONSTRUIR][ROOTS_KEY]
        nr1 = re.sub('u$', 'ú', nr0)
    elif re.search('car$', user_verb):
        tenses_items = paradigms[COMUNICAR][TENSES_KEY].items()
        or0, or1 = paradigms[COMUNICAR][ROOTS_KEY]
        nr1 = re.sub('c$', 'qu', nr0)
    elif re.search('gar$', user_verb):
        tenses_items = paradigms[COMUNICAR][TENSES_KEY].items()
        or0, or1 = paradigms[COMUNICAR][ROOTS_KEY]
        nr1 = re.sub('g$', 'gu', nr0)
    elif re.search('iuzar$', user_verb):
        tenses_items = paradigms[AFIUZAR][TENSES_KEY].items()
        or0, or1, or2, or3 = paradigms[AFIUZAR][ROOTS_KEY]
        nr1 = re.sub('uz$', 'uc', nr0)
        nr2 = re.sub('uz$', 'úz', nr0)
        nr3 = re.sub('uz$', 'úc', nr0)
    elif re.search('zar$', user_verb):
        tenses_items = paradigms[ABRAZAR][TENSES_KEY].items()
        or0, or1 = paradigms[ABRAZAR][ROOTS_KEY]
        nr1 = re.sub('z$', 'c', nr0)
    elif re.search('ar$', user_verb):
        tenses_items = paradigms[CANTAR][TENSES_KEY].items()
        or0 = paradigms[CANTAR][ROOTS_KEY][0]
    elif re.search('er$', user_verb):
        tenses_items = paradigms[VENDER][TENSES_KEY].items()
        or0 = paradigms[VENDER][ROOTS_KEY][0]
    elif re.search('ir$', user_verb):
        tenses_items = paradigms[PARTIR][TENSES_KEY].items()
        or0 = paradigms[PARTIR][ROOTS_KEY][0]

    if or0 and nr0:
        conjugate_from_paradigm = get_conjugate_from_paradigm(or0, or1, or2,
                                                              or3, nr0, nr1,
                                                              nr2, nr3)
        return get_conjugation(tenses_items, conjugate_from_paradigm)


def conjugate(user_verb: str, accusative: bool = False, dative: bool = False)\
        -> dict:
    """This function conjugates all forms of verb

    Besides if accusative or dative are True it adds the
    appropriate pronouns.
    """
    paradigms = load()
    return get_irregular_conjugation(paradigms, user_verb) or \
        get_regular_conjugation(paradigms, user_verb)
