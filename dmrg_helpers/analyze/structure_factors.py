'''
Functions to calculate common structure factors.
'''
from dmrg_helpers.analyze.fourier import (
    calculate_fourier_transform_for_two_point_estimator)

def calculate_spin_struct_factor(db):
    """Calculates the (full) spin structure factor.
    
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
    >>> db = create_db_from_file('tests/real_data/static/estimators.dat',
    ...                          'tests/real_data/real_data.sqlite')
    >>> spin_struct_factor = calculate_spin_struct_factor(db)
    >>> spin_struct_factor.save('spin_struct_factor.dat', 'tests')
    >>> # delete the database file
    >>> import os
    >>> os.remove('tests/real_data/real_data.sqlite')
    """
    zz_component = db.get_estimator('s_z*s_z')
    result = ( 
        calculate_fourier_transform_for_two_point_estimator(zz_component, 
                                                            'number_of_sites'))
    return result 
