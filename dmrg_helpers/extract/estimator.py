'''A class to store estimators once retrieved from the database.
'''
import numpy as np
import os
from itertools import izip
from dmrg_helpers.extract.estimator_site import EstimatorSite
from dmrg_helpers.view.xy_data import XYDataDict

class EstimatorData(object):
    """An auxiliary class to hold the numerical data from an Estimator.

    Estimators contain numerical data and you use this class to store them. 
    
    Parameters
    ----------
    sites_list: an list of tuples of ints.
        The sites at which each of the single-site operators of the correlator
        act.
    values_list: an list of doubles.
        The value of the correlator at each site in the sites_list.
    """
    def __init__(self):
        self.sites_list = []
        self.values_list = []

    def add(self, sites, value):
        """Adds data"""
        self.sites_list.append(sites)
        self.values_list.append(value)
    
    def sites(self):
        """Returns the sites a list of tuples
        """
        return [i.sites for i in self.sites_list]

    def x(self):
        """Returns the first site as an index of the chain in a list
        """
        return map(EstimatorSite.x, self.sites_list)

    def x_as_np(self):
        """Returns the first site as an index of the chain in a numpy array.
        """
        return np.array(map(EstimatorSite.x, self.sites_list), dtype=int)
    
    def y(self):
        """Returns the values as a list.
        """
        return self.values_list

    def y_as_np(self):
        """Returns the values as a numpy array.
        """
        return np.array(self.values_list, dtype=float)

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
    keys: a tuple of strings.
        Obtained from meta_keys. Used to inspect which are the keys, like
        parameters of the Hamiltonian that label your data.
    data: a dict of a string on EstimatorData.
        Contains the actual values for the estimator. The key in the dictionary 
        is given by the parameters that characterize the data, such as 
        Hamiltonian parameters of the DMRG run or the system length. The value
        of the dictionary is given by a EstimatorData object that holds the 
        numerical part of the estimator.
    """
    def __init__(self, name, meta_keys):
        self.name = name
        self.meta_keys = meta_keys
        self.keys = self.meta_keys.split(':')
        self.data = {}

    def __len__(self):
        """Returns number of entry of the data dict.

        You use this function to inspect which are the keys, like parameters of 
        the Hamiltonain that label your data.
        """
        return len(self.data)

    def get_metadata_as_dict(self, meta_val):
        """Returns a dictionary with metadata.
        
        Parameters
        ----------
        meta_val: one of the meta_vals.
        """
        return dict(izip(self.keys, meta_val.split(':'))) 

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

    def save(self, filename, output_dir=os.getcwd()):
        """Saves the correlator data to a file.

        You use this function to save data for a correlator to a file. If there 
        is more that one set of data in the Correlator, for example, because
        you have data for different systems sizes, each set will be saved into
        a different file. The name of these files will be obtained by appending 
        the names and values of the meta_data to `filename`.

        Inside the file the data is organized in two columns: the first is a 
        site of the chain, and the second the value of the correlator.
        """
        xy_data_dict = XYDataDict.from_estimator(self)
        xy_data_dict.save(filename, output_dir)

    def plot(self):
        """Plots the data.

        Makes a plot of the correlator data. If the correlator contains several
        sets of parameters, graphs all in the same plot.
        """
        xy_data_dict = XYDataDict.from_estimator(self)
        xy_data_dict.plot()
