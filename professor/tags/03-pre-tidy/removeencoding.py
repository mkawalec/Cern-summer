"""removeencoding.py

usage:
    find -name '*.py' -exec removeencoding.py \{\} \;
"""

import sys, re, os
encoding_re = re.compile(r'# vim:fileencoding.*')
interp_re = re.compile(r'#!/usr/bin/python.*')


def filter_enc(line):
    return encoding_re.search(line) is None

def filter_interp(line):
    return interp_re.search(line) is None

path = sys.argv[1]

f = open(path, 'r')
temp = filter(filter_enc, f)

del f

if os.access(path, os.X_OK):
    lines = filter(filter_interp, temp)
else:
    lines = temp

f = open(path, 'w')
[f.write(l) for l in lines]

print path
