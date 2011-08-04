"""lego.py

"""

import numpy, matplotlib.mlab

def makeVectorRedundant(xs, red):
    t = numpy.zeros(red * xs.shape[0])
    for i in xrange(red):
        t[i::red] = xs
    return t


def prepLegoData(xlims, ylims, zvals):
    """Prepare 3D histogram data to be used with matplotlib's Axes3D/Axes3DI.

    usage example:

    >>> nx, ny = 3, 5
    >>> X, Y, Z = prepLegoData(numpy.arange(nx), numpy.arange(ny),
    ... numpy.random.rand(nx, ny))
    >>> fig = pylab.figure()
    >>> ax = matplotlib.axes3d.Axes3DI(fig)
    >>> ax.plot_surface(X, Y, Z, rstride=2, cstride=2)
    >>> pylab.show()

    @param xlims: N+1 array with the bin limits in x direction
    @param ylims: M+1 array with the bin limits in y direction
    @param zvals: a 2D array with shape (N, M) with the bin entries,
        example::
        --> y-index (axis 1)
        |       z_0_0  z_0_1  ...
        |       z_1_0  z_1_1  ...
        V        ...
        x-index (axis 0)
    @returns: X, Y, Z 2D-arrays for Axes3D plotting methods
    """
    assert xlims.shape[0] - 1 == zvals.shape[0]
    assert ylims.shape[0] - 1 == zvals.shape[1]

    ## Use a higher redundancy for surface_plot - must be a multiple of 2!
    red = 4

    X, Y = matplotlib.mlab.meshgrid(makeVectorRedundant(xlims, red),
                                    makeVectorRedundant(ylims, red))
    Z = numpy.zeros(X.shape)

    ## Enumerate the columns of the zvals
    for yi, zvec in enumerate(zvals):
        t = makeVectorRedundant(zvec, red)
        for off in xrange(1, red+1):
            Z[red/2:-red/2, red*yi + off] = t
    return X, Y, Z


def test_lego():
    import pylab
    from matplotlib import axes3d

    #X, Y, Z = prepLegoData(numpy.arange(3), numpy.arange(3),
            #numpy.array([[1, 3], [2, 4]]))
    #fig = pylab.figure()
    #ax1 = axes3d.Axes3DI(fig)
    #ax1.plot_wireframe(X, Y, Z)

    # X, Y, Z = prepLegoData(numpy.arange(4), numpy.arange(5),
            # numpy.array([[1.0, 1.5, 1.3],
                        # [1.7, 2.1, 0.8],
                        # [2.1, 2.0, 0.7],
                        # [2.5, 1.9, 0.5]])
            # )

    # ax2 = axes3d.Axes3D(pylab.figure())
    #ax2.plot_wireframe(X, Y, Z, colors=((0,0,0),))
    # ax2.plot_surface(X, Y, Z, rstride=2, cstride=2,
            # edgecolors='w')
    # ax2.set_xlabel('X')
    # ax2.set_ylabel('Y')
    # ax2.set_zlabel('#')

    nx, ny = 10, 8
    z = numpy.random.rand(nx, ny)
    X, Y, Z = prepLegoData(numpy.arange(nx + 1), numpy.arange(ny + 1),
            z)
    ax3 = axes3d.Axes3D(pylab.figure())
    ax3.plot_surface(X, Y, Z, rstride=2, cstride=2,
            edgecolors='w')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('#')


    pylab.show()

# test_lego()
