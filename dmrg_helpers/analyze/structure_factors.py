'''
Functions to calculate common structure factors.
'''
import numpy as np
from dmrg_helpers.analyze.fourier import (
    calculate_fourier_transform_for_two_point_estimator)

def calculate_spin_struct_factor(db):
    """Calculates the (longitudinal) spin structure factor.
    
    Parameters
    ----------
    db: a Database object.
        The database obtained after reading the estimators.dat files.

    Returns
    -------
    A Estimator object with the spin structure factor.

    Example
    -------
    >>> from dmrg_helpers.analyze.structure_factors import (
    ...     calculate_spin_struct_factor)
    >>> from dmrg_helpers.extract.extract import create_db_from_file
    >>> db = create_db_from_file('tests/real_data/static/estimators.dat')
    >>> spin_struct_factor = calculate_spin_struct_factor(db)
    >>> spin_struct_factor.save('spin_struct_factor.dat', 'tests')
    """
    zz_component = db.get_estimator('s_z*s_z')
    result = ( 
        calculate_fourier_transform_for_two_point_estimator(zz_component, 
                                                            'number_of_sites'))
    return result 

def calculate_density_struct_factor(db):
    """Calculates the density (charge) structure factor.
    
    Parameters
    ----------
    db: a Database object.
        The database obtained after reading the estimators.dat files.

    Returns
    -------
    A Estimator object with the charge structure factor.

    Example
    -------
    >>> from dmrg_helpers.analyze.structure_factors import (
    ...     calculate_density_struct_factor)
    >>> from dmrg_helpers.extract.extract import create_db_from_file
    >>> db = create_db_from_file('tests/real_data/static/estimators.dat')
    >>> charge_struct_factor = calculate_density_struct_factor(db)
    >>> charge_struct_factor.save('charge_struct_factor.dat', 'tests')
    """
    fluctuations = db.get_estimator('n*n')
    n = db.get_estimator('n')
    for key, val in fluctuations.data.iteritems():
        n_vals = n.data[key].y_as_np()
        tmp = -1.0 * np.array([n_vals[int(s[0])] * n_vals[int(s[1])] 
                              for s in val.sites()])
        tmp += val.y_as_np()
        val.values_list = tmp.tolist()
    result = ( 
        calculate_fourier_transform_for_two_point_estimator(fluctuations, 
                                                            'number_of_sites'))
    return result 
