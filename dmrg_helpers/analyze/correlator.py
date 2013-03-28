'''A class to store correlators
'''

class Correlator(object):
    """A class for storing data for correlators once retrieved for a database.

    You use this class to store the result of calling the function
    get_estimator in the Database class. Additionally, you can create new
    correlators by making linear combinations of other correlators.

    Parameters
    ----------
    name: a string.
        The name of the correlator. 
    meta_dict: a dict.
        A dict of strings on string which contains the meta data, such as
        Hamiltonian parameters, for the correlator.
    data: a Data object.
        The data for the correlator composed by integer-labelled sites and the
        data for each site.
    """
    def __init__(self, name=None, meta_dict=None, data=None):
        super(Correlator, self).__init__()
        self.name = name
        self.meta_dict = meta_dict
        self.data = []
        if data:
            self.data.append(data)
    
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
