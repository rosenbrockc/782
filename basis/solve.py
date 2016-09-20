#!/usr/bin/python
from basis import msg
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
    "N": dict(default=100, type=int,
              help=("Specifies how many basis functions to use in the expansion "
                    "solution.")),
    "-plot": dict(action="store_true",
                  help=("Plots the solution.")),
    "-potential": dict(help="Path to the file that has the potential "
                       "parameters."),
    "-outfile": dict(default="output.dat",
                     help="Override the default output file name.")
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

def run(args):
    print("RUNNING", args)

if __name__ == '__main__': # pragma: no cover
    run(_parser_options())
