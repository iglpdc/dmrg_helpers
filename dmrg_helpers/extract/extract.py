''' Functions to extract data and create databases.
'''
from dmrg_helpers.extract.database import Database
from dmrg_helpers.extract.locate_estimator_files import locate_estimator_files
from dmrg_helpers.core.dmrg_logging import logger 

def create_db_from_file(filename, database_name=":memory:"):
    """Creates a database with the data extracted for a file.

    The file must be an estimators.dat-type file. A new database is created.
    The database is created in memory if no database_name is provided.

    Parameters
    ----------
    filename: a string.
        The filename of the estimators.dat file to be read. The path can be
        relative or absolute.
    database_name: a string (defaulted to ":memory:").
        The name of the file to which the database will be saved.

    Returns
    -------
    A Database object.
    """
    db = Database(database_name)
    db.insert_data_from_file(filename)
    logger.info('File {0} inserted in database {1}'.format(filename,
                                                           database_name))
    return db

def create_db_from_files(files, database_name=":memory:"): 
    """Creates a database with the data extracted for a list fo files.

    The file must be an estimators.dat-type file. A new database is created.
    The database is created in memory if no database_name is provided.

    Parameters
    ----------
    filename: a list of strings.
        The filenames of the estimators.dat files to be read. The path can be
        relative or absolute.
    database_name: a string (defaulted to ":memory:").
        The name of the file to which the database will be saved.

    Returns
    -------
    A Database object.
    """
    db = Database(database_name)
    for filename in files:
        db.insert_data_from_file(filename)
    return db

def create_db_from_dir(root_dir, database_name=":memory:", 
                       pattern='estimators.dat'):
    """Creates a database with the data extracted by crawling a dir.

    The function crawls down a dir a picks up all the files whose name follows
    the `pattern`.  The files must be estimators.dat-type files. A new
    database is created.  The database is created in memory if no database_name
    is provided.

    Parameters
    ----------
    filename: a list of strings.
        The filenames of the estimators.dat files to be read. The path can be
        relative or absolute.
    database_name: a string (defaulted to ":memory:").
        The name of the file to which the database will be saved.

    Returns
    -------
    A Database object.
    """
    files_found = locate_estimator_files(root_dir, pattern)
    db = create_db_from_files(files_found, database_name)
    return db
