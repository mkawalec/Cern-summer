from numpy import array, dot

def getDirection(p0, p1):
    return array(p1) - array(p0)

def getLambda(P, p0, p1):
    r = getDirection(p0, p1)
    return float(dot(P - p0, r))/float(dot(r, r))

def getIntersection(p0, p1, P):
    r = getDirection(p0, p1)
    return array(p0) + getLambda(P, p0, p1)*r
