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

PARADIGM_KEY = 'paradigm'
ROOTS_KEY = 'roots'
SUFFIX_KEY = 'suffix'
VERBS_KEY = 'verbs'
TENSES_KEY = 'tenses'

FN_KEY = 'fn'
PI_KEY = 'pi'
II_KEY = 'ii'
IA_KEY = 'ia'
IP_KEY = 'ip'
EI_KEY = 'ei'
MI_KEY = 'mi'
TI_KEY = 'ti'
FI_KEY = 'fi'
PS_KEY = 'ps'
IS_KEY = 'is'
FS_KEY = 'fs'
IN_KEY = 'in'


def load() -> dict:
    """This function loads all irregular_verbs stored in Conshuga's verbs.txt
    """
    from os import path

    package_path = path.dirname(__file__)
    verbs_file = path.join(package_path, 'verbos.txt')

    with open(verbs_file, 'r', encoding='utf8') as f:
        irregular_verbs = {}

        # READING VERBS PARADIGM FILE
        line = f.readline()
        while line:
            # PARADIGMS
            if line.startswith('paradigma'):
                paradigm = line.strip()[11:-1]

                line = f.readline()
                roots = None
                suffix = None
                cfn = None
                cpi = None
                cii = None
                cia = None
                cip = None
                cei = None
                cmi = None
                cti = None
                cfi = None
                cps = None
                cis = None
                cfs = None
                cin = None
                verbs = None
                while line and not line.startswith('paradigma'):
                    # RAICES
                    if line.startswith('raiz'):
                        roots = line.strip()[6:].replace('<', '')\
                                .replace('>', '').split(':')
                    # SUFIXO
                    if line.startswith('sufixo'):
                        suffix = line.strip()[7:].replace('<', '')\
                            .replace('>', '')
                    # FN
                    if line.startswith('FN'):
                        cfn = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # PI
                    if line.startswith('PI'):
                        cpi = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # II
                    if line.startswith('II'):
                        cii = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # IA
                    if line.startswith('IA'):
                        cia = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # IP
                    if line.startswith('IP'):
                        cip = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # EI
                    if line.startswith('EI'):
                        cei = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # MI
                    if line.startswith('MI'):
                        cmi = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # TI
                    if line.startswith('TI'):
                        cti = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # FI
                    if line.startswith('FI'):
                        cfi = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # PS
                    if line.startswith('PS'):
                        cps = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # IS
                    if line.startswith('IS'):
                        cis = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # FS
                    if line.startswith('FS'):
                        cfs = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # IN
                    if line.startswith('IN'):
                        cin = line.strip()[3:].replace('<', '')\
                            .replace('>', '').split(':')
                    # Paradigm verbs
                    if line.startswith('<'):
                        verbs = line.strip().replace('<', '').replace('>', '')\
                            .split(',')

                    line = f.readline()

                paradigm = {
                    PARADIGM_KEY: paradigm,
                    ROOTS_KEY: roots,
                    SUFFIX_KEY: suffix,
                    VERBS_KEY: verbs,
                    TENSES_KEY: {
                        FN_KEY: cfn,
                        PI_KEY: cpi,
                        II_KEY: cii,
                        IA_KEY: cia,
                        IP_KEY: cip,
                        EI_KEY: cei,
                        MI_KEY: cmi,
                        TI_KEY: cti,
                        FI_KEY: cfi,
                        PS_KEY: cps,
                        IS_KEY: cis,
                        FS_KEY: cfs,
                        IN_KEY: cin
                    }
                }

                for verb in verbs:
                    irregular_verbs[verb] = paradigm
            else:
                line = f.readline()

    return irregular_verbs
