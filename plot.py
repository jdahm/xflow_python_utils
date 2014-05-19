#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import log10

def plot_accuracy_order_triangle(a, xstart, ystart, rate, length=0.5, xoffset=0.1, yoffset=0,
                                 left=True, polykwargs={}, textkwargs={}):
    """
    Plots an order of accuracy triangle, assumes log-log axes.
    """
    # Calculate x-position of triangle end
    if left:
        xend = xstart * (10**length)
    else:
        xend = xstart * (10**(-1.0*length))
    yend = 10**(log10(ystart) - rate*(log10(xstart) - log10(xend)))
    a.add_patch(Polygon([[xstart, ystart], [xend, ystart], [xend, yend]], closed=True, fill=False), **polykwargs)
    s = "{}".format(rate)
    xtext = xend * (10**xoffset)
    ytext = 10**(0.5*(log10(ystart)+log10(yend))) * (10**yoffset)
    a.text(xtext, ytext, s, **textkwargs)
