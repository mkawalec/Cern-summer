from decorators import deprecated

@deprecated("Is anybody using this function?")
def createArguments(params):
    """ return a list of function arguments (p0, p1, p2 etc.) suitable for
        def() and a dictionary to sort of re-translate them afterwards
        @param params: a list of strings
    """
    return ['p' + str(i) for i, par in enumerate(params)], dict([(
        'p' + str(i), par) for i, par in enumerate(params)])


@deprecated("Is anybody using this function?")
def getAChi2Hack(params):
    """ This will generate a then hardcoded definition of the chi2 as a string
        that is intended to be read using the exec command.
    """
    newargs = createArguments(params)[0]

    function = 'def chi2(' + newargs[0]
    array = '    p = ['+ newargs[0]
    for newarg in newargs[1:]:
        function += ', ' + newarg
        array += ', ' + newarg
    function += '):\n'
    array += ']\n'

    function+= array

    s_chi2 = '    r = .0\n    for refbin, interp, binprob in data:\n'
    s_chi2 += '        r += ((refbin.getYVal() - interp.getValueFromScaled(p))**2\n'
    s_chi2 += '             /refbin.getYErr()**2)\n'
    s_chi2 += '    return r'
    function += s_chi2

    return function

@deprecated("Is anybody using this function?")
def retranslateResult(params, result_dict):
    """ returns a dictionary of parameter:value pairs with the original
        parameter-names and a list of the values ordered in the same way
        the parameters were ordered before. This has to be done, since
        pyMinuit returns results as dictionaries, thus losing the initial
        order of our parameters. And of course we want to get rid of the
        artificial parmeter-names introduced with createArguments
    """
    d = {}
    for newarg, param in createArguments(params)[1].iteritems():
        d[param] = result_dict.get(newarg)
    l = [d.get(param) for param in params]
    return d, l
