# -*- coding: utf-8 -*-
# cfgmng.py

"""
Gestion fichiers de configurations (YAML)

pathfile : dreamtools/cfgmng.py

Repertoires par défaut
----------------------
.. note::
    * PROJECT_DIR/cfg/PROJECT_DIR/cfg/.log.yml : Fichier de configuration des logs
    * PROJECT_DIR/cfg/.app.yml : Fichier de configuration de l'application
    * PROJECT_DIR/cfg/categorie.yml : Fichier de liste définie par un code et un libelle
    * PROJECT_DIR/cfg/mailing.yml : Fichier de mails préparés
    * PROJECT_DIR/cfg/validators.yml : Fichier de validation(cf CERBERUS)
    * PROJECT_DIR/cfg/normalizor.yml : Fichier de normalization(cf CERBERUS)

Class CFBases
-------------
"""

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper, CSafeLoader as SafeLoader
except ImportError:
    from yaml import Loader, Dumper, SafeLoader

from . import tools
from . import profiler


class CFGEngine(object):
    """
    cfg engine
    """
    __dirpath = None

    @staticmethod
    def initial(baz_dir='cfg'):
        """

        :param str baz_dir:
        :return:
        """
        CFGEngine.__dirpath = profiler.path_build(tools.PROJECT_DIR, baz_dir)

    @staticmethod
    def working_directory(sub_dir):
        CFGEngine.initial()
        return profiler.path_build(CFGEngine.__dirpath, sub_dir)

    @staticmethod
    def loading(p, ref=None, m='r'):
        """
        Récupération des parametres de configuration du fichier <p> section <r>

        :param str p: Fichier de configuration
        :param str ref: référence parametres à récupérer, optionnel
        :param str m: bytes par defaut
        :return: configuration | None

        """
        config = None

        try:
            if profiler.file_exists(p):
                with open(p, mode=m) if 'b' in m else open(p, mode=m, encoding='utf-8') as cfg:
                    cfg = yaml.load(cfg, Loader=SafeLoader)
                    if type(cfg) == "dict":
                        cfg = dict(cfg)
                    elif type(cfg).__name__ == "list":
                        cfg = list(cfg)

                    config = cfg.get(ref) if ref else cfg
        except Exception as ex:
            print(f'[Chargement du fichier {p}:\n', ex)
        finally:
            return config

    @staticmethod
    def save_cfg(d, f, m="w"):
        """
        Enregistrement d' un fichier
        ========================================

        :param dict(str, list(str)) d: données à enregistrer
        :param str f: nom du fichier
        :param str m: default (write): mode "w|a", optional
        :return:
        """
        profiler.makedirs(profiler.dirparent(f))

        with open(f, m) if 'b' in m else open(f, mode=m, encoding='utf-8') as f_yml:
            yaml.dump(d, stream=f_yml, allow_unicode=True)

        return f


class CFGBases(CFGEngine):
    """
    Cette class permet de gere des fichiers de configuration disponibles dans le repertoire <PROJET_DIR>/cfg
    """
    CFG_DIR = CFGEngine.working_directory('')  # databases parameters
    _logs = profiler.path_build(CFG_DIR, 'log.yml')
    _app = profiler.path_build(CFG_DIR, 'app.yml')
    _categories = profiler.path_build(CFG_DIR, 'categorie.yml')
    _mail = profiler.path_build(CFG_DIR, 'mailing.yml')
    _validator = profiler.path_build(CFG_DIR, 'validators.yml')  # databases parameters
    _normalisator = profiler.path_build(CFG_DIR, 'normalizor.yml')  # databases parameters

    @staticmethod
    def loadingbyref(filename, *args, **kwargs):
        """
        Récupération des parametres de configuration du fichier <filename> section <r>

        :param str filename: Fichier de configuration
        :param str code: référence parametres à récupérer, optionnel
        :param str mode: bytes par defaut
        :return: configuration | None
        """
        filepath = profiler.path_build(CFGBases.CFG_DIR, f'{filename}.yml')
        return CFGEngine.loading(filepath, *args, **kwargs)

    @staticmethod
    def logs_cfg():
        """ Configuration des logs

        :Exemple:
            >>> import import logging.config as log_config
            >>> import logging
            >>> log_config.dictConfig(CFGBases.logs_cfg())
            >>> tracker = logging.getLogger('PROD|TEST')
            >>> tracker.info("Exemple dun message d'information")

        """

        return CFGBases.loading(CFGBases._logs)

    @staticmethod
    def app_cfg(code=None):
        """ Parametres application

        :param str code: clé a retourner (filtre)
        :return: Configuration
        """
        return CFGBases.loading(CFGBases._app, code)

    @staticmethod
    def validator():
        """ Parametres de validation de formulaire
        """
        return CFGBases.loading(CFGBases._validator)

    @staticmethod
    def normalizor():
        """ Parametres de normalisation de formulaire
        :return: parametres de normaisation
        :rtype: dict
        """
        return CFGBases.loading(CFGBases._normalisator)

    @staticmethod
    def mailing_lib(code):
        """ Mail préparé

        :param str code: référence du mail à envoyer
        :return: mail

        """
        return CFGBases.loading(CFGBases._mail, code)

    @staticmethod
    def categorie_lib(code=None):
        """ Liste de definition

        :param str code: référence du de la liste
        :return: liste(s) de categories
        :rtype: dict
        """
        return CFGBases.loading(CFGBases._categories, code)


_all_ = ['CFGBases']
