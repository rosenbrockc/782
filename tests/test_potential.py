"""Tests the evaluation of the potential for single and array-valued
arguments for SHO, bump and KP potentials.
"""
import pytest
from basis.potential import Potential
import numpy as np

def test_getattr():
    """Tests the attribute re-routing to Potential.params.
    """
    pot = Potential("potentials/kp.cfg")
    assert pot.w == pot.params["w"]

    pot = Potential("potentials/bump.cfg")
    assert pot.a == pot.params["a"]

    pot = Potential("potentials/sho.cfg")
    assert pot.shift == pot.params["shift"]

    with pytest.raises(AttributeError):
        pot.dummy

def test_kp():
    """Tests the Kronig-Penney potential.
    """
    pot = Potential("potentials/kp.cfg")
    # Params for kp are w, s, n and v0. We use R as the new resolution
    # for the numpy array check. My kp file only does even numbers of
    # wells.
    params = [(2, 0.5, 16, -15., 100),
              (1e5, 1e3, 100, -1234., 1e5),
              (1./3, 1./6, 10, 5, 20),
              (np.pi, np.pi/4., 6, np.sqrt(2), 23)]

    for w, s, n, v0, R in params:
        pot.adjust(w=w, s=s, n=n, v0=v0)
        xa = np.linspace(0, w*n, R)
        assert pot(0) == v0
        assert pot(w*n) == 0.
        assert pot((w-s)/2.) == v0
        assert len(pot(xa)) == R
        assert pot(w-s/2.) == 0.
        assert pot(-5.*w*n) == 0.

def test_sho():
    """Tests the SHO potential.
    """
    pot = Potential("potentials/sho.cfg")
    params = [(2, 0., 15., 100),
              (1e5, 1e3, 1234., 1e5),
              (1./3, 1./6, 10, 5),
              (np.pi, np.pi/2., np.sqrt(2), 23)]

    for a, shift, v0, N in params:
        pot.adjust(a=a, shift=shift, v0=v0)
        xa = np.linspace(-a, a, N)
        assert pot(-a) == v0*(-a-shift)**2
        assert pot(a) == 0.
        assert pot(3./4*a) == v0*(3./4*a-shift)**2
        assert len(pot(xa)) == N
        assert pot(-5.*a) == 0. #Outside of region
        with pytest.raises(ValueError):
            pot("some sho")
    
def test_bump():
    """Tests the bump in the square well potential.
    """
    pot = Potential("potentials/bump.cfg")
    params = [(2, 1, -15., 100),
              (1e5, 1e3, -1234., 1e5),
              (1./3, 1./6, -10, 5),
              (np.pi, np.pi/2., -np.sqrt(2), 23)]

    for a, w, V0, N in params:
        pot.adjust(a=a, w=w, v0=V0)
        x = w+(a-w)/2.
        xa = np.linspace(-a, a, N)
        assert pot(x) == 0.
        assert pot(3./4*w) == V0
        assert len(pot(xa)) == N
        assert pot(-5.*a) == 0.
        assert pot(-w) == V0
        assert pot(a) == 0.
        with pytest.raises(ValueError):
            pot("a")

def test_adjust():
    """Tests adjusting a potential using an expression instead of a
    constant. Also tests the warning when attempting to adjust a
    non-existent parameter.
    """
    pot = Potential("potentials/bump.cfg")
    pot.adjust(a="w*numpy.sqrt(v0)")
    pot.adjust(dummy=0.1)
            
def test_incorrect():
    """Tests execution of warning messages for incorrectly configured
    potential files.
    """
    with pytest.raises(ValueError):
        V = Potential("potentials/wrong.cfg")
