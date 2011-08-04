"""__init__.py

"""

__all__ = ['dists', 'generator', 'chi2_vs_dp']

from professor.tools.config import Config

Config().initModule('test',
        {'logfiles':'-',
         'loglevel':'debug'
        })


def buildSimplePG(dim):
    """Create a simple PointGenerator instance with dummy scaler."""
    import generator
    from professor.tools.parameter import Scaler
    sc = Scaler(['param%i'%(i) for i in xrange(dim)])
    return generator.PointGenerator(sc)
