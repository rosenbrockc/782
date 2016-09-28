import pytest

@pytest.fixture(scope="session", autouse=True)
def kp(request):
    """Returns a potential object for the Kronig-Penney model.

    Returns:
        (basis.potential.Potential: representing the sub-directory for
        the packages JSON files.
    """
    from basis.base import set_testmode
    set_testmode(True)

    #Switch to a non-interactive backend so we can run these on travis.
    import matplotlib
    matplotlib.use("Agg")

    from basis.potential import Potential
    return Potential("potentials/paper.cfg")

def assert_float_equal(a, b, tol=1e-10):
    """Asserts equality for floating point numbers. We could have used
    :module:`nose.tools` to do this, but we only need one thing, so it
    is easier to just code it here.
    """
    assert abs(a-b) < tol
