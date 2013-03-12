'''
File: estimator_name.py
Author: Ivan Gonzalez
Description: A class for estimator names.
'''
from dmrg_helpers.core.tuple_to_key import tuple_to_key
from sqlite3 import register_adapter, register_converter

class EstimatorName(object):
    """A class to store estimator names into the database.
    
    You use this function to handle estimator names inside the databaseself.

    Parameters
    ----------
    operators: a tuple of strings.
        The names of the several single-site operators that compose the
        correlator.
    """
    def __init__(self, operators):
        super(EstimatorName, self).__init__()
        self.operators = operators

def adapt_estimator_name(estimator_name):
    '''Adapts the estimator name to the database format.

    You use this function to introduce an estimator name into the database.

    Parameters
    ----------
    estimator_name: an EstimatorName.
        The estimator name you want to adapt.

    Returns
    -------
    a string in the format to be stored in the database.
    '''
    return tuple_to_key(estimator_name.operators)
   
def convert_estimator_name(s):
    '''Converts back an entry of the database to an EstimatorName object.

    You use this function when extracting an estimator name from the database.

    Parameters
    ----------
    s : a string
        An estimator name as stored in the database.

    Returns
    -------
    an EstimatorName object.
    '''
    operators = s.split(':')
    return EstimatorName(operators)

register_adapter(EstimatorName, adapt_estimator_name)
register_converter('estimator_name', convert_estimator_name)
