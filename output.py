#!/usr/bin/env python3

import subprocess as sp

def output_xfa(xfafile, output, eqnfile=None):
    args = ["xf_Post", "-xfa", xfafile, "-output", output]
    if eqnfile is not None:
        args += ["-eqn", eqnfile]
    out = sp.check_output(args)
    return float(out.splitlines()[-2])

def output_xfa_list(l, output, eqnfile=None):
    return [output_xfa(f, output, eqnfile=eqnfile) for f in l]
