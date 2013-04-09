''' Functions to help out with Fourier transform and all that.
'''
import numpy as np
from math import pi
from itertools import izip, chain
from dmrg_helpers.view.xy_data import XYData, XYDataDict
from dmrg_helpers.core.dmrg_exceptions import DMRGException

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
                        estimator_data, x)/length)
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
                      dict(izip(estimator.data.iterkeys(), 
                           fourier_transforms)))

def get_length_directly_from_data(estimator_data):
    """Calculates the length of the system from the estimator data.

    You use this function to cover up for missing information in your data. In
    case you don't have other way to find the length of the DMRG chainm you can
    always do this: assume that the length is the distance between the smallest
    and largest indexes that show up in the estimator sites.

    Note that this is not fine, if for some reason you decide to exclude
    certain parts of the chain from the measurement. 

    Parameters
    ----------
    estimator_data: a EstimatorData object.
        The data you are using.

    Returns
    -------
    length: an int.

    Raises
    ------
    DMRGException if estimator_data is empty.

    """
    if not estimator_data.sites():
        raise DMRGException('Empty estimator data')
    tmp = [int(i) for i in chain.from_iterable(estimator_data.sites())]
    return max(tmp)-min(tmp)+1
