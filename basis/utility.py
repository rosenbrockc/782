"""Utility functions for I/O, system calls and visualization.
"""
def colorspace(size):
    """Returns an cycler over a linear color space with 'size' entries.
    
    :arg int size: the number of colors to define in the space.
    :returns: iterable cycler with 'size' colors.
    :rtype: itertools.cycle
    """
    from matplotlib import cm
    from itertools import cycle
    import numpy as np
    rbcolors = cm.rainbow(np.linspace(0, 1, size))
    return cycle(rbcolors)

def _get_reporoot():
    """Returns the absolute path to the repo root directory on the current
    system.
    """
    from os import path
    import basis
    codepath = path.abspath(basis.__file__)
    return path.dirname(path.dirname(codepath))

reporoot = _get_reporoot()
"""The absolute path to the repo root on the local machine.
"""
