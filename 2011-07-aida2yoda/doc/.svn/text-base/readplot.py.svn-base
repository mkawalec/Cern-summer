#! /usr/bin/env python

## TODO: Why don't these tests work within 'make'?


## Make "set" a builtin type on Python < 2.4
try:
    tmp = set()
    del tmp
except:
    from sets import Set as set

## Make "sorted" a builtin function on Python < 2.4
if 'sorted' not in dir(__builtins__):
    def sorted(iterable, cmp=None, key=None, reverse=None):
        rtn = iterable
        rtn.sort(cmp)#, key, reverse)
        return rtn


## Get input paths to allow rivet module to be imported from the src dir
import os, re, glob, sys
pybuild = os.path.abspath(os.path.join(os.getcwd(), "..", "pyext", "build"))
dirs = []
for d in os.listdir(pybuild):
    if re.match(r"lib\..*-.*-%d\.%d" % (sys.version_info[0], sys.version_info[1]), d):
        dirs.append(os.path.join(pybuild, d))
sys.path = dirs + sys.path
os.environ["LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"] + ":" + \
    os.path.abspath(os.path.join(os.getcwd(), "..", "src", ".libs"))
anadirs = glob.glob(os.path.join(os.getcwd(), "..", "src", "Analyses", "*", ".libs"))
#print anadirs
os.environ["RIVET_ANALYSIS_PATH"] = ":".join(anadirs)


## Change dlopen status to GLOBAL for Rivet lib
try:
    import ctypes
    sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)
except:
    import dl
    sys.setdlopenflags(sys.getdlopenflags() | dl.RTLD_GLOBAL)
import rivet


# all_analyses = rivet.AnalysisLoader.analysisNames()
# for a in
#plotinfos = glob.glob(os.path.join(os.getcwd(), "..", "data", "plotinfo", "*"))


## Get list of plots for each analysis
def plotinfo(aname):
    finfo = None
    rtn = {}
    try:
        import yaml, glob
        files = glob.glob(os.path.join(os.getcwd(), "..", "data", "plotinfo", aname+"*"))
        plotinfofile = files[0]
        finfo = open(plotinfofile, "r")
    except:
        return rtn
    import re
    pat_begin_block = re.compile('^# BEGIN ([A-Z0-9_]+) ?(\S+)?')
    pat_end_block =   re.compile('^#+ END ([A-Z0-9_]+)')
    pat_comment = re.compile('^#|^\s*$')
    pat_property = re.compile('^(\w+?)=(.*)$')
    pat_path_property  = re.compile('^(\S+?)::(\w+?)=(.*)$')

    current_histo = None
    for line in finfo:
        mbegin = pat_begin_block.match(line)
        if mbegin:
            current_histo = mbegin.group(2)
            rtn.setdefault(current_histo, dict())
            continue
        mend = pat_end_block.match(line)
        if mend:
            current_histo = None
            continue
        if pat_comment.match(line):
            continue
        mprop = pat_property.match(line)
        if mprop and mprop.group(1) == "Title":
            rtn[current_histo]["TITLE"] = mprop.group(2)
    finfo.close()
    return rtn


if __name__ == "__main__":
    for i in sys.argv[1:]:
        print plotinfo(i)
