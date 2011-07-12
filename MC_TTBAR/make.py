#! /usr/bin/env python2

""" 
This is supposed to be a small script for running and compiling 
an analysis for Rivet. It has and overgrowth of features, precisely
to boost my line count at github.
"""

import sys
if sys.version_info[:3] < (2, 4, 0):
	print "This script requires at least python 2. Go get it now!!11!!"
	sys.exit(1)

## md5 helper function. It excludes all the lines that start with excludeLine and also the empty ones
def md5(fileName, excludeLine="#"):
	"""Compute md5 hash of the specified file"""
    	m = hashlib.md5()
    	try:
        	fd = open(fileName,"rb")
    	except IOError:
        	print "Unable to open the file in readmode:", filename
        	return
    	content = fd.readlines()
    	fd.close()
    	for eachLine in content:
        	if excludeLine and eachLine.startswith(excludeLine) or len(eachLine) == 0:
            		continue
        	m.update(eachLine)
    	return m.hexdigest()

def ask(files):
	if len(files) == 1:
		return files[0][:-3]
	else:
		print("Which analysis do you want to run?")
		for n, cc in enumerate(files):	
			print str(n) + ") " + cc
		i = int(input("Please specify a number: "))
		return files[i][:-3]

## Parsing command line options:
from optparse import OptionParser
parser = OptionParser(usage=__doc__, version="1")
parser.add_option("-b", "--build", "--make", dest="build", action="store_true", 
	default=None, help="if specified, the analysis will be built first before launching rivet")
parser.add_option("-e", "--energy", dest="energy", type="int", default=7000,
	help="specify the energy at which the simulator should run. The default is 7TeV. You will be greeted with an error if you try to set an unresonably high value.")
parser.add_option("-l", "--lxplus" "--on-cern", dest="lxplus", action="store_true",
	default=False, help="specifies if the script is run on lxplus. If this is the case, certain paths are changed in order for everything to work out of the box.")
parser.add_option("-n", "--number", dest="number", type="int", default=1000,
	help="specify the number of events to generate using agile. Defaults to a 1000.")
parser.add_option("-c", "--compare-histos", dest="histos", action="store_false",
	default=True, help="toggles if compare-histos should be run. Defaults to true.")
parser.add_option("--plots", "--make-plots", dest="plots", action="store_true", 
	default=False, help="specifies if the the plots should be made. Defaults to false.")
parser.add_option("--pythia-version", "--pythia", dest="version", type="int", default=423,
	help="specify the version of pythia. Defaults to 423, just to be sure.")
parser.add_option("-a", "--analysis", dest="analysis", default="",
	help="specify an analysis. Seems like an obligatory one.")
parser.add_option("-p", "--options", dest="options", default="",
	help="specify an options string for Pythia.")
parser.add_option("-P", dest="options2", default="", help="additional options for Pythia")
parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
	default=False, help="make the program verbose")
(args,options) = parser.parse_args()

## Now we check if the file should be built automatically
from glob import glob
import hashlib
files = glob("*.cc")

build = args.build 
of = ""
for cc in files:
	## Those line constitute a hack that creates .makerc if it doesn't exist yet
	data = open(".makerc", "w")
	data.close()

	data = open(".makerc", "rw")
	found = False
	while data:
		line = data.readline()
		if line.find(cc) >=0 and len(line.split()[0]) == len(cc):
			print("Found")
			found = True

			checksum = (line[line.find(cc)+len(line.split()[0]):]).strip()
			if checksum != md5(cc):
				build = True
				line = line.replace(checksum, md5(cc))
			of += line
		if len(line.split()) == 0:
			break
	if not found:
		of += cc + " " + md5(cc) + "\n"
		build = True

## Some moving around of the files to be sure we have what we need in the file
import shutil, os
output = open(".makerc.swp", "w")
output.write(of)
output.close()

os.remove(".makerc")
shutil.move(".makerc.swp", ".makerc")

## Now, setting the parsed arguments:
energy = args.energy
lxplus = args.lxplus
number = args.number
histos = args.histos
plots = args.plots
version = args.version
analysis = args.analysis
## Setting up the analysis: if there is an analysis file in the directory then set it as analysis file. Otherwise use the specified one
if analysis == "":
	analysis = ask(files)

options = args.options
option2 = args.option2
verbose = args.verbose

#Now, let's add the stuff to look for analysis

from os import popen as getoutput
from os import system
## Just make sure that everything that should exists:
if lxplus:
	getoutput("rm /tmp/$USER/hepmc.fifo ; mkfifo /tmp/$USER/hepmc.fifo")
else:
	getoutput("rm /tmp/hepmc.fifo ; mkfifo /tmp/hepmc.fifo")

if build:
	output = system("rivet-buildplugin RivetPlugin.so " + analysis + ".cc")
	if verbose: 
		print(output)

##Create an options string:
optionsString = ""
if(options!="") optionsString+= "-p " + options
if(options!="") optionsString+= "-P " + options2

## Now, run agile
if lxplus:
	output = getoutput("agile-runmc Pythia6:" + str(version) + " " + optionsString + " -n " + number + " --beams=LHC:" + str(energy) + " -o /tmp/$USER/hepmc.fifo")
	if verbose:
		print(output)
else:
	output = getoutput("agile-runmc Pythia6:" + str(version) + " " + optionsString + " -n " + str(number) + " --beams=LHC:" + str(energy) + " -o /tmp/hepmc.fifo")
	if verbose:
		print(output)

## And run rivet:
if lxplus:
	output = getoutput("RIVET_ANALYSIS_PATH=$PWD rivet -a " + analysis + " /tmp/$USER/hepmc.fifo")
	if verbose:
		print(output)
else:
	output = getoutput("RIVET_ANALYSIS_PATH=$PWD rivet -a " + analysis + " /tmp/hepmc.fifo")

if histos:
	output = getoutput("compare-histos Rivet.aida")
	if verbose:
		print(output)
if plots:
	output = getoutput("make-plots --pdfpng *.dat")
	if verbose:
		print(output)

