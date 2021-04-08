# -*- coding: utf-8 -*-
import fnmatch
import os

"""Ensemble de fonctions sur fichiers / repertoire"""


def filerecorder(doc, fp, b=False):
    """ Enregistrement d'un fichier

    Le chemin du filpath sera construit si besoin

    :param  doc: données à enregistrer
    :param str fp: filepath
    :param boolean b: données en byte ?, optional
    :return:
    """
    makedirs(dirparent(fp))  # Check dir exists

    with open(fp, 'wb') if b else open(fp, 'w', encoding='utf-8') as f:
        f.write(doc)


def fileloader(fp, b=False):
    """ Chargement d'un fichier

    :param fp: filepath du fichier recherché
    :param bool b: données en byte(False)  ? optional
    :return: document
    """
    with open(fp, 'rb') if b else open(fp, 'r') as f:
        return f.read()


def dirproject():
    """ Répertoire d'execution """
    return os.getcwd()


def dirparent(path):
    """  Renvoie du repertoire parent

    :param str path: repertoire
    :rtype: str

    """
    return os.path.dirname(os.path.realpath(path))


def dircurrent(source=None):
    """Répertoire pour le fichier en cours """
    return dirparent(source or __file__)


def dirparser(directory, pattern="*"):
    """Récupération des fichiers d'un répertoire

    :param str directory: repertoire
    :param str pattern: '*' pour tous type de fichier par défaut

    :Exemple:
        >>> directory = '/home/user/Documents'
        >>> pattern='*.txt'
        >>> for filename, path_file in dirparser(directory, pattern):
        ...    print(path_file)
        'home/user/Documents/fichier.txt'
        'home/user/Documents/autre_fichier.txt'
    """

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                yield filename, os.path.join(root, filename)


def path_build(directory, ps_complement):
    """ Construction d'un pathfile

    :param str directory: repertoire
    :param str ps_complement: complement permettant de generer le chemin
    :rtype: str

    :Exemple:
        >>> path = 'home/user/Documents'
        >>> path_build(path, '../other_dir')
        'home/user/Documents/other_dir'
    """
    return os.path.abspath(os.path.join(directory, ps_complement))


def file_ext(ps_file):
    """ Retrourne l'extension d'un fichier

    :param ps_file:
    :return: Extension de fichier
    """
    return os.path.splitext(ps_file)[1]


def file_ext_less(ps_file):
    """ Retrourne le fichier sans extension

    :param ps_file:
    :return: Extension de fichier

    Example
    ----------
        >>> f = 'filename.ext'
        >>> file_ext_less(f)
        filename
    """
    return os.path.splitext(ps_file)[0]


def file_exists(fp):
    """Vérifie l'existance d'un fichier

    :param str fp: filepath
    :rtype bool:
    """

    return os.path.exists(fp)


def makedirs(path):
    """ Création du répertoire données

    :param path: chemin du répertoire à créer
    :rtype bool:

    """

    if not file_exists(path):
        os.makedirs(path)
        return file_exists(path)

    return True


def remove_file(p):
    """ Suppression d'un fichier si existant

    :param str p: chemin complet du fichier à supprimer
    """
    if file_exists(p):
        os.remove(p)


def clean_directory(directory, pattern='*'):
    """ Supprimes tous les élements d'un repertoire

    :param str directory: chemin du repertoire
    :param string pattern: patter des fichier à supprimer (filtre)
    :return int: nombre de fichier supprimer

    """
    i_count = 0

    for filename, path_file in dirparser(directory, pattern):
        remove_file(path_file)
        i_count += 1
    return i_count
