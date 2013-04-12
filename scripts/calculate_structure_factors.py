#!/usr/bin/env python
"""Calculates the spin and density structure factors.

This script crawls down a directory finding all the estimator file, i.e. those
whose name is 'estimators.dat'. It reads each file and store the estimator data
in a database. Then you calculate the structure factors reading the data you
ned from the database with all the info. The structure factor data are saved
into a bunch of files, one per parameter set.

The estimator files must have metadata included. 

Usage:
  calculate_structure_factors.py [--in=DIR, --out=DIR, --replot_from=DIR]
  calculate_structure_factors.py -h | --help

Options:
  -h --help            Shows this screen.
  --in=DIR             Directory to crawl down for estimator files 
                       [default: ./]
  --out=DIR            Ouput directory where structure factor data is saved 
                       [default: ./]
  --replot_from=DIR    Replots from pickled data stored in DIR 

"""
import os
import pickle
import math
import numpy as np
from docopt import docopt
import logging
from itertools import izip
# Temporary patch to avoid installing the dmrg_helpers package.
import inspect
import sys
script_full_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
sys.path.insert(0, os.path.dirname(os.path.dirname(script_full_path)))
# patch ends
from dmrg_helpers.extract.extract import create_db_from_dir
from dmrg_helpers.analyze.structure_factors import (
        calculate_spin_struct_factor, calculate_density_struct_factor)
from dmrg_helpers.view.xy_data import XYDataDict
# Let's import the stuff to make plot look good for publication in APS.
import matplotlib.pyplot as plt
import matplotlib as mpl
from dmrg_helpers.view.matplotlib_APS_rc_params import aps
mpl.rcParams.update(aps['params'])

# Band structure calculations for the system of free fermions
# ----------------------------------------------------------
# 
# These are a few functions to help you determine the band structure and the 
# chemical potential at half-filling.

def theta(dispersion, k , mu):
    if dispersion(k) > mu:
        return 0.0
    else:
        return 1.0

def calculate_number_of_electrons_for_mu(mu, dispersion, length):
    return 2*sum([theta(dispersion, 2*math.pi*k/length, mu) 
                  for k in xrange(length)])

def determine_mu_at_half_filling(dispersion, k_max, k_min, length):
    tmp = [(mu, calculate_number_of_electrons_for_mu(mu, dispersion, length)) 
        for mu in np.linspace(dispersion(k_min), dispersion(k_max), 100)]
    return next(x[0] for x in tmp if x[1] > length -1)

def find_fermi_momenta(mu, dispersion, length):
    momenta = [2*math.pi*k/length for k in xrange(length)]
    indexes = np.nonzero(
              np.diff([theta(dispersion, k, mu) for k in momenta]))[0].tolist()
    return [momenta[i] for i in indexes]

def find_fermi_momenta_at_half_filling(dispersion, k_max, k_min,
                                       number_of_sites):
    mu = determine_mu_at_half_filling(dispersion, k_max, k_min, 
                                      number_of_sites)
    return find_fermi_momenta(mu, dispersion, number_of_sites)

def calculate_K_over_t(estimator):
    """Calculates the value of :math:`K/t` for an estimator.

    You can get estimators from calling the `get_estimator` function on the
    Database class, or as the result of calling the functions that calculate
    structure factors.

    Parameters
    ----------
    estimator: an XYDataDict object.
        The thing you want to calculate the parameter from.

    Returns
    -------
    A dictionary with the same keys as the estimator and :math:`K/t` as values.

    """
    k_over_t = []
    for k in estimator.data.iterkeys():
        params = estimator.get_metadata_as_dict(k)
        try:
            tmp = str(float(params['Kring'])/float(params['t']))
        except ZeroDivisionError:
            tmp = r"$\infty$"
        k_over_t.append(tmp)
    return dict(izip(estimator.data.iterkeys(), k_over_t))

def plot_structure_factor(structure_factor, k_fs, y_label, max_plots,
                          selected_keys, K_over_t_crit=None):
    """Pretty plots the structure factor.
    """
    # Make the figure nice
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel(r'$q$')
    ax.set_ylabel(y_label)
    ax.set_xlim((0.0, math.pi))
    ax.set_xticks([0.0, math.pi/2, math.pi, (k_fs[2] - k_fs[1]) % math.pi, 
                   (k_fs[0] - k_fs[3]) % math.pi, 
                   (k_fs[2] - k_fs[0]) % math.pi])
    ax.set_xticklabels(['0', r'$\pi/2$', r'$\pi', r'$2k_{F1}$', r'$2k_{F2}$', 
                        r'$k_{F2}-k_{F1}$'])
    max_y = structure_factor.get_max_y()
    min_y = structure_factor.get_min_y()
    ax.set_yticks([0.0, max_y - min_y])
    #ax.set_yticks([min_y, max_y])
    ax.set_yticklabels(['0', "{0:.2f}".format(max_y-min_y)])
    ax.set_ylim([0.0, 1.1 * (max_y - min_y)]);
    # Get the data and plot

    data = structure_factor.get_data_for_plots(calculate_K_over_t)
    if not selected_keys:
        selected_keys = select_plot_based_to_avoid_cluttering(data, max_plots, 
                                                              K_over_t_crit)
    data = { key[1]: data[key[1]] for key in selected_keys }
    for d in data.itervalues():
        ax.plot(d[1], d[2]-d[2][0], 'b-')

    return fig

def select_plot_based_to_avoid_cluttering(data, max_plots, K_over_t_crit):
    """Picks up some of the :math:`K/t` values guaranteing certain spacing.

    You use this function to select which values of :math:`K/t` you want to
    plot. The values are selected by guaranteing that the distance between
    intercepts of the plots and a vertical axis is at least `sep`. 

    The smallest, highest and critical values are always included.

    Parameters
    ----------
    data: a XYDataDict.
        The whole data you want to plot.
    max_plots:
        The maximum number of selected plots. The actual number can be smaller.
    K_over_t_crit: a string.
        The value of critical value of :math:`K/t`.

    Returns
    -------
    A sublist of the data.keys() with the selected plots.

    """
    mid_x_axis = len(data[data.keys()[0]][1])/2  # Terrible!
    vals_at_mid_x_axis = { k: v[2][mid_x_axis] for k, v in data.iteritems() }
    if K_over_t_crit is not None:
        transition = vals_at_mid_x_axis[K_over_t_crit]
    else:
        transition = None
    all = sorted([(b, a) for a, b in vals_at_mid_x_axis.iteritems()])
    sep = (all[-1][0] - all[0][0]) / max_plots
    selected = [ all[0] ]
    for item in all:
        if (item[0] > selected[-1][0] + sep and 
            item[0] < all[-1][0] - sep):
                if transition is not None:
                    if abs(item[0] - transition) > sep:
                        selected.append(item)
                else:
                        selected.append(item)

    return selected

def main(args):

    output_dir = args['--out']
    if not args['--replot_from']:

        # Create a database with all the files under dir

        db = create_db_from_dir(args['--in'])
        
        # Calculate the structure factors

        logging.info('Calculating spin structure factors')
        spin_struct_factor = calculate_spin_struct_factor(db)
        spin_struct_factor.save('spin_structure_factor.p', output_dir)
        logging.info('Calculating charge structure factors')
        charge_struct_factor = calculate_density_struct_factor(db)
        charge_struct_factor.save('charge_structure_factor.p', output_dir)

        # Find the Fermi momenta to use in the structure factor plots
        #
        # You use need the band dispersion and to determine a few parameters

        def two_bands(k, t_p=0.75):
            return -2*math.cos(k)-2*t_p*math.cos(2*k)

        # hard_code shit
        number_of_sites = 96
        k_max = math.acos(-1.0/3)
        k_min = 0.0

        k_fs = find_fermi_momenta_at_half_filling(two_bands, k_max, k_min,
                                                  number_of_sites)
        pickle.dump(k_fs, open(os.path.join(output_dir, 'k_fs.p'), "wb"))

    else:
        replot_from = args['--replot_from']
        spin_struct_factor = XYDataDict.load('spin_structure_factor.p', 
                                             replot_from)
        charge_struct_factor = XYDataDict.load('charge_structure_factor.p', 
                                               replot_from)
        f = os.path.join(os.path.abspath(replot_from), 'k_fs.p')
        k_fs = pickle.load(open(f, "rb"))

    # Plot the structure factors
    
    selected_keys = []
    y_label = r'$\langle \vec{S}_{q}\cdot\vec{S}_{-q}\rangle$'
    spin_struct_plot = plot_structure_factor(spin_struct_factor, k_fs, y_label,
                                             20, selected_keys)
    print selected_keys
    logging.info('Selected K/t to plot: {}'.format([k[0] for k in
                  selected_keys]))
    f = os.path.join(os.path.abspath(output_dir), 'spin_struct_factor.pdf')
    spin_struct_plot.savefig(f)
    selected_keys = []
    y_label = r'$\langle \delta n_{q}\delta n_{-q}\rangle$'
    charge_struct_plot = plot_structure_factor(charge_struct_factor, k_fs, 
                                               y_label, 20, selected_keys)
    print selected_keys
    logging.info('Selected K/t to plot: {}'.format([k[0] for k in
                  selected_keys]))
    f = os.path.join(os.path.abspath(output_dir), 'charge_struct_factor.pdf')
    charge_struct_plot.savefig(f)

if __name__ == '__main__':
    args = docopt(__doc__, version = 0.1)
    main(args)
