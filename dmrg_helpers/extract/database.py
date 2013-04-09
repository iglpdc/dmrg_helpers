'''A module to construct a database with estimators.
'''
from dmrg_helpers.core.dmrg_exceptions import DMRGException
from dmrg_helpers.core.dmrg_logging import logger
from dmrg_helpers.extract.tuple_to_key import tuple_to_key
from dmrg_helpers.extract.estimator import Estimator
from dmrg_helpers.extract.estimator_name import EstimatorName
from dmrg_helpers.extract.estimator_site import EstimatorSite
from dmrg_helpers.extract.process_estimator_name import process_estimator_name
from dmrg_helpers.extract.reader import FileReader
import os
import sqlite3

def adapt_meta_data(file_reader):
    '''Creates the metadata that label the file.

    Parameters 
    ----------
    file_reader: a FileReader.
        The data read from an estimators file.

    Returns
    -------
    meta_keys: a string.
        The keys from the metadata dictionary joined by the ':' delimiter. 
        The keys are alphabetically ordered.
    meta_values: a string.
        The values from the metadata dictionary joined by the ':' delimiter. 
    '''
    sorted_dict = [ (k, file_reader.meta[k]) for k in sorted(file_reader.meta.keys()) ]
    meta_keys = tuple_to_key(x[0] for x in sorted_dict)
    meta_vals = tuple_to_key(x[1] for x in sorted_dict)
    return meta_keys, meta_vals

class Database(object):
    """A database to store the estimators

    You use this class to create a sqlite3 database where you store all the
    estimators. You can extract the data from the database for a given
    estimator and filter them in the ways you please.

    Parameters
    ----------
    filename: a string.
        The name of the file that will store the database. It's never 
        overwritten.
    meta_keys: a dict of strings on strings.
        The meta comments from the file. It has information about the
        parameters of the Hamiltonian, for example, of the run.
    """
    def __init__(self, filename=":memory:"):
        self.filename = filename
        if filename != ":memory:":
            if os.path.exists(filename):
                raise DMRGException('Cannot create db: file exists already')
        self.meta_keys = None

        self.conn = sqlite3.connect(self.filename, 
                                    detect_types=sqlite3.PARSE_DECLTYPES)
        self.c = self.conn.cursor()
        self.create_estimators_table()
        logger.info('Creating database {}'.format(filename))

    def __del__(self):
        self.c.close()
        self.conn.close()

    def create_estimators_table(self):
        '''Creates the table for the estimators.
        '''
        with self.conn:
            self.c.execute("create table estimators (name estimator_name, \
                                                     sites estimator_site, \
                                                     data real, \
                                                     meta_values text)")

    def insert_data_from_file(self, filename):
        '''Insert into the database the data in `filename`.

        Parameters
        ----------
        filename: a string.
            The filename of the estimators.dat file to be read. The path can be
            relative or absolute.
        '''
        file_reader = FileReader()
        file_reader.read(filename)
        meta_keys, meta_vals = adapt_meta_data(file_reader)
        self.check_meta_keys(meta_keys)

        with self.conn:
            for line in file_reader.data:
                n, s = process_estimator_name(line[0])
                n = EstimatorName(n)
                s = EstimatorSite(s)
                d = line[1]
                self.c.execute("insert into estimators(\
                     name, sites, data, meta_values) values(?,?,?,?)", 
                     (n, s, d, meta_vals))

    def check_meta_keys(self, meta_keys):
        '''Checks whether the `meta_keys` for the file are alright.

        You use this function to check whether you can insert data from this 
        file in the current database.

        Parameters
        ----------
        meta_keys: a string.
            The meta_keys after adapting them.
        '''
        if self.meta_keys is None:
            self.meta_keys = meta_keys
        elif self.meta_keys != meta_keys:
            raise DMRGException('Incompatible file: meta_keys are different')
        else:
            pass

    def get_estimator(self, estimator_name, site_expression=None):
        '''Gets an estimator from the database.

        You use this function to get the values for particular estimators from 
        all the stuff you have in the database.

        Parameters
        ----------
        estimator_name: a string.
            The operators acting in each site, in order, and separated by '*'.
        site_expression: a string.
            Not implemented right now.

        Returns
        -------
        result: an Estimator object with all the data found for this
        estimator.
        '''
        n = EstimatorName(estimator_name.split('*'))
        self.c.execute('select * from estimators where name = ?', (n,))
        fetched = self.c.fetchall()
        result = Estimator(estimator_name, self.meta_keys)
        result.add_fetched_data(fetched)
        return result
