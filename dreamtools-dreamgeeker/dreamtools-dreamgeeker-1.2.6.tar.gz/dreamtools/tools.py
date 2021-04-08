# -*- coding: utf-8 -*-

"""
Module de fonctions basiques
=============================

Liste de fonctions utiles

pathfile : dreamtools/tools

Constantes globales
--------------------
.. note::

    * RGX_ACCENTS = 'àâäãéèêëîïìôöòõùüûÿñç'
    * RGX_EMAIL = Expression reguliere email
    * RGX_PUNCT = Caractere speciaux autorisé pour mot de passe
    * RGX_PWD = Expression régulière pour un mot de passe de 8 à 12 avec un car.Special/une Majuscule/Une minuscule
    * RGX_PHONE = Expression réguliere remative à un numéro de téléphon
    * RGX_URL = expression reguliere pour URL
    * *PROJECT_DIR*  : Repertoire du projet
    * *APP_NAME* : Nom de l'application
    * *APP_DIR* : PROJECT_DIR/APP_NAME
    * *TMP_DIR* : PROJECT_DIR/tmp

.. warning::
    Il faut configurer l'application afin d'avoir accès au variable PROJECT_DIR, APP_NAME, TMP_DIR

    >>> from dreamtools import config
    >>> from dreamtools import tools
    >>> config.CConfig('monapp')
    >>> print (tools.APP_DIR)
    '../PROJECT/mon_app'

"""

import ast
import re
import sys
from random import choice, randint
from string import punctuation, ascii_letters, digits

RGX_ACCENTS = 'àâäãéèêëîïìôöòõùüûÿñç'
RGX_EMAIL = r'^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$'
RGX_PUNCT = '#!?$%&_@*+-'
RGX_PWD = fr'.*(?=.{{8,12}})(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[{RGX_PUNCT}]).*'
RGX_PHONE = r'^0[1-9]\d{8}$'
RGX_URL = r'https?:\/\/(www\.)?[-a-z0-9@:%._\+~#=]{1,256}\.[a-z0-9()]{1,6}\b([-a-z0-9()@:%_\+.~#?&//=]*)'

APP_NAME = ''
PROJECT_DIR = ''
APP_DIR = ''
TMP_DIR = ''


def print_err(*args, **kwargs):
    """Ecriture sur le flux erreur de la console

    :param args: arguments 1
    :param kwargs: arguemnts2
    """
    print(*args, file=sys.stderr, **kwargs)


def string_me(v):
    """ Convertion d'une valeur en chaine

    :param v: valeur à convertir
    :rtype: str, None en cas d'erreur

    """

    try:
        return str(v)
    except:
        return None


def clean_space(ch):
    """ Nettoyage des espaces "superflus"

    * Espaces à gouche et à droite supprimés
    * Répétition d'espace réduit

    :Exemple:
        >>> chaine = 'Se  réveiller au matin        de sa destiné    ! !           '
        >>> clean_space (chaine)
        'Se réveiller au matin  de sa destiné ! !'

    """
    s = string_me(ch)
    return re.sub(r'\s{2,}', ' ', s.strip())


def clean_allspace(ch, very_all=True):
    """Nettoyage de tous les espace et carateres vides

    :param str ch: Chaine à nettoyer
    :param bool very_all: caractère vide aussi, True (False = Espaces uniquement)

    :Exemple:
        >>> chaine = 'Se  réveiller au matin        de sa destiné !'
        >>> clean_allspace (chaine)
        'Seréveilleraumatindesadestiné!'

    """
    c = r'\s' if very_all else '[ ]'
    s = string_me(ch)

    return re.sub(c, '', s.strip())


def clean_coma(ch, w_punk=False):
    """ Supprime les accents/caractères spéciaux du texte source en respectant la casse

    :param ch: Chaine de caractere à "nettoyer"
    :param w_punk: indique si la punctuation est à nettoyer ou pas (suppression)

    :Exemple:
        >>> s = 'Se  réveiller au matin    de sa destiné !!'
        >>> clean_coma (s)
        'Se seveiller au matin (ou pas) de sa destine !!''
        >>> clean_coma (s, True)
        'Se reveiller au matin ou pas de sa destine'

    """

    if w_punk:
        # Nettoyage caractere spéciaux (espace...)
        o_rules = str.maketrans(RGX_ACCENTS, 'aaaaeeeeiiioooouuuync', punctuation)
    else:
        o_rules = str.maketrans(RGX_ACCENTS, 'aaaaeeeeiiioooouuuync')

    return clean_space(ch).translate(o_rules).swapcase().translate(o_rules).swapcase()


def clean_master(ch):
    """ Supprime les accents, caractères spéciaux et espace du texte source

    :param str ch: Chaine de caractere à "nettoyer"
    :return str: chaine sans accents:car. spéciaux ni espace en minuscule

    :Exemple:
        >>> s = 'Se  réveiller au matin  (ou pas) de sa destiné !'
        >>> clean_master (s)
        'sereveilleraumatinoupasdesadestine

    """
    return clean_allspace(clean_coma(ch, True)).lower()


def inttohex(v):
    """ Conversion d'une valeur en hexadécimal

    :param int v: nombre à convertir
    :returns: valeur en hexadécimal
    :rtype: str

    """

    return hex(int(v))


def addhex(h, v):
    """Additionne une valeur hexadécimal

    :param str h: valeur hexadécimal
    :param int v: valeur entière à ajouter
    :return: valeur additionné en hexedécimal

    :Example:
        >>> hx = '0x129'
        >>> addhex(hx, 2)
        0x12b

    """

    v += int(h, 16)
    return hex(v)


def plain_hex(hx, s=3):
    """ Complète un chiffre hexadecimal en préfixant une valeur de zéro

    :param str hx: valeur hexadécimal
    :param int s: longeur chaine attendu
    :rtype: str:

    :Examples:
        >>> hx = '0x129'
        >>> plain_hex(hx, 5)
        0x00129

    """
    return hx[:2] + plain_zero(hx[2:], s)


def plain_zero(v, s):
    """Complete une valeur chaine de zéro

    :param v: valeur à completer
    :param s: taille chaine attendu préfixé de zerom

    :Exemple:
        >>> d = 5
        >>> plain_zero(d,3)
        '005'

    """

    s = '{:0>' + str(s) + '}'
    return s.format(v)


def check_password(s):
    """ Vérifie que la syntaxe d'une chaine répond au critère d'un mot de passe

    :Conditions:
        * Une majuscule
        * Une minuscule
        * Un chiffre
        * Un carectère spécial (@#!?$&-_ autorisé )

    :param str s: chaine à vérifier
    :return bool: True si la chaine est valide
    """
    r = re.compile(RGX_PWD)
    return r.match(s)


def comphex(hx_a, hx_b):
    """Compare deux valeurs  hexadécimales

    :param str hx_a:
    :param str hx_b:

    :return int:
        * 0 : hx_a == hx_b
        * 1 : hx_a > hx_b
        * -1 : hx_a < hx_b
    """
    v = int(hx_a, 16) - int(hx_b, 16)

    if v == 0:
        return 0
    else:
        return -1 if v < 0 else 1


def pwd_maker(i_size=8):
    """ Génération d'un password respectant les regles de password

    :Conditions:
        * Une majuscule
        * Une minuscule
        * Un chiffre
        * Un carectère spécial (@#!?$&-_ autorisé )

    :param int i_size: Nombre de caracteres de la chaine
    :return: Mot de passe
    """

    t = list(ascii_letters + digits + RGX_PUNCT)

    while True:
        s_chaine = ''
        for i in range(0, i_size):
            s = choice(t)
            s_chaine += s
            t.remove(s)
        if check_password(s_chaine):
            break

    return s_chaine


def code_maker(i_size=4):
    """Génération d'une chaine aléatoire composé de lettre et de chiffres

    :param int i_size: taille du code
    :rtype str:
    """
    ll = list(ascii_letters + digits)
    s = ''

    for i in range(0, i_size):
        s += choice(ll)

    return s


def aleatoire(end, s=1):
    """ Génération d'un nombre aléatoire entre [1-end] => end caractère

    :param int end: valeur maximal (paut indiquer la taille si s=1)
    :param s: valeur de départ, default to 1
    :return: Un chiffre aléatoire

    :Exemple:
        >>> aleatoire (5)
        1 : Renvoie un chiffre entre 1 et 5
        >>> aleatoire (5,3)
        1 : Renvoie un chiffre entre 3 et 5
        >>> 4

    """

    return randint(s, end)


def add_list(v, ll):
    """ Ajout d'un item dans une liste avec gestion des doublons

    :param str v: valeur à ajouter
    :param list ll: liste

    """
    if v not in ll:
        ll.append(v)


def dictlist(k, v, d):
    """ Ajout d'un valeur dans une liste d'un dictionnaire

    :param str k: clé dictionnaire
    :param v: valeur à ajouter
    :param dict[str, list[]] d: dictionnaire

    :Exemple:
        >>> dictionnaire= {}
        >>> dictlist('printemps', 'mar', dictionnaire)
        dictionnaire{'printemps', ['mars']}
        >>> dictlist('printemps', 'avril', dictionnaire)
        dictionnaire{'printemps', ['mars', ''avril']}
        >>> dictlist('printemps', 'mars', dictionnaire)
        dictionnaire{'printemps', ['mars', ''avril']}

    """
    if k is None or v is None: return

    if k not in d: d[k] = []

    add_list(v, d.get(k))


def str_dic(chaine):
    """Convertion d'une chaine en dictionnaire

    :param str chaine:
    :rtype: dic

    :Exemple:
        >>> s_dic = "{'key':value}"
        >>> str_dic(s_dic)
        {'key': 'value'}

    """

    return ast.literal_eval(chaine)


def pop_dic(l_ids, dic):
    """ Suppression d'une liste d'éléments d'un dictionnaire

    :param list[str] l_ids : liste de clé à supprimer
    :param dict[str:object] dic: dictionaire à nettoyer

    """
    if dic:
        for s in l_ids:
            if s in dic: del dic[s]

def dicFindKey (value, dic):
    """Recherche une clé d'un dictionnaire à partir de sa valeur"""
    for k, v in dic.items():
        if v == value:
            return k
    else:
        return None


def htmltexted (texte):
    import bs4

    try:
        bs = bs4.BeautifulSoup(texte, features="html.parser")
        texte = bs4.UnicodeDammit(bs.get_text()).unicode_markup
    except:
        pass
    finally:
        return clean_space(texte)