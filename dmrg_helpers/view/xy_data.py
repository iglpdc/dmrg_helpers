'''A class to store estimators once retrieved from the database.
'''
import numpy as np
import os
from itertools import izip
from dmrg_helpers.core.dmrg_exceptions import DMRGException

class XYData(object):
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
    def __init__(self, xy_list):
        self.xy_list = xy_list
        self.x_list, self.y_list = self.unzip_in_xy()
    
    @classmethod
    def from_lists(cls, x, y):
        if len(x) != len(y):
            raise DMRGException('Different sizes for lists')
        return cls(izip(x, y))

    @classmethod
    def from_estimator_data(cls, estimator_data):
        return cls(izip(estimator_data.x(), estimator_data.y()))

    def unzip_in_xy(self):
        return map(list, zip(*self.xy_list))

    def x(self):
        """Returns x component in a numpy array.
        """
        return np.array(self.x_list)

    def y(self):
        """Returns y component in a numpy array.
        """
        return np.array(self.y_list, dtype=float)

class XYDataDict(object):
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
    def __init__(self, meta_keys, data):
        self.meta_keys = meta_keys
        self.keys = self.meta_keys.split(':')
        self.data = data

    @classmethod
    def from_estimator(cls, e):
        return cls(e.meta_keys, 
                   dict(izip(e.data.iterkeys(), 
                             map(XYData.from_estimator_data,
                                 e.data.itervalues())))) 

    def get_metadata_as_dict(self, meta_val):
        """Returns a dictionary with metadata.
        
        Parameters
        ----------
        meta_val: one of the meta_vals.
        """
        return dict(izip(self.keys, meta_val.split(':'))) 

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
        output_dir = os.path.abspath(output_dir)
        for key, val in self.generate_filenames(filename).iteritems():
            import pdb; pdb.set_trace()
            tmp = izip(self.data[key].x_list, self.data[key].y_list)
            saved = os.path.join(output_dir, val)
            with open(saved, 'w') as f:
                f.write('\n'.join('%s %s' % x for x in tmp))

    def generate_filenames(self, filename):
        """Generates one filename per entry in data according to `label`.

        Parameters
        ----------
        filename: a string.
            The filename to be created. If it has a '.dat' extension, the 
            extension is stripped off.

        Returns
        -------
        filenames: a list of strings.
            The result is to append the labels with their values to `filename`.

        Raises
        ------
        DMRGException if the label is not found in self.keys.
        """
        if filename[-4:] == '.dat':
            filename = filename[:-4]
        filenames = []
        for meta_val in self.data.keys():
            meta_dict = self.get_metadata_as_dict(meta_val)
            extended_filename = filename
            for key in sorted(meta_dict.iterkeys()):
                extended_filename += '_'+str(key)+'_'+str(meta_dict[key])
            extended_filename += '.dat'
            filenames.append(extended_filename)
        return dict(izip(self.data.keys(), filenames))

    def plot(self):
        """Plots the data.

        Makes a plot of the correlator data. If the correlator contains several
        sets of parameters, graphs all in the same plot.

        """
        pass
