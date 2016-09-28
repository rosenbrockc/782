"""Tests the script access to the basis solver.
"""
import pytest
from basis.solve import run
def get_sargs(args):
    """Returns the list of arguments parsed from sys.argv.
    """
    import sys
    sys.argv = args
    from basis.solve import _parser_options
    return _parser_options()    

def test_examples():
    """Makes sure the script examples work properly.
    """
    argv = ["py.test", "-examples"]
    assert get_sargs(argv) is None

def test_potplot(kp):
    """Tests plotting of the potential.
    """
    argv = ["py.test", "-potential", "potentials/paper.cfg", "-potplot"]
    args = get_sargs(argv)
    run(args)

    #Also test the interactive plotting with custom parameters.
    kp.plot(0., kp.L, 1000, ylim=(0,103))

def test_bands(kp, tmpdir):
    """Tests calculation and plotting of the bands.
    """
    plotfile = str(tmpdir.join("bands.pdf"))
    argv = ["py.test", "-potential", "potentials/paper.cfg", "-bands",
            "-action", "save", "-plotfile", plotfile]
    args = get_sargs(argv)
    run(args)

    from os import path
    assert path.isfile(plotfile)
    
def test_run(tmpdir):
    """Tests that a default solve works properly. This tests the
    default plotting functionality of the wave functions as well.
    """
    outfile = str(tmpdir.join("output-{}.dat"))
    plotfile = str(tmpdir.join("plots.pdf"))
    argv = ["py.test", "-potential", "potentials/paper.cfg", "-action",
            "save", "-outfile", outfile, "-plotfile", plotfile]
    args = get_sargs(argv)
    run(args)

    from os import path
    assert path.isfile(str(tmpdir.join("output-E.dat")))
    assert path.isfile(str(tmpdir.join("output-C.dat")))
    assert path.isfile(plotfile)

def test_probplot():
    """Tests plotting of the probability distribution function instead
    of the wave function.
    """
    argv = ["py.test", "-potential", "potentials/paper.cfg", "-prob"]
    args = get_sargs(argv)
    run(args) == 0

def test_envplot():
    """Tests plotting of the probability distribution function instead
    of the wave function.
    """
    argv = ["py.test", "-potential", "potentials/paper.cfg", "-envelope"]
    args = get_sargs(argv)
    run(args) == 0    

def test_nbconv(tmpdir):
    """Tests the band energy filling as a function of the number of
    barriers.
    """
    plotfile = str(tmpdir.join("plots.pdf"))
    argv = ["py.test", "-potential", "potentials/paper.cfg",
            "-nbconv", "-action", "save", "-plotfile", plotfile]
    args = get_sargs(argv)
    run(args) == 0

    from os import path
    assert path.isfile(plotfile)   
