#!/usr/bin/python
"""resolution.py

"""
import os, sys, numpy

def getScreenResolution():
    """ return tuple of screens resolution by redirection of command xrandr to
        a temporary file and parsing the latter for keywords
    """
    os.system("xrandr|grep 'Screen 0' >> temp_resolution_file")
    f = open('temp_resolution_file', 'r')
    temp = f.next().split(',')
    for token in temp:
        if token.strip().startswith('current'):
            res = [int(item) for item in token.split() if item != 'current' and item != 'x']
    f.close()
    os.system('rm -f temp_resolution_file')
    return res

def getScreenSize(inch=True):
    """ return Screensize in inch or mm """
    os.system('xdpyinfo|grep dimensions >> temp_size_file')
    f = open('temp_size_file', 'r')
    temp = f.next()
    f.close()
    os.system('rm -f temp_resolution_file')
    mm = map(int,temp.split('(')[1].split()[0].split('x'))
    if inch:
        return tuple(.9*numpy.array(mm)/25.4)
    else:
        return tuple(mm)

