#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __main__.py

import shutil
import sys

import pkg_resources

from dreamtools import tools, profiler


def setproject():
    """
    Intialisation du projet
    """

    base = profiler.dirproject()
    dest = profiler.path_build(base, 'cfg')

    print('**************************************************************************')
    print('** Création architecture')
    print('** -----------------------------------------------------------------------')
    print('** Répertoire logs ')
    profiler.makedirs(profiler.path_build(base, 'logs'))
    print('**\t>> Répertoire créé : ', profiler.path_build(base, 'logs'))
    print('** Répertoire configuration')
    src = pkg_resources.resource_filename('dreamtools', 'cfg')
    shutil.copytree(src, dest)
    print('**\t>> Répertoire créé : ', dest)
    src = pkg_resources.resource_filename('dreamtools', '.env')
    dest = profiler.path_build(base, '.env')
    shutil.copyfile(src, dest)
    print('**\t>> environneemet créé : ', dest)
    print('**=======================================================================-')


if __name__ == "__main__":
    sys.exit(setproject())
