'''
Test for the database class.
'''
import os
from nose.tools import with_setup
import dmrg_helpers.extract.extract as ex

def setup_function():
    pass

def teardown_function():
    os.remove('tests/db_test.sqlite3')

@with_setup(setup_function, teardown_function)
def test_create_db_from_file():
    db = ex.create_db_from_file('tests/file_ok.dat', 'tests/db_test.sqlite3')
    assert len(db.get_estimator('n_up')) == 2

@with_setup(setup_function, teardown_function)
def test_create_db_from_files():
    files = ['tests/file_one.dat', 'tests/file_two.dat']
    db = ex.create_db_from_files(files, 'tests/db_test.sqlite3')
    assert len(db.get_estimator('n_up')) == 2
    assert len(db.get_estimator('n_down')) == 2

@with_setup(setup_function, teardown_function)
def test_create_db_from_dir():
    db = ex.create_db_from_dir('tests/results', 'tests/db_test.sqlite3')
    assert len(db.get_estimator('n_up')) == 2
    assert len(db.get_estimator('n_down')) == 2

