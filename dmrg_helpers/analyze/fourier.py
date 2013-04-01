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
    return 2*np.sum(np.multiply(values*np.cos(q*diff)))
    #return np.sum(np.multiply(values*np.exp(1j*q*diff)).real)

def generate_momenta(length):
    """Generates the allowed momenta for a system of a given `length`.

    Parameters
    ----------
    length: an int.
        the length of the chain you want to generate the momenta for.

    """
    for i in xrange(length):
        yield 2*i*pi/length

def calculate_fourier_transform_for_two_point_correlator(sites, values,
                                                         length):
    """Calculates the Fourier transform for a two-point correlator.
    
    Parameters
    ----------
    sites: a tuple of two lists of ints.
        The two sites where the correlator lives. 
    values: a numpy array of floats.
        The data for the correlator.
    length: an int.
        the length of the chain you want to generate the momenta for.

    Returns
    -------
    result: a list of two-tuples with the momenta and the values for the
    Fourier transform.

    """
    return [(x, calculate_fourier_comp_for_two_point_correlator(x))
            for x in generate_momenta(length)]
