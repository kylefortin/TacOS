"""
===========
TacOS Tools
===========

Contains various global tools and utilities for the TacOS application.

"""

import datetime
import pickle
from Objects import Config


def now():
    return str(datetime.datetime.now())

def group(n, l):
    """
    Group a list into n tuples.
    :param n: Qty to group by.
    :type n: int
    :param l: List to group.
    :type l: list
    :return: A list of tuples of len <= n.
    :rtype: list
    """
    return [tuple(l[i:i + n]) for i in range(0, len(l), n)]

def loggingLevel():
    return pickle.load(open(Config.prefs, 'rb'))['debugLogging']
