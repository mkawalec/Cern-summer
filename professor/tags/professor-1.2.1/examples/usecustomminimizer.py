
## Load the professor framework.
import professor.user as prof

## 0. Make some selections.
## 0.1 Use quadratic interpolations (the weave flag is not important here.)
IpolCls = prof.getInterpolationClass("quadratic", True)

## 1. Create input data structures.

## 1.1 Interface to the files from disk.

## These PATHs must be changed appropriately.
## Note: For minimization we do not need MC data *if* we specify the runs.
dataproxy = prof.DataProxy()
dataproxy.refpath = "/PATH/to/refdata"
dataproxy.ipolpath = "/PATH/to/ipol"    # Note: The interpolations must have
                                        # been pre-generated.
## 1.2 Load the observables to tune to from a file.
weights = prof.WeightManager.mkFromFile("/PATH/to/weights/file")
observables = weights.posWeightObservables

## 1.3 Prepare data for *one* minimization with reference and
runs = [...]    # Can be None instead if the MC data path of dataproxy was set by 
                # >>> dataproxy.setMCPath("/PATH/to/mc/")
tunedata = dataproxy.getTuneData(withref=True, useipol=IpolCls,
                                 useruns=runs, useobs=observables)

## 2. Create minimization objects and minimize.
## 2.1 Create a GoF calculator that uses the chi^2 between interpolation and
## ref. data.
gof = prof.SimpleIpolChi2(tunedata)


## 2.2 Create a helper function and feed it to a minimizer.
def minimize_me(pvec):
    """
    `pvec` is a list/numpy array with the parameter values.
    """
    gof.setParams(pvec)
    return gof.calcGoF()

the_custom_minimizer(minimize_me)

print "order of parameters:"
print gof.tunedata.paramranges.names

## Now the tuned parameters can be put into a ParameterTune or
## MinimizationResult and dressed with more data. 

