#! /usr/bin/env python2

""" 
This is supposed to be a small script for running and compiling 
an analysis for Rivet. It has and overgrowth of features, precisely
to boost my line count at github.
"""

import sys
if sys.version_info[:3] < (2, 0, 0):
	print "This script requires at least python 2. Go get a decent operating system"
	sys.exit(1)

## Parsing command line options:
from optparse import OptionParser
parser = OptionParser(usage=__doc__, version="1")
parser.add_option("-b", "--build", "--make", dest="build", action="store_true", 
	default=False, help="if specified, the analysis will be built first before launching rivet")
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
parser.add_option("-p", "--pythia", dest="version", type="int", default=423,
	help="specify the version of pythia. Defaults to 423, just to be sure.")
parser.add_option("-a", "--analysis", dest="analysis", default="MC_TTBAR",
	help="specify an analysis. Seems like an obligatory one.")
parser.add_option("-o", "--options", dest="options", default=" ",
	help="specify an options string for Pythia.")
parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
	default=False, help="make the program verbose")
(args,options) = parser.parse_args()

## Now, setting the parsed arguments:
build =  args.build 
energy = args.energy
lxplus = args.lxplus
number = args.number
histos = args.histos
plots = args.plots
version = args.version
analysis = args.analysis
options = args.options
verbose = args.verbose


from os import popen as getoutput 
## Just make sure that everything that should exists:
if lxplus:
	getoutput("rm /tmp/$USER/hepmc.fifo ; mkfifo /tmp/$USER/hepmc.fifo")
else:
	getoutput("rm /tmp/hepmc.fifo ; mkfifo /tmp/hepmc.fifo")

if build:
	output = getoutput("rivet-buildplugin RivetPlugin.so " + analysis + ".cc")
	if verbose: 
		print(output)

## Now, run agile
if lxplus:
	output = getoutput("agile-runmc Pythia6:" + str(version) + " " + options + " -n " + number + " --beams=LHC:" + str(energy) + " -o /tmp/$USER/hepmc.fifo")
	if verbose:
		print(output)
else:
	print("2 ")
	output = getoutput("agile-runmc Pythia6:" + str(version) + " " + options + " -n " + str(number) + " --beams=LHC:" + str(energy) + " -o /tmp/hepmc.fifo")
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


