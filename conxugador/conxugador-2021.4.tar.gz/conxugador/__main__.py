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

import argparse
from conxugador.conjugation import conjugate
from conxugador.load_paradigms import TENSES_KEY, FN_KEY, PI_KEY, II_KEY, \
                            IA_KEY, IP_KEY, EI_KEY, MI_KEY, TI_KEY, FI_KEY, \
                            PS_KEY, IS_KEY, FS_KEY, IN_KEY

COLON = ':'


def print_conjugation(conjugation: dict):
    """This function prints a conjugation"""
    print(FN_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][FN_KEY]))
    print(IP_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][IP_KEY]))
    print(PI_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][PI_KEY]))
    print(II_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][II_KEY]))
    print(EI_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][EI_KEY]))
    print(MI_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][MI_KEY]))
    print(TI_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][TI_KEY]))
    print(FI_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][FI_KEY]))
    print(PS_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][PS_KEY]))
    print(IS_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][IS_KEY]))
    print(FS_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][FS_KEY]))
    print(IA_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][IA_KEY]))
    print(IN_KEY.upper() + COLON + COLON.join(conjugation[TENSES_KEY][IN_KEY]))


def main():
    print('Conxugador Copyright (C) 2021 Andrés Vieites Pérez\n\
This program comes with ABSOLUTELY NO WARRANTY; for details read COPYING.\n\
This is free software, and you are welcome to redistribute it.\n')
    parser = argparse.ArgumentParser(prog="conxugador", description="Galician \
        conjugator")
    parser.add_argument("verb", type=str, help='the verb which will be \
        conjugated')
    parser.add_argument("-a", "--accusative", action="store_true", help='if \
        present it adds accusative pronouns')
    parser.add_argument("-d", "--dative", action="store_true", help='if present \
        it adds dative pronouns')
    args = parser.parse_args()

    verb_conjugation = conjugate(args.verb, args.accusative, args.dative)
    print_conjugation(verb_conjugation)

if __name__ == "__main__":
    main()
