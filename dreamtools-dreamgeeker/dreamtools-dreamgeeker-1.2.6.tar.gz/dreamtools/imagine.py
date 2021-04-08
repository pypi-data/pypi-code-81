# !/usr/bin/python3
# -*- coding: utf-8 -*-
# project/dreamtools/imagine.py

import os
from io import BytesIO

from PIL import Image
from PIL.ExifTags import TAGS
from PIL.TiffImagePlugin import ImageFileDirectory_v2

from . import (tools, profiler)
from .logmng import CTracker

TYPE_IMG_JPEG = 'JPEG'
TYPE_IMG_PNG = 'PNG'
TYPE_IMG_GIF = 'GIF'

"""
Class CImagine
=============================

Class permettant le traitement d'une image png convertit en jpg avec prise en charge de la transparence (fond blanc)


pathfile : dreamtools/pyimaging

"""


class CImagine(object):

    def __init__(self, src, dest, with_ext=False):
        """
        Preparation image  pour traitement
        ==================================
        Les images sont convertit au format JPEG

        :parametres:
        :param str src: pathfile image d'origine
        :param src dest: path destionantion image
        :param bool with_ext: Avec ou sans extension, False par défaut
        """

        self.img = Image.open(src)
        self.exif = None

        if self.img.mode != 'RGB':
            self.img = self.img.convert('RGB')

        self._size = self.img.size
        self.format = self.img.format

        if self.format != TYPE_IMG_JPEG:
            try:
                self.img = self.white_background
            except Exception as ex:  # pas de fond transparent
                tools.print_err("imagine.init Ajout fond blanc", ex)

        self.file = profiler.file_ext_less(dest)     # on s'assure de retirer l'extension

        if with_ext:
            self.file += '.jpg'

        self.thumb = (200, 200)

        self.min_size = 250
        self.max_size = 500

    def __enter__(self):
        return self

    @property
    def _size(self):
        return self.w, self.h

    @_size.setter
    def _size(self, s):
        self.w, self.h = s

    @property
    def white_background(self):
        """
        Ajout d'un fond transparent
        :return:
        """
        bg = Image.new("RGB", self._size, (255, 255, 255))
        bg.paste(self.img, self.img)

        return bg

    def resize(self, s=None, mn=None, mx=None):
        """ Redimensionnement de l'image au format jpg

        :param tuple(int, int) s: si indiqué, (w,h) de redimensionnement
        :param int mn,optional: taille maximum (carré), default 250
        :param int mx,optional: taille maximum de l'image,  default 250
        :return:
        """

        if s is None:
            min_size = mn or self.min_size
            max_size = mx or self.max_size

            h = self.h
            w = self.w

            if self.w >= self.h:
                if not (min_size <= self.w <= max_size):
                    s_ref = min_size if self.w < min_size else max_size
                    h = self.h * s_ref / self.w
                    w = s_ref
            elif not (min_size <= self.h <= max_size):
                s_ref = min_size if self.h < min_size else max_size
                w = self.w * s_ref / self.h
                h = s_ref

            s = (int(w), int(h))

        img = self.img.resize(s)
        img.save(self.file, TYPE_IMG_JPEG)

    def thumbed(self, s=None):
        """ Thumb Image

        :param tuple[int, int] s: taille image, defaul (200, 200à

        """

        img = self.img.convert('L')
        img.thumbnail(s or self.thumb)

        if self.exif:
            img.save(self.file + ".thumb", TYPE_IMG_JPEG, exif=self.exif)
        else:
            img.save(self.file + ".thumb", TYPE_IMG_JPEG)

    def __exit__(self, exc_type, exc_value, traceback):
        self.img.close()

    def protected(self, artist, description):
        """Ajoute un nom d'artist et le copyright d'une image"""

        _TAGS_r = dict(((v, k) for k, v in TAGS.items()))

        # Image File Directory
        ifd = ImageFileDirectory_v2()
        ifd[_TAGS_r["Artist"]] = artist
        ifd[_TAGS_r["Copyright"]] = 'Tous droits reserves'
        ifd[_TAGS_r["Description"]] = description

        out = BytesIO()
        ifd.save(out)

        self.exif = b"Exif\x00\x00" + out.getvalue()
        self.img.save(self.file, TYPE_IMG_JPEG, exif=self.exif)

    @classmethod
    def treat_dir(cls, s):
        """
        Redimensionne toutes les images contenu dans un répertoire donné + thumb
        :param s:
        """
        for f in os.listdir(s):
            f_path = os.path.join(s, f)
            if os.path.isfile(f_path):
                cls.treat_img(f_path, f_path)

    @classmethod
    def treat_img(cls, s, f):
        """
        Enregistre une image, la reformat + thumb
        :param s:
        :param f:
        """
        o = cls(s, f)
        o.resize()
        o.thumbed()

    @classmethod
    def imgrecorder(cls, fs, fp):
        """
        Enregistremetn d'une image uploaded (byte)

        :param file fs: filestream from flask request
        :param str fp: filepath d'enregistrement
        :return:
        """
        import uuid

        tmp = uuid.uuid1().int >> 64
        tmp = profiler.path_build(tools.TMP_DIR, str(tmp))

        profiler.makedirs(tools.TMP_DIR)

        try:
            CTracker.flag(f'[tools.imgrecorder] Image temp recording : {tmp}')
            fs.save(tmp)

            CTracker.flag(f'[tools.imgrecorder] Image treatment: {tmp} | {fp}')
            o = cls(tmp, fp)
            CTracker.flag(f'[tools.imgrecorder] Image resizing: {fp}')
            o.resize()
            CTracker.flag('[tools.imgrecorder] Image thumbing')
            o.thumbed()

            CTracker.flag('[tools.imgrecorder] Temp Cleaning')
            return True
        except Exception as e:
            CTracker.exception_tracking(e, '[tools.imgrecorder] Aïe')
            profiler.remove_file(tmp)
            return False
