'''
Functions to calculate common structure factors.
'''
from dmrg_helpers.extract.estimator import Estimator
from itertools import izip

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
    >>> from dmrg_helpers.extract.database import Database
    >>> db = Database() # just empty for the example
    >>> spin_struct_factor = calculate_spin_struct_factor(db)
    >>> spin_struct_factor.save('spin_struct_factor.dat', 'tests')
    """
    zz_component = db.get_estimator('S_z*S_z')

    meta_keys = zz_component.meta_keys
    result = Estimator('spin_struct_factor', meta_keys)
    result.data = dict(izip(zz_component.x(), zz_component.y()))

    return result 
