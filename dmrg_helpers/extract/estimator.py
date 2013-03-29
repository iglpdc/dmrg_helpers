'''A class to store estimators once retrieved from the database.
'''
import numpy as np
from dmrg_helpers.extract.estimator_site import EstimatorSite

class EstimatorData(object):
    """An auxiliary class to hold the numerical data from an Estimator.

    Estimators contain numerical data and you use this class to store them. 
    
    Parameters
    ----------
    sites_array: an array of tuples of ints.
        The sites at which each of the single-site operators of the correlator
        act.
    values_array: an array of doubles.
        The value of the correlator at each site in the sites_array.
    """
    def __init__(self):
        self.sites_array = []
        self.values_array = []

    def add(self, sites, value):
        """Adds data"""
        self.sites_array.append(sites)
        self.values_array.append(value)

    def x(self):
        """Returns the first site as an index of the chain in a numpy array.
        """
        return np.array(map(EstimatorSite.x, self.sites_array), dtype=int)

    def y(self):
        """Returns the values as a numpy array.
        """
        return np.array(self.values_array, dtype=float)

class Estimator(object):
    """A class for storing data for estimators once retrieved for a database.

    You use this class to store the result of calling the function
    get_estimator in the Database class. Additionally, you can create new
    correlators by making linear combinations of other correlators.

    Parameters
    ----------
    name: a tuple of strings.
        Each of the names of the single site operators that make up the
        estimator. 
    meta_keys: a string.
        The keys from the metadata dictionary joined by the ':' delimiter. 
        The keys are alphabetically ordered. It stores the metadata of the
        estimator, like the names of the parameters of the Hamiltonian.
    data: a dict of a string on EstimatorData.
        Contains the actual values for the estimator. The key in the dictionary 
        is given by the parameters that characterize the data, such as 
        Hamiltonian parameters of the DMRG run or the system length. The value
        of the dictionaty is given by a EstimatorData object that holds the 
    """
    def __init__(self, name, meta_keys):
        self.name = name
        self.meta_keys = meta_keys
        self.data = {}

    def __len__(self):
        """Returns number of entry of the data dict.

        Mostly for testing purposes.
        """
        return len(self.data)

    def add_fetched_data(self, fetched_data):
        """Adds data fecthed from the database to the Estimator.

        Parameters
        ----------
        fetched_data : data as it comes for the database.
            This is a list of tuples. The elements of the tuple are: an
            EstimatorName, an EstimatorSite, the data for the correlator, and
            a string with the values of the meta_keys.
        """
        for d in fetched_data:
            meta_vals = d[3]
            if meta_vals not in self.data:
                self.data[meta_vals] = EstimatorData()
            self.data[meta_vals].add(d[1], d[2])

    def save(self, filename):
        """Saves the correlator data to a file.

        Parameters
        ----------
        filename: a string.
            The filename to be created.
        """
        pass

    def plot(self, label = None):
        """Plots the data.

        Makes a plot of the correlator data. If the correlator contains several
        sets of parameters, graphs all in the same plot.

        Parameters
        ----------
        label: a string.
            You can use it to print a label. The label must be one of the
            keys for the dictionary of the correlator.
        """
        pass
