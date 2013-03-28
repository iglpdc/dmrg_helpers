'''
Functions to calculate common structure factors.
'''
from dmrg_helpers.analyze.correlator import Correlator

def calculate_spin_struct_factor(database):
    """Calculates the (full) spin structure factor.
    
    Parameters
    ----------
    database: a Database object.
        The database obtained after reading the estimators.dat files.

    Returns
    -------
    A Correlator object with the spin structure factor.
    """
    return Correlator
