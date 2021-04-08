#!/usr/bin/python3
# -*- coding: utf-8 -*-
# krypt.py

"""
Module de cryptage
=========================================
pathfile : dreamtools/tools

Pré-Requis
----------------------
Une clé privé et un grain de sel doivent être défini dans le fichier "de parapetre d'application"
**PROJECT_DIR/cfg/.app.yml**
* SECRET_KEY
* SALT_EXT

*Méthode* : sha-512`

Class CKrypting
----------------
"""

import crypt
import os


class CKrypting:
    """
    Gestion kryptage des données
    """
    PREFIX = "$5$"
    SALT = os.getenv('SECRET_KEY')
    SALT_EXT = os.getenv('EXTERN_SECRET_KEY')

    @staticmethod
    def __encrypt(ch, prefix):
        if isinstance(ch, bytes):
            orig = ch
            try:
                ch = ch.decode("utf-8")
            except UnicodeDecodeError:
                return None
            assert ch.encode("utf-8") == orig, "utf-8 spec says this can't happen!"

        return crypt.crypt(ch, prefix)

    @staticmethod
    def encrypt(ch):
        """Crypte une chaine selon la clé privé et le grain de sel paramétrés

        :param str ch: Chaine à crypter
        :return str: Chaine cryptée

        """

        return CKrypting.__encrypt(ch, CKrypting.PREFIX + CKrypting.SALT)

    @staticmethod
    def extern_encrypt(ch):
        """
        Cryptage chaine pour utilisation extrene (suppression prefix)

        :param str ch:
        :return: mot de passe crypté - grain de sel
        """
        """This is used in place of `mkpasswd --sha-512`"""
        s = CKrypting.__encrypt(ch, CKrypting.PREFIX + CKrypting.SALT_EXT)
        i = len(CKrypting.SALT_EXT)

        return s[i:]

    @staticmethod
    def compare(enc, s):
        """Comparaison d'un chaine en clair à un mot de passe crypté

        :param str enc: chaine cryptée
        :param str s: chaine en claire
        :rtype: bool

        """
        return crypt.crypt(s, enc) == enc
