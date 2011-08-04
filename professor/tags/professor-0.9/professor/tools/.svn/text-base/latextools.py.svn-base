import numpy
from professor.tools import stringtools as st


def getCorrelationTable(adict, params, statistics=False, sortparams=False):
    """ this returns latex code of a triangle-shaped tabular
        adict is considered to be a dictionary as returned by
        result.getCorrelations
        params has to be a list of the paramnames used
    """
    # try sorting parameternames
    if sortparams:
        params = st.sortParamNameList(params)
    table = [] # this will hold strings of lines of latex code
    head ='\\documentclass[landscape]{article}\n\\pagestyle{empty}\n\\usepackage[landscape]{geometry}\n\\usepackage{amsmath}\n\\begin{document}'
    table.append(head)
    # this is declaration of the tabular thing
    begin = '\\begin{tabular}{'
    for i in xrange(len(params) + 1):
        begin += 'c'
    begin += '}\\\\ \\hline'
    table.append(begin)
    # this is the first row of the tabular
    first = ' '
    for i in params:
        first += '& %s'%i
    first += '\\\\ \\hline'
    table.append(first)
    # here we make use of the symmetry of the correlation matrix (i,j) = (j,i) 
    # and exclude the (j,i) values except for j = i
    combinations = {}
    for num, i in enumerate(params):
        temp = [(i,j) for j in params[num:]]
        combinations[str(num)] = temp
    # now creating all the other lines
    for num, i in enumerate(params):
        line = i
        combs = combinations[str(num)]
        # some blank cells...
        for j in xrange(len(params) - len(combs)):
            line += ' &'
        # the non blank cells
        for c in combs:
            try:
                if statistics:
                    line += ' & %.2f +- %.2f'%(float(adict[c][0]), float(adict[c][1]))
                else:
                    line += ' & %.2f'%float(adict[c])
            except KeyError:
                line += ' & ------ '
        line += '\\\\'
        table.append(line)
    # this closes the tabular definition
    end = '\\end{tabular}\n\\end{document}'
    table.append(end)
    return table


