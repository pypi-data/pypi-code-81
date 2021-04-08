# -*- coding: utf-8 -*-
# dreamtools/dtemng.py

"""
Module de Gestion des date
=============================

Liste de fonction pour utilisation des dates
pathfile : dreamtools/tools

Constantes globales
-------------------

Liste des jours de la semaine
I_MON, I_TUES, I_WED,I_THU, I_FRI, I_SAT, I_SUN = 1, 2, 3, 4,5,6,0

Fonctions
-------------

"""

import locale
import time
from datetime import datetime, timedelta, date

import pytz

I_MON, I_TUES, I_WED, I_THU, I_FRI, I_SAT, I_SUN = 1, 2, 3, 4, 5, 6, 0

locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')

ISO_FORMAT = '%Y-%m-%dT%H:%M:%S'
FR_FORMAT = '%d/%m%/%Y'

FRM_ISO, FRM_TIMESTAMP = 'iso', 'ts'


def set_timezone(dt, tz=pytz.UTC):
    """ Applique la timezone indiquée à la date passée en parametre

    :param datetime dt: date
    :param timezone tz: timezone
    """
    return dt.replace(tzinfo=tz)


def datetime_from_utc_to_local(utc_datetime):
    """Convertie la date et heure donné (utc) en date local

    :param utc_datetime: datetime utc
    :return: date locale
    """
    return pytz.utc.localize(utc_datetime, is_dst=None).astimezone()


def datetime_from_local_to_utc(utc_datetime):
    """
    Convertie une date et heure local en heure utc

    :param datetime utc_datetime: datetime local
    :return: datatime utc
    """
    return utc_datetime.astimezone(pytz.utc)


def maintenant(utc=False, fm=None, tz=None):
    """ Date et heure de l'instant (Now)

        :param bool utc: Si True renvoie de l'heure UTC (GMT) ou l'heure local
        :param str fm: format date : fm == FRM_ISO (iso) | FRM_TIMESTAMP (ts)
        :param timezone tz: Timezone, None by def
        :rtype: datetime | string

        :Exemple:
            >>> maintenant ()
            datetime.datetime (2019, 06, 02, 17, 30, 43, 248622)
            >>> maintenant (True)
            '2019-06-02T17:30:43.248622'

    """
    d = datetime.utcnow()
    if not utc:
        d = pytz.utc.localize(d, is_dst=None).astimezone(tz)

    if fm == FRM_ISO:
        return d.isoformat()
    elif fm == FRM_TIMESTAMP:
        return dtets(d)
    else:
        return d


def utcnow_iso():
    """Date et heure actuelle utc au format iso
    :return: date utc
    """
    return maintenant(True, FRM_ISO)


def utcnow_ts():
    """Date et heure actuelle utc au format timestamp
    :return: timestamp
    """
    return maintenant(True, FRM_TIMESTAMP)


def datestr(dte=None, fm='%Y-%m-%dT%H:%M:%S'):
    """ Convertit une date en chaine selon un format donnée

    :param datetime dte: date à convertir date du jour par défaut
    :param str fm: format désirée, defaults to  '%d/%m/%Y'
    :return: Renvoie un chaine correspondant au format date passé en parametre
    :rtype: str

    :Exemple:
        >>> d = maintenant ()
        >>> datestr (d, '%d.%m.%Y')
        02.06.2019

    """

    if dte is None:
        dte = maintenant()

    return dte.strftime(fm)
  

def today(fm='%d/%m/%Y'):
    """ Renvoie la date du jour

        :param str fm: Format de la date attendu
        :rtype: str

        :Exemple:
            >>> today ()
            '02/06/2019'
            >>> today('%d.%m.%Y')
            '02.06.2019'

        """

    return datestr(fm=fm)


def date_dayed(dte=None, b=True):
    """ Positionne la date indiquée à minuit au matin ou au soir

    :param datetime dte: Date
    :param bool b: Date debut de jour (00:00:00.000) ou
        date de fin de journee date du jour + 1 (minuit) soit lendemin à 00

    :Example:
        >>> date_dayed()
        datetime.datetime(2020, 12, 19, 0, 0,datetime.datetime(2020, 12, 19, 0, 0)

    """

    if dte is None:
        dte = maintenant()

    dte = dte.replace(hour=0, minute=0, second=0, microsecond=0)

    return dte if b else dateadd(dte, 1)


def get_time(dte):
    """ Renvoie d'une date au format time
    :param datetime dte:
    :rtype: time
    """
    return dte.time()


def get_date(p_year, p_month, p_day):
    """Generationd'une date a partir des valeur numerique

    :param int p_year: année
    :param int p_month: mois
    :param int p_day: date jour
    :rtype: datetime
    """
    return date(p_year, p_month, p_day)


def tsdate(ts):
    """ Conversion timestamp - date

        :param ts: temps en milliseconde depuis 1970
        :return: date
    """
    return datetime.fromtimestamp(int(ts))  # => renvoie datetime


def tstring(ts, fm='%Y.%m.%d-%H:%M (%a)'):
    """
     Conversion timestamp - chaine(str)

     :param int ts: timestamp
     :param str fm: format attendu
     :rtype: str
    """
    return datestr(tsdate(ts), fm)


def dtets(dte=None):
    """ Conversion date - timestamp

    :param date dte: date à convertir
    :return int: date en miliseconde (sans les ms)
    """
    if dte is None:
        dte = maintenant()

    return int(dte.timestamp())  # int => sans les ms


def strdate(dte, fm='%d-%m-%Y %H:%M:%S'):
    """ Conversion string - date

    :param str dte: date
    :param str fm: formayt, default '%d-%m-%Y %H:%M:%S': patterne, optional

    :return: Renvoie la date convertit ou None en cas d'invalidité (date non conform)
    :rtype: datetime

    :Exemple:
        >>> s = '24-O2-1976 16:45'
        >>> strdate (s, '%d-%m-%Y %H:%m')
        datetime.datetime(1976,02,24,16,45)

    """

    return datetime.strptime(dte, fm)


def isotodate(dte):
    """ Conversion str_iso - date

    Format ISO : YYYY-MM-DDTHH:MN
    :param dte:

    :return:
    """
    return strdate(dte, fm=ISO_FORMAT)


def datepaques(y):
    """Dates Pâques d'une année donnée

    * Lundi de paque : lundi suivant le dimanche de paque (La Pâque)
    * Jeudi de l'ascension : 3 jour après paques
    * pentecote : 49 jours après le lundi de paques

    :param int y: année de référence
    :rtype: list[date]
    """
    y = int(y)

    a = y // 100
    b = y % 100

    c = (3 * (a + 25)) // 4
    d = (3 * (a + 25)) % 4
    e = (8 * (a + 11)) // 25

    f = (5 * a + b) % 19
    g = (19 * f + c - e) % 30
    h = (f + 11 * g) // 319

    j = (60 * (5 - d) + b) // 4
    k = (60 * (5 - d) + b) % 4

    m = (2 * j - k - g + h) % 7
    n = (g - h + m + 114) // 31
    p = (g - h + m + 114) % 31

    jour = p + 1

    mois = n

    dte_paques = date(y, mois, jour)
    lundi_pak = dte_paques + timedelta(days=1)
    jeudi_ascension = dte_paques + timedelta(days=39)
    pentecote = lundi_pak + timedelta(days=49)

    return [dte_paques, lundi_pak, jeudi_ascension, pentecote]


def jours_feries(y=None):
    """ Jour fériés pour une date donnée

    :param int y: Année de référence (optionnel), default : année en cours
    :return: un tableau de date de jours fériés

    :Exemple:
        >>> jours_feries ()		#Jours fériés année en cours
        >>> jours_feries (2018)	# jours fériés année 2018

    """

    y = maintenant().year if y is None else int(y)

    dt_feries = datepaques(y)

    dt_feries.append(date(y, 1, 1))  # jour de l'y
    dt_feries.append(date(y, 5, 1))  # fete du travail
    dt_feries.append(date(y, 5, 8))  # jour victoire
    dt_feries.append(date(y, 7, 14))  # fete national
    dt_feries.append(date(y, 8, 15))  # assomption
    dt_feries.append(date(y, 11, 1))  # toussain
    dt_feries.append(date(y, 11, 1))  # armistice
    dt_feries.append(date(y, 12, 25))  # noel

    return dt_feries


def is_workday(dte):
    """ Determine si la date est un jour ouvré ou vaqué (week-end / fériés)

    :param dte: date à évaluer
    :return: renvoie le statut jour ouvré (true=ouvré)
    :rtype bool:
    """
    feries = jours_feries(dte.year)
    return not (dte in feries or dte.weekday() in [I_SAT, I_SUN])


def dateadd(dte, nb, fm='d'):
    """ Ajoute un nombre de jours données à une date

    :param date dte: date de départ
    :param int nb: nombre de jour à additionner (valeur négative/positive)
    :param str fm: * days (default), * h (hours), * m (minutes)

    :rtype: datetime

    """
    if fm == 'h':
        return dte + timedelta(hours=nb)
    elif fm == 'm':
        return dte + timedelta(minutes=nb)
    else:
        return dte + timedelta(days=nb)


def timeadd(dte, nb):
    """  Ajoute un nombre d'heure données à une date

    :param date dte: date de départ
    :param int nb: nombre de jour à additionner (valeur négative/positive)

    :return: date de depat + nombre de jours
    """
    return dateadd(dte, nb, 'h')


def date_add_workday(dte, nb):
    """ Ajoute un nombre de jours ouvrés donnés à une date

        :param datetime dte: date de référence
        :param int nb: nombre de jour à additionner (valeur négative/positive)
        :return: date de depat + nombre de jours
    """
    while nb > 0:
        dte = dateadd(dte, 1)
        if is_workday(dte):
            nb -= 1

    return dte


def dtediff(dtea, dteb):
    """ Calcul du nombre de jours entre deux dates

    :param datetime dtea: date à comparer
    :param datetime dteb: date à comparer
    :rtype: int
    """
    t = dteb - dtea
    return abs(t.days)


def dtecompare(dtea, dteb):
    """ Compare si dateb es supérieur à la datea

    :param datetime dtea: date à comparer
    :param datetime dteb: date à comparer
    :retur: 0 si les dates sont égale, -1 si la dateb est antérieur à datea 1 le c&s inverse
    :rtype: int
    """
    t = dteb - dtea

    if t.days == 0:
        return t.days
    elif t.days < 0:
        return -1
    else:
        return 1


def get_weeks_num(dte=None):
    """Renvoie le numéro de la date indiqué (now par deafut)"""
    if dte is None:
        dte = maintenant()

    return dte.isocalendar()[1]


def fullmonth(dte):
    """ Renvoie la date du jour au format MOIS YYYY

    :param datetime dte:
    :rtype: str
    """
    return datestr(dte, "%B %Y")


def date_rss(dte=None,short=False):
    """Dtate au format RSS """
    ctime = time if dte is None else time.mktime(dte.timetuple())
    return ctime.strftime('%a %d %b %Y') if short else ctime.strftime('%a, %d %b %Y %H:%M:%S %z')


def day_in_sec(dy, ml=False):
    """
    Convertion d'un nombre de jours en secondes ou milisecondes

    :param int dy: nombre de jours
    :param bool ml: en millisecondes si True sinon en secondes, dafault False
    :return: (milli) secondes
    """
    nb = int(dy)
    nb = nb * 24 * 60 * 60

    return nb * 1000 if ml else nb


def day_in_hour(dy):
    """ Convertion d'un nombre de jours en heure

    :param int dy: nombre de jours
    :rtype: int
    """
    nb = int(dy)
    return nb * 24
