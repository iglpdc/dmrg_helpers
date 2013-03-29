'''
Test for the database class.
'''
import os
from nose.tools import with_setup
from dmrg_helpers.extract.database import Database

def setup_function():
    pass

def teardown_function():
    os.remove('tests/db_test.sqlite3')

@with_setup(setup_function, teardown_function)
def test_database_from_scratch():
    db = Database('tests/db_test.sqlite3')
    db.insert_data_from_file('tests/file_ok.dat')
    assert len(db.get_estimator('n_up')) == 1

@with_setup(setup_function, teardown_function)
def test_database_from_two_files():
    db = Database('tests/db_test.sqlite3')
    db.insert_data_from_file('tests/file_one.dat')
    db.insert_data_from_file('tests/file_two.dat')
    assert len(db.get_estimator('n_up')) == 1
    assert len(db.get_estimator('n_down')) == 1

@with_setup(setup_function, teardown_function)
def test_database_from_two_point_correlators():
    db = Database('tests/db_test.sqlite3')
    db.insert_data_from_file('tests/file_two_point_estimators.dat')
    assert len(db.get_estimator('n_up')) == 1
    assert len(db.get_estimator('n_down')) == 0
    assert len(db.get_estimator('n_up*n_up')) == 1
