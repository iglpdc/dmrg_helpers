'''A class for estimator sites.
'''
from dmrg_helpers.extract.tuple_to_key import tuple_to_key
from sqlite3 import register_adapter, register_converter

class EstimatorSite(object):
    """A class to store estimator sites into the database.
    
    You use this function to handle estimator sites inside the database.
    Eventually, the sites will be transformed to ints, but here you don't
    care.

    Parameters
    ----------
    sites: a tuple of strings.
        The sites where the several single-site operators that compose the
        correlator act.
    """
    def __init__(self, sites):
        super(EstimatorSite, self).__init__()
        self.sites = sites

    def x(self):
        """Returns the first elememt of the tuple as an int.
        """
        return int(self.sites[0])

def adapt_estimator_site(estimator_site):
    '''Adapts the estimator site to the database format.

    You use this function to introduce an estimator site into the database.

    Parameters
    ----------
    estimator_site: an EstimatorSite.
        The estimator site you want to adapt.

    Returns
    -------
    a string in the format to be stored in the database.
    '''
    return tuple_to_key(estimator_site.sites)
   
def convert_estimator_site(s):
    '''Converts back an entry of the database to an EstimatorSite object.

    You use this function when extracting an estimator site from the database.

    Parameters
    ----------
    s : a string
        An estimator site as stored in the database.

    Returns
    -------
    an EstimatorSite object.
    '''
    sites = s.split(':')
    return EstimatorSite(sites)

register_adapter(EstimatorSite, adapt_estimator_site)
register_converter('estimator_site', convert_estimator_site)
