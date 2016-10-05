#!/usr/bin/python
from basis import msg
from basis.base import testmode
def examples():
    """Prints examples of using the script to the console using colored output.
    """
    script = "BASIS: 1D Quantum Potential Solver via Basis Expansion"
    explain = ("For simple 1D potentials such as Kronig-Penny, infinite "
               "square well, finite square well, harmonic oscillator, "
               "etc. this code produces a numerical solution via basis "
               "expansion.")
    contents = [(("Solve the potential in `kp.cfg` using 200 basis functions."), 
                 "solve.py 200 -potential kp.cfg",
                 "This saves the solution to the default 'output.dat' "
                 "file in the current directory."),
                (("Solve the potential in `kp.cfg` and plot the solution."), 
                 "solve.py 200 -potential kp.cfg -plot",
                 ""),
                (("Solve the potential `sho.cfg`, save the solution to "
                  "`mysol.out`."),
                 "solve.py 400 -potential sho.cfg -outfile mysol.out","")]
    required = ("REQUIRED: potential config file `pot.cfg`.")
    output = ("RETURNS: plot window if `-plot` is specified; solution "
              "output is written to file.")
    details = ("The plotting uses `matplotlib` with the default configured "
               "backend. If you want a different backend, set the rc config "
               "for `matplotlib` using online documentation.")
    outputfmt = ("")

    msg.example(script, explain, contents, required, output, outputfmt, details)

script_options = {
    "-N": dict(default=100, type=int,
              help=("Specifies how many basis functions to use in the expansion "
                    "solution.")),
    "-plot": dict(nargs="*", type=int, default=[0],
                  help=("Plots the wave functions; basis functions with "
                        "indices in this list will be plotted, or all will "
                        "be plotted if none are specified.")),
    "-potential": dict(help="Path to the file that has the potential "
                       "parameters."),
    "-outfile": dict(default="output-{}.dat",
                     help=("Override the default output file name.")),
    "-envelope": dict(action="store_true",
                      help=("When specified, the envelope function for a given "
                            "wave function will be included in plots.")),
    "-plotfile": dict(default="plot.pdf",
                      help="Override the default file name for saving plots."),
    "-bands": dict(action="store_true",
                   help="Plot/save the bands as a function of wave number `k`."),
    "-prob": dict(action="store_true",
                  help="Plot the probability distribution function, instead "
                  "of the wave function (which may be complex)."),
    "-potplot": dict(action="store_true",
                     help="Plot the potential."),
    "-nbconv": dict(action="store_true",
                     help="Plot covergence of bands vs. number of barriers.")
    }
"""dict: default command-line arguments and their
    :meth:`argparse.ArgumentParser.add_argument` keyword arguments.
"""
    
def _parser_options():
    """Parses the options and arguments from the command line."""
    #We have two options: get some of the details from the config file,
    import argparse
    from basis import base
    pdescr = "1D Quantum Potential Solver."
    parser = argparse.ArgumentParser(parents=[base.bparser], description=pdescr)
    for arg, options in script_options.items():
        parser.add_argument(arg, **options)
        
    args = base.exhandler(examples, parser)
    if args is None:
        return

    return args

def _eigsolve(args, **adjustment):
    """Constructs the :math:`H` matrix for the potential specified in
    the command-line arguments and then solves the eigensystem to
    produce the wavefunctions and energy levels.

    Returns:
        (tuple): of eigenvalues and eigenvectors
          (:class:`numpy.ndarray`).
    """
    from basis.evaluate import H
    from basis.potential import Potential
    V = Potential(args["potential"])
    if len(adjustment) > 0:
        V.adjust(**adjustment)
        
    _H = H(V, args["N"])

    from numpy.linalg import eig
    return (V, ) + eig(_H)

def _plotwaves(V, EC, args):
    """Plots the wave functions for the solutions with the specified indices.
    
    Args:
        EC (list): of tuples (En, Cn) where `En` is the eigenvalue and `Cn` is
        the corresponding eigenvector (:class:`numpy.ndarray`).
        args (dict): parsed command-line arguments.
        indices (list): 
    """
    import matplotlib.pyplot as plt
    import numpy as np
    #We use the parameters from the potential to decide what the x-values will
    #look like. Then we evaluate the basis functions for the y-values.
    from basis.evaluate import wave
    from basis.utility import colorspace
    
    x = np.linspace(0, V.L, V.nb*25)
    cycols = colorspace(len(args["plot"]))
    for n in args["plot"]:
        wavefun = wave(V, EC[n][1], args["prob"])
        col = next(cycols)
        plt.plot(x, wavefun(x), color=col)
        if args["envelope"]:
            env = np.sin((n+1)*np.pi*x/V.L)
            if args["prob"]:
                env = abs(env)
            plt.plot(x, env, color=col, linestyle="dashed")

    if "save" in args["action"]:
        plt.savefig(args["plotfile"])
    elif not testmode: # pragma: no cover
        plt.show()

def _plot_nbconv(args):
    """Plots the energies as we increase the number of barriers in the
    model. Reproduces figure 4 in the paper.
    """
    import matplotlib.pyplot as plt    
    for nb in range(1, 11):
        V, E, C = _eigsolve(args, nb=nb)
        xs = [nb for i in range(3*nb)]
        Es = sorted(E)
        if len(xs) > len(Es): # pragma: no cover
            #This is just a sanity check for the plotting library. It doesn't
            #ever fire.
            xs = xs[0:len(Es)]
        plt.scatter(xs, Es[0:len(xs)], marker='s')

    plt.xlabel("Number of barriers (cells)")
    plt.ylabel("Energy")
    plt.xlim((0,11))
    plt.ylim((0,100))
        
    if "save" in args["action"]:
        plt.savefig(args["plotfile"])
    elif not testmode: # pragma: no cover
        plt.show()
        
def _plot_bands(V, EC, args):
    """Plots the first few bands for the potential as a function of :math:`k`.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from operator import itemgetter
    NB=30
    k = np.linspace(0, NB//V.nb, NB)
    E = np.array(list(map(itemgetter(0), EC)))
    plt.figure()
    plt.scatter(k[0:NB-1], E[0:NB-1]/np.pi**2, c='k', marker='o', label="Matrix method")
    for i in range(1, 4):
        analytic = np.loadtxt("analytic/KP.bands.{}".format(i))
        plt.plot(analytic[:,0], analytic[:,1],
                 c='r', label="Analytic Solution" if i== 0 else None)
    plt.plot(k, k**2, 'b--', label="Infinite square well")
    plt.xlabel("$k/\pi$")
    plt.ylabel("$E_n/\pi^2$")
    plt.title("Kronig-Penney Band Plot")
    plt.legend(loc=2)
    plt.xlim((-0.1, NB//V.nb))
    plt.ylim((0., NB/2))

    if "save" in args["action"]:
        plt.savefig(args["plotfile"])
    elif not testmode: # pragma: no cover
        plt.show()
        
def run(args):
    """Runs the basis expansion solver for the specified potential.
    """
    V, E, C = _eigsolve(args)
    #We need to sort the eigenvalues and vectors to get the lowest energy ones
    #first.
    from operator import itemgetter
    EC = list(sorted(zip(E, C.T), key=itemgetter(0)))
    if ("save" in args["action"] and not
        (args["potplot"] or args["bands"] or args["nbconv"])):
        #Write the eigenvalues and vectors to file; for this project,
        #`numpy.savetxt` is probably the most useful for
        #cross-compatibility with Mathematica, etc.
        from numpy import savetxt
        savetxt(args["outfile"].format("E"), E)
        savetxt(args["outfile"].format("C"), C)

    if args["potplot"]:
        V.plot(0, V.L, 1000)
    elif (args["plot"] and not
          (args["bands"] or args["nbconv"])):
        _plotwaves(V, EC, args)
    elif args["bands"]:
        _plot_bands(V, EC, args)
    elif args["nbconv"]:
        _plot_nbconv(args)
        
if __name__ == '__main__': # pragma: no cover
    run(_parser_options())
