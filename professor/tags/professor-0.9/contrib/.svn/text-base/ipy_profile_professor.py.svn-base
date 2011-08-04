import IPython.ipapi

from IPython.Extensions import ipy_profile_scipy

ip = IPython.ipapi.get()
try:
    ip.ex("import professor")
    ip.ex("from professor.rivetreader import getTuningData, getSingleAnalysisInfo, readObservableFile, getConfiguredData")
    ip.ex("from professor.tuningdata import TuningData, GoFData, SingleTuneData, BinProps")
    ip.ex("from professor.histo import Histo, Bin")
    ip.ex("from professor.interpolation import InterpolationSet, getInterpolationClass")
    ip.ex("from professor.minimize import getMinimizerClass, ResultList")
    ip.ex("from professor.minimize.pyminuitminimizer import PyMinuitMinimizer")
    ip.ex("from professor.tools.parameter import Scaler, ParameterPoint, readParameterFile")
except ImportError, err:
    print "Unable to start professor profile, is professor installed?"

