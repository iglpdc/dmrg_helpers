''' Functions to help out with Fourier transform and all that.
'''
import numpy as np
from math import pi

def calculate_fourier_comp_for_two_point_correlator(sites, values, q):
    """Calculates the Fourier component for a two-point correlator.

    The sites and values must be symmetrized. 

    Parameters
    ----------
    sites: a tuple of two lists of ints.
        The two sites where the correlator lives. 
    values: a numpy array of floats.
        The data for the correlator.
    q: a double.
        The momentum component.
    Returns
    -------
    result: A float with the value of the Fourier component.
    """
    first_site, second_site = zip(*sites) # unzip using zip!
    diff = np.array(first_site)-np.array(second_site)
    return np.sum(np.multiply(values*np.exp(1j*q*diff)).real)

def generate_momenta(length):
    """Generates the allowed momenta for a system of a given `length`.

    Parameters
    ----------
    length: an int.
        The length of the chain you want to generate the momenta for.

    """
    i = 0
    while i < length:
        yield 2*i*pi/length

