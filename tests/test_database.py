'''
Test for the database class.
'''
import os
from nose.tools import with_setup
from dmrg_helpers.extract.database import Database
from dmrg_helpers.extract.reader import FileReader

def setup_function():
    pass

def teardown_function():
    os.remove('tests/db_test.sqlite3')

@with_setup(setup_function, teardown_function)
def test_database_from_scratch():
    file_reader = FileReader()
    file_reader.read('tests/file_ok.dat')
    db = Database('tests/db_test.sqlite3')
    db.insert_data_from_file(file_reader)
    assert len(db.get_estimator('n_up')) == 2

@with_setup(setup_function, teardown_function)
def test_database_from_two_files():
    db = Database('tests/db_test.sqlite3')
    file_reader = FileReader()
    file_reader.read('tests/file_one.dat')
    db.insert_data_from_file(file_reader)
    file_reader = FileReader()
    file_reader.read('tests/file_two.dat')
    db.insert_data_from_file(file_reader)
    assert len(db.get_estimator('n_up')) == 2
    assert len(db.get_estimator('n_down')) == 2

@with_setup(setup_function, teardown_function)
def test_database_from_two_point_correlators():
    db = Database('tests/db_test.sqlite3')
    file_reader = FileReader()
    file_reader.read('tests/file_two_point_estimators.dat')
    db.insert_data_from_file(file_reader)
    assert len(db.get_estimator('n_up')) == 2
    assert len(db.get_estimator('n_down')) == 0
    assert len(db.get_estimator('n_up*n_up')) == 2
