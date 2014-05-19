#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from .output import output_xfa
from .mesh import nelem_xfa, n0_xfa
from .adaptation import adaptation_errest, adaptation_time, sequence_time

def _create_time_array(timing_list):
    total_time = []
    time = 0
    for t in timing_list:
        for k in t:
            time += t[k]
        total_time.append(time)
    return np.array(total_time)

class output_convergence_plot:

    _xaxis_types = ['nelem', 'n0', 'h', 'time']

    def __init__(self, xaxis='nelem', output_name=None, exact=0., dim=None, options={}):
        if xaxis not in self._xaxis_types:
            raise ValueError("invalid xaxis type")
        if (xaxis == 'h') and (dim is None):
            raise TypeError("must specify dimension for h xaxis type")
        self.xaxis = xaxis
        self.output_name = output_name
        self.exact = exact
        self.dim = dim
        self.options = options

        self.figure = plt.figure()
        self.axis = self.figure.gca()

        self.axis.set_xscale('log')

    def add_sequence(self, xfa_list, label, options={}, logfile=None, output_name=None, exact=None, correct_output=False, plot_abs=True, run_type=None, nproc=1, ymult=1.):

        if output_name is None:
            output_name = self.output_name

        if exact is None:
            exact = self.exact

        options.update(self.options)

        y = np.array([(output_xfa(xfa, output_name) - exact) for xfa in xfa_list])

        if correct_output:
            if logfile is None:
                raise TypeError("must specify logfile for correcting output")

            errest = np.array(adaptation_errest(logfile))
            y -= errest[:len(y)]

        if plot_abs:
            y = np.abs(y)

        y *= ymult

        if self.xaxis == 'nelem':
            x = [nelem_xfa(xfa) for xfa in xfa_list]
        elif self.xaxis == 'n0':
            x = [n0_xfa(xfa) for xfa in xfa_list]
        elif self.xaxis == 'h':
            x = [1./(nelem_xfa(xfa))**(1./self.dim) for xfa in xfa_list]
        elif self.xaxis == 'time':
            if logfile is None:
                raise TypeError("must specify logfile for time output")
            if run_type == 'sequence':
                x = nproc*np.cumsum(sequence_time(logfile))[:len(y)]
            elif run_type == 'adaptation':
                x = _create_time_array(adaptation_time(logfile))[:len(y)]
            else:
                raise TypeError("run_type must be one of ['sequence', 'adaptation']")
        else:
            raise ValueError("invalid xaxis type")

        self.axis.plot(x, y, label=label, **options)
