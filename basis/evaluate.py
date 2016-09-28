"""Functions for evaluating basis functions for a given potential and
constructing the Hamiltonian matrix for the basis expansion
solution. By default, we use the Fourier :math:`\sin(n \pi x/L)`
basis functions as explained in [1]_.

.. [1] http://dx.doi.org/10.1119/1.4944706
"""
import numpy as np
def wave(V, Cn, prob=False):
    """Returns the wave function for the given vector of basis
    expansion coefficients.
    
    Args:
        V (basis.potential.Potential): object for evaluating the
          potential.
        Cn (numpy.ndarray): eigenvector of basis expansion coefficients to
          use when plotting the wave function.
        prob (bool): when True, plot the magnitude squared of the wave
          function.

    Returns:
        function: that can be evaluated for arbitrary values (including
          array-valued arguments).
    """
    if prob:
        return lambda x: sum([np.abs(c)**2*np.sin((n+1)*np.pi*x/V.L)
                              for (n, c) in enumerate(Cn)])
    else:
        return lambda x: sum([c*np.sin((n+1)*np.pi*x/V.L)
                              for (n, c) in enumerate(Cn)])
    
def _En0(n, L):
    """Returns the energy of the `n`-th infinite square well
    eigenstate, in units of :math:`\frac{\hbar^2}{2 \mu a^2}`.
    """
    return n**2*np.pi**2/L**2 #\hbar^2/2ma^2 with a the Bohr radius.

def H(V, N):
    """Returns the Hamiltonian matrix for the specified potential so
    that it can be solved via basis expansion. Assumed K-P form of the
    potential.

    Args:
        V (basis.potential.Potential): object for evaluating the
          potential.
        N (int): number of basis functions to use.

    Returns:
        numpy.ndarray: with shape (N, N); and elements as specified in
          equation (14).
    """
    #In equation (14), the :math:`E_n^{(0)}` refers the `n`-th energy
    #state of the infinite square well, which was the :math:`H_0` that
    #they introduced in equation (8).
    result = np.zeros((N, N))
    for n in range(1, N+1):
        for m in range(1, N+1):
            dE = 0. if n != m else _En0(n, V.L)
            result[n-1,m-1] = dE + sum([V(-V.a/2 + r*V.a) *
                                        _hnm(n, m, -V.a/2 + r*V.a, V.b, V.L)
                                        for r in range(1, V.nb+1)])
    return result    

def _hnm(n, m, s, b, L):
    """Evaluates a single element in the Hamiltonian basis
    matrix. Assumes that a Kronig-Penney type potential is being used
    with wells spaced by `a` that have barriers with width `b` between
    them.

    Args:
        n (int): index of the row in the :math:`H` matrix.
        m (int): column index in the :math:`H` matrix.
        s (float): position of the well given by :math:`-a/2 + ra` for the
          `r`-th barrier in the potential.
        b (float): width of the barrier between each well.
        L (float): width of the infinite square well that the K-P barriers
          are placed in.
    """
    return _Fnm(n, m, s+b/2, L) - _Fnm(n, m, s-b/2, L)

def _Fnm(n, m, x, L):
    """Returns the value derived in equation (16) and (17) of [1]_.

    Args:
        n (int): index of the row in the :math:`H` matrix.
        m (int): column index in the :math:`H` matrix.
        x (float): independent variable to evaluate functions at.
        L (float): width of the infinite square well that the K-P barriers
          are placed in.
    """
    if n == m:
        return x/L - np.sin(2*np.pi*n*x/L)/(2*np.pi*n)
    else:
        return (np.sin((m-n)*np.pi*x/L)/(np.pi*(m-n)) -
                np.sin((m+n)*np.pi*x/L)/(np.pi*(m+n)))
