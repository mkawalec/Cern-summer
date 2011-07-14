#!/usr/bin/env python2

## Adding two dat files:

from glob import glob
files = glob("*.dat")

def finder(content):
    foundBegin = False
    foundTitle = False
    output = ['']*100
    counter = 0

    for line in content:
        if line.find("# BEGIN HISTOGRAM") != -1:
            foundBegin = True
        if foundBegin and foundTitle:
            output[counter] += line 
        if foundBegin and line.find("Title") != -1:
            foundTitle = True

        if line.find("# END HISTOGRAM") != -1:
            foundBegin = False
            foundTitle = False
            counter += 1
    
    return output 

def printOut(content, output):
    dat = ""
    foundTitle = False
    for line in content:
        if foundTitle and line.find("Title") != -1:
            dat += line
            break
        if line.find("Title") != -1:
            foundTitle = True
        dat += line
    
    for line in output:
        for number in line:
            dat += str(number) + "   "
        dat += "\n"
    dat += "# END HISTOGRAM"
    
    return dat

## Parsing
from optparse import OptionParser
usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage, version="1")
parser.add_option("-a", "--average", dest="AVERAGE", action="store_true",
    default=False, help="if specified the data will be averaged between the file that are added. Default is False, but in most cases (all when any kind of normalistaion is on) it needs to be set.")
(args, options) = parser.parse_args()
average = args.AVERAGE

## The 'almost main' loop
count = 0
for dat in files:
    histo = open(dat, "r")
    content = histo.readlines()
    histo.close()
    
    ## Protection against empty files
    if len(content) == 0:
        continue
        count +=1
    begin = finder(content)

    ## Now, numpy parsing:
    import numpy as np
    from StringIO import StringIO

    array = [] 
    for matrix in begin:
        if len(matrix) > 0:
            array.append(np.genfromtxt(StringIO(matrix)))

    # Adding
    output = np.copy(array[0])
    for  matrix in array[1:]:
        output[:,2:] += matrix[:,2:]

    if average:
        output /= len(array)
    
    ## Now the last bits of writing and moving stuff around:
    import os
    os.remove(dat)
    out = open(dat, "w")
    out.write(printOut(content,output))
    out.close()

print "Processed " + str(len(files) - count)+ " files"
