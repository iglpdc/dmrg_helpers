''' Functions to help out with Fourier transform and all that.
'''
import numpy as np
from math import pi
from itertools import izip
from dmrg_helpers.view.xy_data import XYData, XYDataDict

def calculate_fourier_comp_for_two_point_estimator(estimator_data, q):
    """Calculates the Fourier transform for an EstimatorData object.

    Parameters
    ----------
    estimator_data: an EstimatorData object.
        The estimator data you want to Fourier transform.
    q: a double.
        The momentum component.
    Returns
    -------
    result: A float with the value of the Fourier component.

    """
    sites = map(list, zip(*estimator_data.sites())) 
    diff = np.array(sites[0], dtype=int)-np.array(sites[1], dtype=int)
    return 2*np.sum(np.multiply(estimator_data.y_as_np(), np.cos(q*diff)))
    #return np.sum(np.multiply(estimator_data.y_as_np(), np.exp(1j*q*diff)).real)

def generate_momenta(length):
    """Generates the allowed momenta for a system of a given `length`.

    Parameters
    ----------
    length: an int.
        the length of the chain you want to generate the momenta for.

    """
    for i in xrange(length):
        yield 2*i*pi/length

def calculate_fourier_transform_for_two_point_estimator_data(estimator_data,
                                                             length):
    """Calculates the Fourier transform for a two-point estimator data set.
    
    Parameters
    ----------
    estimator_data: an EstimatorData object.
        The estimator data you want to Fourier transform.
    length: an int.
        the length of the chain you want to generate the momenta for.

    Returns
    -------
    result: a list of two-tuples with the momenta and the values for the
    Fourier transform.

    """
    return XYData([(x, 
                    calculate_fourier_comp_for_two_point_estimator(
                        estimator_data, x))
            for x in generate_momenta(length)])

def calculate_fourier_transform_for_two_point_estimator(estimator, 
                                                        length_label):
    """Calculates the Fourier transform for a two-point estimator.

    Parameters
    ----------
    estimator: an EstimatorData object.
        The estimator data you want to Fourier transform.
    length_label: a string (default to 'number_of_sites').
        The key you used in the Estimator.meta_keys to store the length of the
        chain in the DMRG code.

    Returns
    -------
    result: a list of two-tuples with the momenta and the values for the
    Fourier transform.

    """
    fourier_transforms = []
    for key, data in estimator.data.iteritems():
        if length_label in estimator.keys:
            length = data.get_metadata_as_dict(key)
        else:
            length = get_length_directly_from_data(data)
        fourier_transforms.append(
            calculate_fourier_transform_for_two_point_estimator_data(data,
                                                                     length))
    return XYDataDict(estimator.meta_keys, 
                      dict(izip(estimator.data.iterkeys(), fourier_transforms)))

def get_length_directly_from_data(estimator_data):
    return int(96)

