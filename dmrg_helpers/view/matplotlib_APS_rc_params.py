"""matplotlib rc params for APS journals

Gives a dictionary with the proper sizes for APS journals.

Modified from:
    - M.V. DePalatis, 2010-09-01. Licensed under the GNU GPL v3
    - http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples

Examples
--------
>>> import pylab
>>> from pylab import arange, pi, sin, cos
>>> import dmrg_helpers.view.matplotlib_APS_rc_params as aps_params
>>> pylab.rcParams.update(aps_params.aps['params'])
>>> # Generate data
>>> x = pylab.arange(-2*pi, 2*pi, 0.01)
>>> y = sin(x)
>>> # Plot data
>>> pylab.figure(1) #doctest: +ELLIPSIS
<...
>>> pylab.axes(aps_params.aps['axes']) #doctest: +ELLIPSIS
<...
"""
# documentclass 'article' with package 'fullpage'
fullpage = {'params': {'axes.labelsize': 10,
                       'text.fontsize': 10,
                       'legend.fontsize': 10,
                       'xtick.labelsize': 8,
                       'ytick.labelsize': 8,
                       'text.usetex': True,
                       'font.family': 'serif',
                       'figure.figsize': (4.774, 2.950)},
            'axes': [0.150, 0.175, 0.95-0.15, 0.95-0.25]}

# two-column APS journal format
aps = {'params': {'backend': 'ps',
                  'axes.labelsize': 10,
                  'text.fontsize': 10,
                  'legend.fontsize': 10,
                  'xtick.labelsize': 8,
                  'ytick.labelsize': 8,
                  'text.usetex': True,
                  'figure.figsize': (3.4039, 2.1037)},
       'axes': [0.125, 0.2, 0.95-0.125, 0.95-0.2]}
