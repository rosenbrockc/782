"""Tests the construction of the Hamiltonian from an arbitrary
potential.
"""
import pytest
from conftest import assert_float_equal
from numpy import loadtxt
from glob import glob
    
def test_Fnm(kp):
    """Tests the function that returns a partial matrix element for
    :math:`n=n` and :math:`n=m` cases.
    """
    from basis.evaluate import _Fnm    
    cases = glob("tests/model/Fnm.*.dat")
    for case in cases:
        model = loadtxt(case)
        for i in range(len(model)):
            n, m = tuple(map(int, model[i,0:2]))
            x, r = model[i,2:]
            print(n, m, x)
            assert_float_equal(_Fnm(n, m, x, kp.L), r)

def test_hnm(kp):
    """Tests the construction of the Hamiltonian matrix.
    """
    from basis.evaluate import _hnm
    cases = glob("tests/model/hnm.*.dat")
    for case in cases:
        model = loadtxt(case)
        for i in range(len(model)):
            n, m, r = tuple(map(int, model[i,0:3]))
            x, ans = model[i,3:]
            s = -kp.a/2.+r*kp.a
            assert_float_equal(_hnm(n, m, s, kp.b, kp.L), ans)

def test_En0(kp):
    """Tests infinite square well energies."""
    from basis.evaluate import _En0
    model = loadtxt("tests/model/En0.dat")
    for n in range(len(model)):
        assert_float_equal(_En0(n+1, kp.L), model[n])

def test_H(kp):
    from basis.evaluate import H
    model = loadtxt("tests/model/H.dat")
    from numpy import allclose
    print(len(model), model[:,1])
    Hans=H(kp, 100)
    print(len(Hans), Hans[1,:])
    assert allclose(Hans, model)
    
